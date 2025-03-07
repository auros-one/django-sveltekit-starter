import logging
from uuid import UUID

import django_filters
from asgiref.sync import async_to_sync
from django.contrib.postgres.search import SearchQuery, SearchRank, TrigramSimilarity
from django.db.models import Case, F, IntegerField, OuterRef, Subquery, Value, When
from django.http import Http404
from django.shortcuts import get_object_or_404
from drf_spectacular.utils import (
    OpenApiParameter,
    extend_schema,
    extend_schema_view,
    inline_serializer,
)
from rest_framework import serializers, status
from rest_framework.exceptions import APIException, ValidationError
from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveAPIView
from rest_framework.permissions import IsAdminUser
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_api_key.permissions import HasAPIKey

from project.accounts.models import User
from project.applications.models import Application, ApplicationStatus
from project.core.utils.views import LargeResultsSetPagination
from project.resumes.models import Resume
from project.search.services.matching import get_match_ids_from_user
from project.vacancies.models import (
    ScrapedVacancy,
    ScrapingTask,
    Status,
    Vacancy,
    VacancyRating,
)
from project.vacancies.serializers import (
    ScrapedVacancySerializer,
    ScrapingTaskSerializer,
    URLListSerializer,
    VacancyRatingSerializer,
    VacancySerializer,
    VacancyStatsSerializer,
)
from project.vacancies.services.application_status_handler import (
    handle_disinterest,
    handle_interest,
)
from project.vacancies.services.job_finder.serperdev import execute_serperdev_search
from project.vacancies.tasks import process_pending_vacancies_task

logger = logging.getLogger(__name__)

# Vacancies


class VacancyFilter(django_filters.FilterSet):
    min_salary = django_filters.NumberFilter(
        field_name="min_salary",
        lookup_expr="gte",
        label="Filter by minimum salary",
    )
    max_salary = django_filters.NumberFilter(
        field_name="max_salary",
        lookup_expr="lte",
        label="Filter by maximum salary",
    )
    company = django_filters.CharFilter(
        field_name="company__name",
        lookup_expr="icontains",
        label="Filter by company name",
    )
    published_at = django_filters.DateFromToRangeFilter(
        label="Filter by publication date"
    )
    search = django_filters.CharFilter(
        method="search_vacancies", label="Search vacancies"
    )
    skills = django_filters.CharFilter(method="filter_skills", label="Filter by skills")
    resume_based = django_filters.BooleanFilter(
        method="resume_based_filter", label="Filter by resume"
    )

    class Meta:
        model = Vacancy
        fields = [
            "published_at",
            "search",
            "min_salary",
            "max_salary",
            "skills",
        ]

    def filter_skills(self, queryset, name, value):
        skills = self.request.query_params.getlist("skills")  # type: ignore[attr-defined]
        if skills:
            # Use AND logic by chaining filter calls
            for skill in skills:
                queryset = queryset.filter(skills__name__iexact=skill)
            return queryset.distinct()
        return queryset

    def resume_based_filter(self, queryset, name, value):
        if not value:
            return queryset
        if not self.request:
            raise APIException("User not authenticated")
        user: User = self.request.user

        # Get job matches for the candidate
        matched_vacancy_ids = get_match_ids_from_user(user)
        # Create a Case expression to preserve the order
        preserved_order = Case(
            *[
                When(id=id, then=Value(position))
                for position, id in enumerate(matched_vacancy_ids)
            ],
            output_field=IntegerField(),
        )
        # Apply the filter and ordering to the original queryset
        matched_vacancies = (
            queryset.filter(id__in=matched_vacancy_ids)
            .annotate(custom_order=preserved_order)
            .order_by("custom_order")
        )
        return matched_vacancies

    def search_vacancies(self, queryset, name, value):
        if not value:
            return queryset

        icontains_queryset = queryset.filter(title__icontains=value)
        # Advanced search for longer queries
        search_query = SearchQuery(value)
        trigram_queryset = (
            queryset.annotate(
                rank=SearchRank(F("search_vector"), search_query),
                similarity=TrigramSimilarity("title", value),
            )
            .filter(similarity__gt=0.3)
            .order_by("-similarity", "-rank")
        )
        return (trigram_queryset | icontains_queryset).distinct()


@extend_schema_view(
    get=extend_schema(
        operation_id="List Vacancies",
        responses={200: VacancySerializer(many=True)},
        parameters=[
            OpenApiParameter(
                name="skills",
                type=str,
                description="Filter by skills",
                required=False,
                explode=False,
                style="form",
                many=True,
            ),
        ],
    )
)
class ListVacancyView(ListAPIView):
    queryset = Vacancy.objects.prefetch_related("skills").all()
    serializer_class = VacancySerializer
    pagination_class = LargeResultsSetPagination
    filterset_class = VacancyFilter

    def get_queryset(self):
        user_rating_subquery = VacancyRating.objects.filter(
            user=self.request.user, vacancy=OuterRef("pk")
        ).values("rating")[:1]

        return Vacancy.objects.prefetch_related("skills").annotate(
            user_rating=Subquery(user_rating_subquery)
        )


class GetVacancyView(RetrieveAPIView):
    queryset = Vacancy.objects.prefetch_related("skills").all()
    lookup_field = "slug"
    serializer_class = VacancySerializer


# Scraped Vacancy


class CreateScrapedVacancyView(CreateAPIView):
    permission_classes = [HasAPIKey]
    serializer_class = ScrapedVacancySerializer

    def perform_create(self, serializer):
        url = serializer.validated_data["url"]
        if ScrapedVacancy.objects.filter(url=url).exists():
            raise ValidationError(
                {"url": ["Scraped vacancy with this URL already exists."]}
            )
        serializer.save()


# POST Vacancy Interest (Create JobMatch object)


class GetVacancyInterestView(APIView):

    @extend_schema(
        operation_id="get_vacancy_interest_status",
        responses={
            200: {
                "type": "object",
                "properties": {
                    "is_interested": {"type": "boolean"},
                },
            }
        },
    )
    def get(self, request, vacancy_id: UUID, *args, **kwargs):
        """Retrieve the interest status and application status for a specific vacancy."""
        vacancy: Vacancy = get_object_or_404(Vacancy, id=vacancy_id)
        is_interested = Application.objects.filter(
            vacancy=vacancy.id,
            user=request.user,
        ).exists()

        return Response(
            {
                "is_interested": is_interested,
            }
        )


class ToggleVacancyInterestView(APIView):

    @extend_schema(
        operation_id="toggle_vacancy_interest_status",
        request=None,
        responses={
            201: {"type": "string"},
            200: {"type": "object", "properties": {"message": {"type": "string"}}},
            400: {"type": "object", "properties": {"error": {"type": "string"}}},
        },
    )
    def post(self, request, vacancy_id: UUID, is_interested: str, *args, **kwargs):
        """Toggle the interest status of the user for a specific vacancy."""
        vacancy = get_object_or_404(Vacancy, id=vacancy_id)
        resume = get_object_or_404(Resume, user=request.user, is_primary=True)
        application = Application.objects.filter(
            vacancy=vacancy, user=request.user, resume=resume
        ).first()

        if is_interested.lower() != "true":
            handle_disinterest(application, request.user, vacancy)
            return Response(
                {"message": "Application deleted"}, status=status.HTTP_200_OK
            )

        # Handle interest case
        application, is_new = handle_interest(
            application, vacancy, request.user, resume
        )

        if not is_new and application.status == ApplicationStatus.SUCCESS:
            return Response(
                {"message": "Application already exists and was successful"},
                status=status.HTTP_200_OK,
            )
        return Response(str(application.id), status=status.HTTP_201_CREATED)


# CHECK the existence of Scraped Vacancy


class ScrapedVacancyExistsView(APIView):
    """
    Check if a list of URLs already exists in the database.

    Returns a list of booleans indicating whether each URL already exists.
    """

    permission_classes = [HasAPIKey]
    serializer_class = URLListSerializer

    def post(self, request, *args, **kwargs):
        serializer = URLListSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        urls = serializer.validated_data["urls"]
        existing_urls_set = set(
            ScrapedVacancy.objects.filter(url__in=urls).values_list("url", flat=True)
        )
        exists = [url in existing_urls_set for url in urls]
        return Response({"result": exists})


# POST Launch vacancy processing job


class LaunchVacancyProcessingJob(APIView):

    permission_classes = [IsAdminUser]

    @extend_schema(
        operation_id="Launch Vacancy Processing Job",
        request=None,
        responses={
            204: None,
        },
    )
    def post(self, request, *args, **kwargs):
        process_pending_vacancies_task.delay()

        return Response(status.HTTP_204_NO_CONTENT)


# GET Vacancy stats


class VacancyStatsView(APIView):
    permission_classes = [IsAdminUser]

    @extend_schema(
        responses={
            200: VacancyStatsSerializer,
        }
    )
    def get(self, request, *args, **kwargs):
        scraped_vacancies = {
            f"{status}": ScrapedVacancy.objects.filter(status=status).count()
            for status in Status.values
        }
        scraped_vacancies["total"] = sum(scraped_vacancies.values())
        vacancy_stats = {
            "scraped_vacancies": scraped_vacancies,
            "vacancies": Vacancy.objects.count(),
        }

        return Response(vacancy_stats)


class RateVacancyView(APIView):
    serializer_class = VacancyRatingSerializer

    @extend_schema(
        summary="Rate a vacancy",
        description="Rate a vacancy between -1 and 1.",
        responses={
            204: None,
            400: None,
        },
    )
    def post(self, request: Request, vacancy_id: int) -> Response:
        vacancy = get_object_or_404(Vacancy, id=vacancy_id)
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            VacancyRating.objects.update_or_create(
                user=request.user,
                vacancy=vacancy,
                defaults={"rating": serializer.validated_data["rating"]},
            )

            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SearchJobsView(APIView):
    permission_classes = [IsAdminUser]
    serializer_class = None

    def post(self, request: Request, user_id: str) -> Response:
        try:
            _ = get_object_or_404(User, id=user_id)
            logger.error("SearchJobsView not implemented")
            # TODO : make call to scraper to get vacancies
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Http404:
            return Response(status=status.HTTP_404_NOT_FOUND)


class FindJobsView(APIView):
    serializer_class = VacancySerializer

    @extend_schema(
        operation_id="find_jobs",
        request=inline_serializer(
            name="FindJobs",
            fields={
                "query": serializers.CharField(
                    help_text="Query to search for jobs.",
                    required=False,
                ),
            },
        ),
        responses={
            200: VacancySerializer(many=True),
        },
    )
    def post(self, request: Request, *args, **kwargs):
        search_query = request.data["query"]
        if not search_query or not isinstance(search_query, str):
            return Response(
                {"error": "Search query is required"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        vacancies = async_to_sync(execute_serperdev_search)(search_query)
        if not vacancies:
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(
            self.serializer_class(vacancies, many=True).data, status=status.HTTP_200_OK
        )


class ListPendingScrapingTasksView(ListAPIView):
    queryset = ScrapingTask.objects.filter(status=Status.PENDING)
    serializer_class = ScrapingTaskSerializer

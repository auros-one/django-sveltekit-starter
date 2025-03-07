from django.contrib import admin
from django.contrib.admin import ModelAdmin
from django.shortcuts import redirect
from django.utils.html import format_html

from .models import ScrapedVacancy, Skill, Vacancy
from .tasks import process_pending_vacancies_task


@admin.register(ScrapedVacancy)
class ScrapedVacancyAdmin(ModelAdmin):
    list_display = ("id", "url", "created", "modified", "vacancy_link")
    list_filter = ("created", "modified")
    search_fields = ("url",)
    readonly_fields = ("vacancy_link", "html")
    actions = ["process_selected_scraped_vacancies"]

    @admin.display(description="Vacancy")
    def vacancy_link(self, obj):
        if hasattr(obj, "vacancy"):
            url = f"/api/admin/vacancies/vacancy/{obj.vacancy.id}/change/"
            return format_html('<a href="{}" target="_blank">View Vacancy</a>', url)
        return "None"

    @admin.action(description="Process selected scraped vacancies")
    def process_selected_scraped_vacancies(self, request, queryset):
        # Extract the IDs of the selected ScrapedVacancies
        ids = list(str(id) for id in queryset.values_list("id", flat=True))

        # Call the process_pending_vacancies command with the selected IDs
        process_pending_vacancies_task.delay(ids=ids)

        # Redirect back to the admin page with a success message
        self.message_user(request, "Selected scraped vacancies are being processed.")
        return redirect(request.get_full_path())


@admin.register(Vacancy)
class VacancyAdmin(ModelAdmin):
    list_display = (
        "id",
        "title",
        "published_at",
        "min_salary",
        "max_salary",
        "created",
        "modified",
    )
    list_filter = ("published_at", "created", "modified")
    search_fields = ("title", "description")
    raw_id_fields = (
        "source",
    )  # Using raw_id_fields for better performance with ForeignKey relations
    readonly_fields = ("vacancy_public_link", "published_at")

    @admin.display(description="Company")
    def company_name(self, obj):
        return obj.company.name if obj.company else "No Company"

    @admin.display(description="Public Vacancy")
    def vacancy_public_link(self, obj):
        url = f"/vacancies/{obj.slug}"
        return format_html('<a href="{}">View Public Vacancy</a>', url)


@admin.register(Skill)
class SkillAdmin(ModelAdmin):
    search_fields = ("name",)
    list_display = ("id", "name")

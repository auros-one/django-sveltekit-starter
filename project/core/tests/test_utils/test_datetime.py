from datetime import datetime, timedelta, timezone

import pytest
from rest_framework.exceptions import ValidationError
from rest_framework.request import Request
from rest_framework.test import APIRequestFactory

from project.core.utils.datetime import get_request_datetime_argument


class TestDatetimeArgumentParsing:
    @pytest.fixture
    def factory(self) -> APIRequestFactory:
        return APIRequestFactory()

    @pytest.mark.parametrize(
        "string, expected",
        [
            (
                "2020-01-01T12:24:48Z",
                datetime(2020, 1, 1, 12, 24, 48, tzinfo=timezone.utc),
            ),
            (
                "2020-08-01T12:24:00Z",
                datetime(2020, 8, 1, 12, 24, 0, tzinfo=timezone.utc),
            ),
            (
                "2025-01-18T23:24:00+01:00",
                datetime(2025, 1, 18, 23, 24, 0, tzinfo=timezone(timedelta(hours=1))),
            ),
            (
                "2020-01-01T12:24:00-01:00",
                datetime(2020, 1, 1, 12, 24, 0, tzinfo=timezone(timedelta(hours=-1))),
            ),
        ],
    )
    def test_valid_datetime(self, string, expected, factory: APIRequestFactory):
        request = Request(factory.get("/dummy_url", {"start_time": string}))
        result = get_request_datetime_argument(request, "start_time")
        assert result == expected

    def test_invalid_datetime(self, factory: APIRequestFactory):
        request = Request(factory.get("/dummy_url", {"start_time": "invalid_datetime"}))
        with pytest.raises(ValidationError) as context:
            get_request_datetime_argument(request, "start_time")
        assert context.value.detail == {
            "start_time": [
                "Invalid datetime, expects ISO format. For example: 2020-01-01T00:00:00Z"
            ]
        }

    def test_missing_datetime(self, factory: APIRequestFactory):
        request = Request(factory.get("/dummy_url"))
        with pytest.raises(ValidationError) as context:
            get_request_datetime_argument(request, "start_time")
        assert context.value.detail == {
            "start_time": [
                "Missing 'start_time' parameter. Expects a datetime in ISO format. For example: 2020-01-01T00:00:00Z"
            ]
        }

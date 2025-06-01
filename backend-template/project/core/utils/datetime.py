from datetime import datetime

from rest_framework.exceptions import ValidationError
from rest_framework.request import Request


def get_request_datetime_argument(request: Request, name: str) -> datetime:
    datetime_str = request.query_params.get(name, None)
    if datetime_str is None:
        raise ValidationError(
            {
                name: [
                    f"Missing '{name}' parameter. Expects a datetime in ISO format. For example: 2020-01-01T00:00:00Z"
                ]
            }
        )
    try:
        datetime_str = datetime_str.replace("Z", "+00:00")
        return datetime.fromisoformat(datetime_str)
    except ValueError:
        raise ValidationError(
            {
                name: [
                    "Invalid datetime, expects ISO format. For example: 2020-01-01T00:00:00Z"
                ]
            }
        )

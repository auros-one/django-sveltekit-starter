FROM python:3.11-slim AS builder

WORKDIR /build

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    POETRY_HOME="/opt/poetry" \
    POETRY_VIRTUALENVS_IN_PROJECT=true \
    POETRY_NO_INTERACTION=1

# Install Poetry
RUN pip install --upgrade pip && \
    pip install poetry

RUN apt-get -y update && apt-get -y install --no-install-recommends \
    gcc \
    libc-dev \
    libpq-dev

COPY pyproject.toml poetry.lock* /build/

ARG ENVIRONMENT="production"
RUN if [ "$ENVIRONMENT" = "development" ] ;\
    then poetry install --no-root ;\
    else poetry install --no-root --only main ;\
    fi

# Final runner

FROM python:3.11-slim

WORKDIR /app

# Stops an annoying message when running `shell_plus`.
RUN mkdir -p /root/.config/ptpython && touch /root/.config/ptpython/config.py

RUN apt-get -y update && apt-get -y install --no-install-recommends \
    libpq-dev \
    postgresql-client

COPY --from=builder /build/.venv/ /opt/venv/
RUN find /opt/venv/bin/ -type f -iname "*" -exec sed -i 's@#\!/build/.venv/bin/python@#\!/opt/venv/bin/python@g' {} \;
# Prefer Python from the virtual environment.
ENV PATH="/opt/venv/bin:$PATH"

COPY . .

RUN python manage.py collectstatic --no-input

ENTRYPOINT ["./docker/entrypoint.sh"]
CMD ["python", "-m", "gunicorn"]

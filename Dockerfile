FROM python:3.11-slim AS builder

WORKDIR /build

ENV PIPENV_VENV_IN_PROJECT=1

RUN pip install --user pipenv setuptools wheel

RUN apt-get -y update && apt-get -y install --no-install-recommends \
    gcc \
    libc-dev \
    libpq-dev

COPY Pipfile Pipfile.lock /build/

RUN pip install --user pipenv

ARG ENVIRONMENT="production"
RUN if [ "$ENVIRONMENT" = "development" ] ;\
    then /root/.local/bin/pipenv install --deploy --dev ;\
    else /root/.local/bin/pipenv install --deploy ;\
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

ENTRYPOINT ["python"]
CMD ["-m", "gunicorn"]

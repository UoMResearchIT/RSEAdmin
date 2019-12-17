FROM alpine:latest
#FROM debian:buster

LABEL maintainer="w.furnass@sheffield.ac.uk"
LABEL vendor="University of Sheffield"

SHELL ["/bin/ash", "-eu", "-c"]

ENV \
    LANG=C.UTF-8 \ 
    # python:
    PYTHONFAULTHANDLER=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONHASHSEED=random \
    # pip:
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100 \
    # poetry:
    POETRY_VERSION=1.0.2 \
    # django:
    DJANGO_PROJ_NAME=RSEAdmin \
    # SECRET_KEY=...
    # DJANGO_ALLOWED_HOSTS=host1,host2,host3,...
    # DJANGO_DEFAULT_FROM_EMAIL=mail1,mail2,...
    # DJANGO_SERVER_EMAIL=mail1,mail2,...
    DJANGO_PROJ_ROOT=/app \
    DJANGO_DB_NAME=rseadmin \
    DJANGO_DB_USER=rseadmin \
    #DJANGO_DB_PASSWORD=...
    DJANGO_DB_HOST=localhost \
    DJANGO_DB_PORT=5432 \
    DJANGO_OS_USER=rseadmin \
    # gunicorn: 
    GUNICORN_PORT=8002 \
    GUNICORN_HOST=127.0.0.1

ENV \
    # More django (required as cannot recursively define env vars above)
    DJANGO_STATIC_ROOT="${DJANGO_PROJ_ROOT}/static" \
    DJANGO_SETTINGS_MODULE="${DJANGO_PROJ_NAME}.settings.settings_deployed" \
    DJANGO_OS_HOME="/var/lib/${DJANGO_OS_USER}"

# Copy repo into image
COPY . "${DJANGO_PROJ_ROOT}"
RUN ln -s "${DJANGO_PROJ_ROOT}/docker/django_settings_deployed.py" "${DJANGO_PROJ_ROOT}/${DJANGO_PROJ_NAME}/settings/settings_deployed.py"

# Install OS Python3 package and 
# packages required to build psycopg2 Python pkg
RUN apk add \
    python3 \
    ca-certificates \
    postgresql-dev \
    python3-dev \
    gcc \
    musl-dev

# Download poetry
RUN wget 'https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py' -qP /usr/local/bin/

# Create system user for running gunicorn
RUN addgroup \
        --system \
        "${DJANGO_OS_USER}" && \
    adduser \
        --home "${DJANGO_OS_HOME}" \
        --disabled-password \
        --ingroup "${DJANGO_OS_USER}" \
        --system \
        "${DJANGO_OS_USER}"

USER "${DJANGO_OS_USER}"
WORKDIR "${DJANGO_PROJ_ROOT}"

# Install Poetry and patch so works with Python 3 (yuk)
RUN python3 /usr/local/bin/get-poetry.py --version "${POETRY_VERSION}" --yes && \
    sed -i '1s/python$/python3/' ~/.poetry/bin/poetry
ENV PATH="${DJANGO_OS_HOME}/.poetry/bin:${PATH}"

# Install project's Python dependencies
RUN poetry install --no-dev --no-interaction --no-ansi -E gunicorn -E pgsql
# Install django custom settings for deployment (staging/production)
# Collect Django static files under the Django STATIC_ROOT
RUN ls -l RSEAdmin/settings/settings_deployed.py
RUN poetry run python manage.py collectstatic --noinput --settings="${DJANGO_SETTINGS_MODULE}" && \
# Process Django migrations
RUN poetry run python manage.py migrate --settings="${DJANGO_SETTINGS_MODULE}"

EXPOSE "${GUNICORN_PORT}"
CMD poetry run gunicorn --bind="${GUNICORN_HOST}:${GUNICORN_PORT}" "${DJANGO_SETTINGS_MODULE}"

# Creating a python base with shared environment variables
FROM python:3.11-slim-bullseye AS python-base
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100 \
    POETRY_HOME="/opt/poetry" \
    POETRY_VIRTUALENVS_IN_PROJECT=true \
    POETRY_NO_INTERACTION=1 \
    PYSETUP_PATH="/opt/pysetup" \
    POETRY_VERSION=1.4.2 \
    VENV_PATH="/opt/pysetup/.venv"

ENV PATH="$POETRY_HOME/bin:$VENV_PATH/bin:$PATH"


# builder-base is used to build dependencies
FROM python-base AS builder-base
#RUN printf 'Acquire::http::Proxy "%s";' "$HTTP_PROXY" > /etc/apt/apt.conf
#RUN printf 'Acquire::https::Proxy "%s";' "$HTTPS_PROXY" >> /etc/apt/apt.conf

RUN buildDeps="build-essential" \
    && apt-get update \
    && apt-get install --no-install-recommends -y \
    curl \
    netcat \
    && apt-get install -y --no-install-recommends $buildDeps \
    && rm -rf /var/lib/apt/lists/*

# Install Poetry - respects $POETRY_VERSION & $POETRY_HOME
SHELL ["/bin/bash", "-o", "pipefail", "-c"]
RUN curl -sSL https://install.python-poetry.org | POETRY_HOME=${POETRY_HOME} python3 - --version ${POETRY_VERSION} && \
    chmod a+x /opt/poetry/bin/poetry

# We copy our Python requirements here to cache them
# and install only runtime deps using poetry
WORKDIR $PYSETUP_PATH
COPY ./poetry.lock ./pyproject.toml ./
RUN poetry install --only main


FROM python-base AS development
ENV DEBUG=True

# Copying poetry and venv into image
COPY --from=builder-base $VENV_PATH $VENV_PATH

# Copying in our entrypoint
COPY ./docker/docker-entrypoint.sh /docker-entrypoint.sh
RUN chmod +x /docker-entrypoint.sh

WORKDIR /tb
COPY . .

ENTRYPOINT /docker-entrypoint.sh $0 $@
CMD ["uvicorn", "--host ${SERVER_HOST}", "--port ${SERVER_PORT}", "app.main:app", "--reload"]


FROM python-base AS production
ENV DEBUG=False

# Copying poetry and venv into image
COPY --from=builder-base $VENV_PATH $VENV_PATH

# Copying in our entrypoint
COPY ./docker/docker-entrypoint.sh /docker-entrypoint.sh
RUN chmod +x /docker-entrypoint.sh

WORKDIR /tb
COPY . .

ENTRYPOINT /docker-entrypoint.sh $0 $@
CMD ["gunicorn", "-c app/conf/gunicorn/conf.py", "app.main:app"]

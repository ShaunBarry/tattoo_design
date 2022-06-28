# syntax=docker/dockerfile:1.3

FROM python:3.10 as build-stage

RUN apt-get update
RUN apt-get install -y --no-install-recommends \
    build-essential \
    gcc \
    python3-dev \
    python3-venv \
    libssl-dev \
    libcurl4-openssl-dev \
    libcairo2

ENV PIP_NO_CACHE_DIR=1

RUN python3 -m pip install --upgrade pip setuptools wheel && \
    python3 -m pip install "poetry==1.1.13"

RUN python3 -m venv /venv

ENV VIRTUAL_ENV=/venv
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

WORKDIR /project

COPY ["pyproject.toml", "/project/"]

RUN poetry install --no-interaction --remove-untracked --no-root

FROM python:3.10-slim as final

RUN apt-get update
RUN apt-get upgrade -y && \
    apt-get install --no-install-recommends -y \
    libssl-dev \
    libcurl4-openssl-dev \
    curl

RUN useradd -m appuser
USER appuser

ENV PYTHONUNBUFFERED=1 \
    VIRTUAL_ENV=/venv

ENV PATH="$VIRTUAL_ENV/bin:$PATH"

WORKDIR /project

RUN python3 -m pip install drawSvg

COPY --from=build-stage --chown=appuser $VIRTUAL_ENV $VIRTUAL_ENV
COPY --chown=appuser [".", "/project"]
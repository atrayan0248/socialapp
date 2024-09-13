# Use an official python runtime as the base image
FROM python:3.10.12-buster

# Set the working directory in the container
WORKDIR /opt/project

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV PYTHONPATH .
ENV SOCIALAPP_IN_DOCKER 1

# Install dependencies
RUN set -xe \
    && apt-get update \
    && apt-get install -y --no-install-recommends build-essential \
    && pip install virtualenvwrapper poetry=1.8.3 \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Copy and install python dependencies
COPY ["poetry.lock", "pyproject.toml", "./"]
RUN poetry install --no-root


# Copy project files
COPY ["README.rst", "Makefile", "./"]
COPY socialapp socialapp
COPY local local

# Expose the django server port
EXPOSE 8000

# Set up the entrypoint
COPY scripts/entrypoint.sh /entrypoint.sh
RUN chmod a+x /entrypoint.sh

ENTRYPOINT ["entrypoint.sh"]

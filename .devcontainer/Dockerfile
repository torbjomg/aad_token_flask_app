ARG PYTHON_TAG
FROM python:$PYTHON_TAG

USER root
WORKDIR /stg

RUN apt-get update && apt-get install -y \
    ca-certificates \
    unzip \
    wget \
    curl \
    make \
    git \
    dnsutils \
    && apt-get clean

COPY ./.devcontainer/ca-bundle.crt /usr/local/share/ca-certificates/
RUN update-ca-certificates

# # Urllib likes the first. Request supposedly likes the second. VSCode extensions likes the third
ENV SSL_CERT_FILE /etc/ssl/certs/ca-certificates.crt
ENV REQUESTS_CA_BUNDLE /etc/ssl/certs/ca-certificates.crt
ENV NODE_EXTRA_CA_CERTS /etc/ssl/certs/ca-certificates.crt


# Pre-commit
# npm: to enable node pre-commit hooks behind corporate PKI
RUN apt-get install -y --no-install-recommends npm
RUN pip install pre-commit
ARG PRE_COMMIT_CONFIG_FILE_PATH
COPY $PRE_COMMIT_CONFIG_FILE_PATH ./.pre-commit-config.yaml
RUN git init . && pre-commit install-hooks

ARG REQUIREMENTS_FILE_PATH
COPY $REQUIREMENTS_FILE_PATH ./requirements.txt
RUN pip install -r requirements.txt
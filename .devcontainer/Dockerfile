ARG PYTHON_VERSION=3.12
FROM mcr.microsoft.com/devcontainers/python:${PYTHON_VERSION}

# Install uv via the official installer
ARG UV_VERSION=0.10.9
RUN curl -LsSf https://astral.sh/uv/${UV_VERSION}/install.sh | UV_INSTALL_DIR=/usr/local/bin sh

# Environment variables
ENV DEPSIGHT_ENV=development
ENV PYTHONUNBUFFERED=1

USER vscode
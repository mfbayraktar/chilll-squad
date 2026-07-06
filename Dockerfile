#
# BUILD STAGE
# # # # # # # #
ARG PYTHON_VERSION=3.12
FROM python:${PYTHON_VERSION}-slim AS builder


# Install uv via official installer script
ARG UV_VERSION=0.10.9
RUN apt-get update \
    && apt-get install -y --no-install-recommends curl \
    && rm -rf /var/lib/apt/lists/* \
    && curl -LsSf https://astral.sh/uv/${UV_VERSION}/install.sh | UV_INSTALL_DIR=/usr/local/bin sh

WORKDIR /depsight

# depsight is installed automatically from PyPI via the dependency in pyproject.toml.

COPY pyproject.toml uv.lock ./

RUN uv sync --frozen --no-install-project

# Copy source code
COPY src/ src/

# Install the project (reuses cached dependency layer above)
RUN uv sync --frozen

#
# FINAL STAGE
# # # # # # # #
ARG PYTHON_VERSION=3.12
FROM python:${PYTHON_VERSION}-slim

WORKDIR /depsight

# Create non-root user
ARG USER_ID=1000
ARG USER_NAME=depsight
RUN groupadd -g ${USER_ID} ${USER_NAME} && \
    useradd -u ${USER_ID} -g ${USER_NAME} -m -s /bin/bash ${USER_NAME}

# Copy uv binaries from the builder stage
COPY --from=builder /usr/local/bin/uv /usr/local/bin/uvx /usr/local/bin/

# Copy the virtual environment from the builder stage
COPY --from=builder /depsight/.venv /depsight/.venv

# Copy the plugin source so depsight can load it via the entry point
COPY --from=builder /depsight/src /depsight/src

# Prepare runtime directories and fix ownership
RUN mkdir -p /home/${USER_NAME}/.depsight/logs /home/${USER_NAME}/.depsight/data && \
    chown -R ${USER_NAME}:${USER_NAME} /depsight /home/${USER_NAME}

USER ${USER_NAME}

ENV PATH="/depsight/.venv/bin:$PATH"
ENV PYTHONPATH="/depsight/src"
ENV PYTHONUNBUFFERED=1

ENTRYPOINT ["depsight"]
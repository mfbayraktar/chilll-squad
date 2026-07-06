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

# TODO: Copy pyproject.toml and uv.lock into the container.
#       Copying them before the source code allows Docker to cache the
#       dependency-install layer — dependencies are only re-installed when
#       these files change, not on every code edit.
#       Command:
#         COPY pyproject.toml uv.lock ./

# TODO: Install only the project's dependencies (not the project itself).
#       Use 'uv sync' with two flags:
#         --frozen             : use the exact versions from uv.lock without updating it
#         --no-install-project : skip installing your own package (just its dependencies)
#       This creates a cached layer so dependency installation is skipped on rebuilds
#       unless pyproject.toml or uv.lock changes.
#       Command:
#         RUN uv sync --frozen --no-install-project

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
# TODO: Create a non-root group and user for running the container securely.
#       Use 'groupadd' to create a group with the given GID, then 'useradd' to
#       create a user with the given UID, assigned to that group, with a home
#       directory (-m) and a login shell (-s /bin/bash).
#       Command:
#         RUN groupadd -g ${USER_ID} ${USER_NAME} && \
#             useradd -u ${USER_ID} -g ${USER_NAME} -m -s /bin/bash ${USER_NAME}

# Copy uv binaries from the builder stage
COPY --from=builder /usr/local/bin/uv /usr/local/bin/uvx /usr/local/bin/

# TODO: Copy the virtual environment from the builder stage.
#       Use COPY with --from=builder to bring the .venv directory to the same
#       path in the final image (/depsight/.venv).
#       Command:
#         COPY --from=builder /depsight/.venv /depsight/.venv

# Copy the plugin source so depsight can load it via the entry point
COPY --from=builder /depsight/src /depsight/src

# TODO: Prepare runtime directories and fix ownership.
#       Create the log and data directories under the user's home, then
#       recursively change ownership of the workdir and home to the non-root user.
#       Command:
#         RUN mkdir -p /home/${USER_NAME}/.depsight/logs /home/${USER_NAME}/.depsight/data && \
#             chown -R ${USER_NAME}:${USER_NAME} /depsight /home/${USER_NAME}

# TODO: Switch to the non-root user using the Docker USER syntax

ENV PATH="/depsight/.venv/bin:$PATH"
ENV PYTHONPATH="/depsight/src"
ENV PYTHONUNBUFFERED=1

# TODO: Define the container's entrypoint to launch the depsight CLI.
#       Use the Docker ENTRYPOINT[] syntax to specify 'depsight'
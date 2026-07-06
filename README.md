# Depsight Third-Party Plugin

## About

This repository is a **template** for building third-party plugins for [Depsight](https://github.com/ValentinTwin1206/depsight-dependency-manager), a Python-based dependency management CLI. It provides all the scaffolding needed to develop, test, package, and ship a plugin as a Python wheel — without having to set up the toolchain from scratch.

The project is designed as a **hands-on DevOps learning exercise**. Rather than providing a fully working pipeline out of the box, it intentionally leaves key steps as guided TODO items, challenging you to wire up the CI/CD workflow yourself. Along the way you will practice common DevOps patterns found in real Python projects: containerised development environments with Dev Containers, linting and type checking with Ruff and Mypy, automated testing with pytest, wheel packaging with uv, and multi-job GitHub Actions pipelines that build, publish, and release artefacts.

## Usage

Please read the [Depsight User Instructions](https://valentintwin1206.github.io/depsight-third-party-plugin/).

## Development

### System Requirements

- **IDE with DevContainer support** — either of the following:
    - [Visual Studio Code](https://code.visualstudio.com/) with the [Dev Containers](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-containers) extension
    - [JetBrains Gateway](https://www.jetbrains.com/remote-development/gateway/) (supports Dev Containers via the Remote Development plugin)
- **Container manager** — any one of the following:
    - [Docker Desktop](https://www.docker.com/products/docker-desktop/) (macOS, Windows, Linux) (**RECOMMENDED**)
    - [Docker Engine](https://docs.docker.com/engine/install/) (Linux)
    - [Podman](https://podman.io/) with the Podman Desktop or CLI

### Setup Locally

- Open Visual Studio Code at the project root directory
- When prompted, click **Reopen in Container** (or use Command Palette: `Dev Containers: Reopen in Container`)

  <img src="./images/reopen_in_container.png" alt="Logo" width="400"/>

- Wait for the containers to build and start
- Once ready, you'll have a fully configured development environment with all dependencies installed
- Open a terminal inside the DevContainer and run `depsight --help`

### Run Tests

- Open a terminal inside the DevContainer
- Activate the virtual environment:

  ```bash
  source .venv/bin/activate
  ```

- Run all tests:

  ```bash
  pytest tests/ -v
  ```

### Lint & Type Check

- Run the Ruff linter:

  ```bash
  ruff check src/ tests/
  ```

- Run the Mypy type checker:

  ```bash
  mypy src/
  ```

## Release

#### Pre-release

- Navigate to your repository on GitHub and click the **Actions** tab
- Select the **Manual Dispatch** workflow from the left sidebar
- Click **Run workflow**
- Set `plugin_version` to the version string to verify against `pyproject.toml` (e.g. `1.2.3`) — this field is **required**
- Optionally set `uv_version` (defaults to `0.11.1`) or check **Push the container image to Docker Hub**
- The plugin currently pins `depsight==1.3.0` in `pyproject.toml`
- Click **Run workflow**

#### Release

- Bump the `version` field in `pyproject.toml` to the desired version (e.g. `1.2.3`)
- Commit and push the change to `main`
- Navigate to your repository on GitHub and click **Releases** → **Draft a new release**
- Create a new tag matching the version in `pyproject.toml` exactly (e.g. `1.2.3`)
- Click **Publish release**
- The **Release** workflow triggers automatically, runs the full CI pipeline, and pushes the Docker image to Docker Hub

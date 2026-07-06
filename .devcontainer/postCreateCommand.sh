#!/usr/bin/env bash
set -euo pipefail

# Ensure depsight is always resolved from PyPI at the latest version
uv lock --upgrade-package depsight

# Install all dependencies
uv sync --all-groups

# Clone the JS fullstack learning course repository
# git clone https://github.com/ValentinTwin1206/fancy-fileserver.git \
#     /workspaces/fancy-fileserver
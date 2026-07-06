from __future__ import annotations

from pathlib import Path

# third-party imports
from depsight.core.plugins.base import BasePlugin
from depsight.core.plugins.dependency import Dependency

# TODO: RENAME "MyPlugin" TO "NpmPlugin"
class MyPlugin(BasePlugin):
    """Example third-party plugin for depsight."""

    def __init__(self) -> None:
        self.dependencies: list[Dependency] = []

    @property
    def name(self) -> str:
        # TODO: Replace the name to "npm"
        return "myplugin"

    @property
    def dependency_files(self) -> tuple[str, ...]:
        # TODO: Add "package-lock.json"to the tuple
        return ("",)

    @property
    def default_file(self) -> str:
        # TODO: Return "package-lock.json" once dependency_files is updated
        return self.dependency_files[0]

    def collect(self, project_dir: str | Path, _file: str | None = None) -> None:
        """Return two fake dependencies for testing."""
        # TODO: Parse dependencies from a 'package-lock.json' file.
        # Implementation guidance:
        # - Locate and load the 'package-lock.json' from the given project directory.
        # - Read the JSON content and detect the lockfile format version.

        # For npm v2/v3 (preferred approach):
        # - Use the top-level "packages" field.
        # - Iterate over all entries in "packages".
        # - Skip the root entry identified by an empty string key ("").
        # - Only consider entries under "node_modules/...".
        # - Extract the dependency name from the path:
        #     e.g. "node_modules/lodash" → "lodash"
        #          "node_modules/@scope/pkg" → "@scope/pkg"
        # - Read the resolved version from the "version" field.
        # - Create a Dependency(name, version, tool_name=self.name) for each entry.

        # For npm v1 (fallback):
        # - Use the nested "dependencies" field.
        # - Recursively traverse all dependency objects.
        # - Extract "name" (key) and "version" from each node.

        # General rules:
        # - Do NOT resolve versions manually; always use the locked version.
        # - Skip entries without a valid "version".
        # - Ensure each dependency is added only once (avoid duplicates).
        # - Store results in self.dependencies.

        self.dependencies = [
            Dependency(name="foo", version="1.0.0", tool_name=self.name),
            Dependency(name="bar", version="2.0.0", tool_name=self.name),
        ]

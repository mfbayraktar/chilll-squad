from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from depsight.core.plugins.base import BasePlugin
from depsight.core.plugins.dependency import Dependency


class NpmPlugin(BasePlugin):
    """Depsight plugin that scans npm projects via ``package-lock.json``."""

    def __init__(self) -> None:
        self.dependencies: list[Dependency] = []

    @property
    def name(self) -> str:
        return "npm"

    @property
    def dependency_files(self) -> tuple[str, ...]:
        return ("package-lock.json",)

    def collect(self, path: str | Path, file: str | None = None) -> None:
        lockfile_name = file or self.default_file
        lockfile = Path(path) / lockfile_name

        with lockfile.open(encoding="utf-8") as fh:
            data = json.load(fh)

        file_str = str(lockfile.resolve())
        collected: dict[tuple[str, str], Dependency] = {}

        packages = data.get("packages")
        if isinstance(packages, dict):
            self._collect_v2(packages, file_str, collected)
        else:
            self._collect_v1(data.get("dependencies") or {}, file_str, collected)

        self.dependencies = list(collected.values())

    def _collect_v2(
        self,
        packages: dict[str, dict[str, Any]],
        file_str: str,
        collected: dict[tuple[str, str], Dependency],
    ) -> None:
        root = packages.get("", {}) or {}
        direct_prod = set((root.get("dependencies") or {}).keys())
        direct_dev = set((root.get("devDependencies") or {}).keys())
        direct_names = direct_prod | direct_dev
        constraints: dict[str, str] = {}
        constraints.update(root.get("dependencies") or {})
        constraints.update(root.get("devDependencies") or {})

        for key, entry in packages.items():
            if not key or not key.startswith("node_modules/"):
                continue
            # rpartition handles nested "node_modules/foo/node_modules/bar"
            _, _, dep_name = key.rpartition("node_modules/")
            if not dep_name:
                continue
            version = entry.get("version")
            if not version:
                continue
            is_dev = bool(entry.get("dev")) or dep_name in direct_dev
            dep = Dependency(
                name=dep_name,
                version=version,
                constraint=constraints.get(dep_name),
                tool_name=self.name,
                registry=entry.get("resolved"),
                file=file_str,
                category="dev" if is_dev else "prod",
                is_transitive=dep_name not in direct_names,
            )
            collected.setdefault((dep_name, version), dep)

    def _collect_v1(
        self,
        tree: dict[str, dict[str, Any]],
        file_str: str,
        collected: dict[tuple[str, str], Dependency],
        transitive: bool = False,
    ) -> None:
        for dep_name, entry in tree.items():
            version = entry.get("version")
            if version:
                collected.setdefault(
                    (dep_name, version),
                    Dependency(
                        name=dep_name,
                        version=version,
                        tool_name=self.name,
                        registry=entry.get("resolved"),
                        file=file_str,
                        category="dev" if entry.get("dev") else "prod",
                        is_transitive=transitive,
                    ),
                )
            children = entry.get("dependencies") or {}
            if children:
                self._collect_v1(children, file_str, collected, transitive=True)

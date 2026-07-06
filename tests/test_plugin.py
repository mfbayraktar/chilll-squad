from __future__ import annotations

import csv
from pathlib import Path

# third-party imports
from depsight.core.plugins.base import BasePlugin

from npm.npm import NpmPlugin

FIXTURES = Path(__file__).parent / "fixtures"


class TestCollect:
    """Verify collect() populates dependencies correctly."""

    def test_plugin_implements_base_plugin_contract(self):
        plugin = NpmPlugin()

        assert isinstance(plugin, BasePlugin)
        assert isinstance(plugin.default_file, str)
        assert plugin.default_file.strip()
        assert Path(plugin.default_file).name == plugin.default_file
        assert plugin.default_file not in {".", ".."}
        assert plugin.default_file in plugin.dependency_files

        assert plugin.name == "npm"
        assert plugin.default_file == "package-lock.json"
        assert "package-lock.json" in plugin.dependency_files

    def test_collect_dependency_details(self):
        plugin = NpmPlugin()
        plugin.collect(FIXTURES, file=plugin.default_file)

        by_name = {dep.name: dep for dep in plugin.dependencies}
        assert set(by_name) == {"lodash", "mocha", "ms"}

        lodash = by_name["lodash"]
        assert (lodash.version, lodash.tool_name) == ("4.17.21", "npm")
        assert lodash.category == "prod"
        assert lodash.is_transitive is False
        assert lodash.registry == "https://registry.npmjs.org/lodash/-/lodash-4.17.21.tgz"

        mocha = by_name["mocha"]
        assert (mocha.version, mocha.tool_name) == ("10.2.0", "npm")
        assert mocha.category == "dev"
        assert mocha.is_transitive is False

        ms = by_name["ms"]
        assert (ms.version, ms.tool_name) == ("2.1.3", "npm")
        assert ms.category == "dev"
        assert ms.is_transitive is True


class TestExport:
    """Verify export() writes a valid CSV."""

    def test_export_csv(self, tmp_path: Path):
        plugin = NpmPlugin()
        plugin.collect(FIXTURES, file=plugin.default_file)
        csv_path = plugin.export(FIXTURES, tmp_path)
        assert csv_path.exists()
        assert csv_path.name == "npm_fixtures.csv"

        with csv_path.open(encoding="utf-8") as fh:
            rows = list(csv.DictReader(fh))

        assert len(rows) == 3
        assert {row["name"] for row in rows} == {"lodash", "mocha", "ms"}


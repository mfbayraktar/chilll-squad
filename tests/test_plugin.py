from __future__ import annotations

import csv
from pathlib import Path

# third-party imports
from depsight.core.plugins.base import BasePlugin

# TODO: Once you rename the class in `src/myplugin/myplugin.py` from
#       `MyPlugin` to `NpmPlugin`, update this import to match:
#           from myplugin.myplugin import NpmPlugin
from myplugin.myplugin import MyPlugin


class TestCollect:
    """Verify collect() populates dependencies correctly."""

    def test_plugin_implements_base_plugin_contract(self):
        # TODO: Replace `MyPlugin()` with `NpmPlugin()` after the rename.
        plugin = MyPlugin()

        assert isinstance(plugin, BasePlugin)
        assert isinstance(plugin.default_file, str)
        assert plugin.default_file.strip()
        assert Path(plugin.default_file).name == plugin.default_file
        assert plugin.default_file not in {".", ".."}
        assert plugin.default_file in plugin.dependency_files

        # TODO: Add assertions that pin down the new expected values once
        #       you have updated the plugin's properties, for example:
        #           assert plugin.name == "npm"
        #           assert plugin.default_file == "package-lock.json"
        #           assert "package-lock.json" in plugin.dependency_files

    def test_collect_dependency_details(self):
        # TODO: Replace `MyPlugin()` with `NpmPlugin()` after the rename.
        plugin = MyPlugin()

        # TODO: The current call points at a non-existent directory and relies
        #       on the stub implementation returning the hard-coded "foo"/"bar"
        #       dependencies. Once you implement real parsing of
        #       `package-lock.json`:
        #         1. Add a small fixture file under `tests/fixtures/` (e.g.
        #            `tests/fixtures/package-lock.json`) with a couple of
        #            dependencies and pinned versions you control.
        #         2. Point `collect()` at the directory containing that
        #            fixture, e.g.:
        #                plugin.collect(
        #                    Path(__file__).parent / "fixtures",
        #                    file="package-lock.json",
        #                )
        plugin.collect("/nonexistent", file=plugin.default_file)

        # TODO: Rename `foo` / `bar` to variable names that match the
        #       dependencies declared in your fixture (e.g. `lodash`,
        #       `express`) and update the expected tuples below to match
        #       the real names, versions, and the new tool name ("npm").
        foo, bar = plugin.dependencies
        assert (foo.name, foo.version, foo.tool_name) == ("foo", "1.0.0", "myplugin")
        assert (bar.name, bar.version, bar.tool_name) == ("bar", "2.0.0", "myplugin")


class TestExport:
    """Verify export() writes a valid CSV."""

    def test_export_csv(self, tmp_path: Path):
        # TODO: Replace `MyPlugin()` with `NpmPlugin()` after the rename.
        plugin = MyPlugin()

        # TODO: Same as in `test_collect_dependency_details` — once parsing is
        #       implemented, point `collect()` at the directory containing
        #       your `package-lock.json` fixture instead of "/some/project".
        plugin.collect("/some/project", file=plugin.default_file)
        csv_path = plugin.export("/some/project", tmp_path)
        assert csv_path.exists()

        # TODO: The exported CSV filename is derived from the plugin's `name`
        #       property. After changing the plugin name to "npm", update the
        #       expected filename here, e.g.:
        #           assert csv_path.name == "npm_project.csv"
        assert csv_path.name == "myplugin_project.csv"

        with csv_path.open(encoding="utf-8") as fh:
            rows = list(csv.DictReader(fh))

        # TODO: Update the expected row count and names so they match the
        #       dependencies declared in your `package-lock.json` fixture.
        assert len(rows) == 2
        assert rows[0]["name"] == "foo"
        assert rows[1]["name"] == "bar"

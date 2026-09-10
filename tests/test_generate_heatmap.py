import importlib.util
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory


MODULE_PATH = Path(__file__).parents[1] / "scripts" / "generate_heatmap.py"
SPEC = importlib.util.spec_from_file_location("generate_heatmap", MODULE_PATH)
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


def calendar_fixture():
    return {
        "totalContributions": 943,
        "weeks": [
            {
                "contributionDays": [
                    {
                        "date": f"2025-01-{day:02d}",
                        "contributionCount": day,
                        "contributionLevel": "FOURTH_QUARTILE" if day else "NONE",
                    }
                    for day in range(1, 8)
                ]
            }
            for _ in range(53)
        ],
    }


class HeatmapGeneratorTests(unittest.TestCase):
    def test_render_contains_live_total_dated_tooltips_and_animation(self):
        svg = MODULE.render(calendar_fixture(), "sanskriti49")
        self.assertIn("943 PTS", svg)
        self.assertIn("contribution on 2025-01-01", svg)
        self.assertIn("@keyframes scan", svg)
        self.assertIn("animateTransform", svg)

    def test_render_escapes_login(self):
        svg = MODULE.render(calendar_fixture(), "<profile>")
        self.assertIn("&lt;profile&gt; contribution heatmap", svg)

    def test_cache_buster_updates_existing_readme_reference(self):
        with TemporaryDirectory() as directory:
            readme = Path(directory) / "README.md"
            readme.write_text('<img src="./assets/contribution-heatmap.svg">', encoding="utf-8")
            MODULE.update_readme_cache_buster(readme, "20260910")
            self.assertIn("contribution-heatmap.svg?v=20260910", readme.read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()

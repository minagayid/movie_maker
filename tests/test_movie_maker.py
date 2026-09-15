import json
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parents[1] / "src"))

from movie_maker.cli import main
from movie_maker.models import ProjectSpec, SourceMaterial
from movie_maker.pipeline import MovieMaker
from movie_maker.rights import RightsError
from movie_maker.validation import validate_package_dict


class MovieMakerTests(unittest.TestCase):
    def setUp(self):
        self.source = SourceMaterial(
            title="The Lantern",
            author="Demo Author",
            text="A traveler finds a lantern.\n\nThe lantern reveals a hidden path.\n\nThe traveler chooses to return home.",
            rights_status="user_owned",
            rights_notes="Test fixture created for this repository.",
        )
        self.spec = ProjectSpec("The Lantern", self.source, target_runtime_minutes=12)

    def test_end_to_end_package_is_complete(self):
        package = MovieMaker().generate(self.spec)
        data = package.to_dict()
        self.assertEqual(len(package.scenes), 3)
        self.assertEqual(sum(scene.duration_seconds for scene in package.scenes), 12 * 60)
        self.assertEqual(len(package.roles), 14)
        self.assertEqual(validate_package_dict(data), [])

    def test_generation_is_deterministic(self):
        first = MovieMaker().generate(self.spec).to_dict()
        second = MovieMaker().generate(self.spec).to_dict()
        self.assertEqual(first, second)

    def test_unknown_rights_fail_closed(self):
        blocked = ProjectSpec(
            "Uncleared",
            SourceMaterial("Uncleared", "Unknown", "Text", "unknown"),
            target_runtime_minutes=10,
        )
        with self.assertRaises(RightsError):
            MovieMaker().generate(blocked)

    def test_validator_catches_a_missing_department_item(self):
        package = MovieMaker().generate(self.spec).to_dict()
        package["manifests"]["audio"]["items"].pop()
        errors = validate_package_dict(package)
        self.assertTrue(any("audio must contain exactly one" in error for error in errors))

    def test_validator_reports_malformed_nested_json_without_raising(self):
        self.assertEqual(validate_package_dict([]), ["package must be an object"])
        package = MovieMaker().generate(self.spec).to_dict()
        package["manifests"]["audio"] = None
        package["manifests"]["edit"]["sequence"] = [None, {"scene_id": [], "shot_ids": None}]
        package["manifests"]["shots"]["items"] = [None, {"shot_id": [], "scene_id": {}, "duration_seconds": True}]
        errors = validate_package_dict(package)
        self.assertTrue(any("audio must be an object" in error for error in errors))
        self.assertTrue(any("edit item 0 must be an object" in error for error in errors))
        self.assertTrue(any("shot item 0 must be an object" in error for error in errors))
        self.assertTrue(any("positive integer duration" in error for error in errors))

    def test_cli_writes_and_validates_artifacts(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            input_path = root / "story.txt"
            output_path = root / "generated"
            input_path.write_text(self.source.text, encoding="utf-8")
            self.assertEqual(
                main(
                    [
                        "generate",
                        "--input",
                        str(input_path),
                        "--output",
                        str(output_path),
                        "--title",
                        "The Lantern",
                        "--author",
                        "Demo Author",
                        "--rights-status",
                        "user_owned",
                        "--rights-notes",
                        "fixture",
                        "--runtime",
                        "12",
                    ]
                ),
                0,
            )
            project_path = output_path / "project.json"
            self.assertTrue(project_path.exists())
            self.assertEqual(main(["validate", "--project", str(project_path)]), 0)
            self.assertIn("voice_over", json.loads(project_path.read_text(encoding="utf-8"))["manifests"])

    def test_cli_rejects_uncleared_source_without_traceback(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            input_path = root / "story.txt"
            input_path.write_text(self.source.text, encoding="utf-8")
            self.assertEqual(
                main(
                    [
                        "generate",
                        "--input",
                        str(input_path),
                        "--output",
                        str(root / "blocked"),
                        "--title",
                        "Blocked",
                        "--author",
                        "Demo Author",
                        "--rights-status",
                        "unknown",
                        "--runtime",
                        "12",
                    ]
                ),
                2,
            )


if __name__ == "__main__":
    unittest.main()

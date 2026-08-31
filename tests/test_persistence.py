import importlib
import os
import sys
import tempfile
from pathlib import Path
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))


class PersistenceTests(unittest.TestCase):
    def test_activities_persist_across_reload(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            db_path = Path(temp_dir) / "activities.db"
            os.environ["ACTIVITIES_DB_PATH"] = str(db_path)

            import app as app_module
            importlib.reload(app_module)

            app_module.activities["Test Activity"] = {
                "description": "A test activity",
                "schedule": "Mondays, 4:00 PM",
                "max_participants": 5,
                "participants": ["student@example.edu"],
            }
            app_module.save_activities()

            importlib.reload(app_module)
            self.assertIn("Test Activity", app_module.activities)
            self.assertEqual(app_module.activities["Test Activity"]["participants"], ["student@example.edu"])


if __name__ == "__main__":
    unittest.main()

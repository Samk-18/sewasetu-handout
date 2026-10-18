
import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "app" / "scripts" / "deemed_approval.py"


class DeemedApprovalConfigTest(unittest.TestCase):
    def test_scheduler_uses_existing_configuration_file(self):
        source = SCRIPT.read_text(encoding="utf-8")
        match = re.search(r'CONFIG_PATH\s*=\s*os\.path\.join\(\s*BASE_DIR\s*,\s*"config"\s*,\s*"([^"]+)"\s*\)', source)

        self.assertIsNotNone(match, "Could not locate CONFIG_PATH in the script")
        config_name = match.group(1)
        self.assertTrue(
            (ROOT / "app" / "config" / config_name).is_file(),
            f"Scheduler configuration file does not exist: {config_name}",
        )


if __name__ == "__main__":
    unittest.main()

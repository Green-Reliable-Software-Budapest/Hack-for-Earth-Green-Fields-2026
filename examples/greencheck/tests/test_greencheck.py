import importlib.util
import sys
import unittest
from pathlib import Path


HERE = Path(__file__).resolve().parents[1]
MODULE_PATH = HERE / "greencheck.py"

spec = importlib.util.spec_from_file_location("greencheck", MODULE_PATH)
greencheck = importlib.util.module_from_spec(spec)
sys.modules["greencheck"] = greencheck
assert spec.loader is not None
spec.loader.exec_module(greencheck)


class GreenCheckTests(unittest.TestCase):
    def test_percent_change(self):
        self.assertEqual(greencheck.percent_change(100, 80), -20)
        self.assertEqual(greencheck.percent_change(100, 120), 20)

    def test_percent_change_zero_baseline(self):
        self.assertEqual(greencheck.percent_change(0, 10), 0)

    def test_examples_return_same_result(self):
        baseline = greencheck.load_run_function(
            HERE / "examples" / "version_a.py",
            "test_baseline",
        )
        candidate = greencheck.load_run_function(
            HERE / "examples" / "version_b.py",
            "test_candidate",
        )
        self.assertEqual(baseline(), candidate())


if __name__ == "__main__":
    unittest.main()

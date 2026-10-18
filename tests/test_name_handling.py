import ast
import unittest
from pathlib import Path


class NameHandlingTest(unittest.TestCase):
    def test_sanitize_preserves_indian_language_characters(self):
        source = Path("app/app.py").read_text(encoding="utf-8")
        tree = ast.parse(source)

        sanitize = next(
            node for node in tree.body
            if isinstance(node, ast.FunctionDef)
            and node.name == "sanitize"
        )

        function_source = ast.get_source_segment(source, sanitize)
        self.assertIn("value[:maxlen]", function_source)
        self.assertNotIn('encode("utf-8")[:maxlen]', function_source)


if __name__ == "__main__":
    unittest.main()

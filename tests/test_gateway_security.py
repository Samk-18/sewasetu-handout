import ast
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
APP_FILE = ROOT / "app" / "app.py"


class GatewaySecurityTest(unittest.TestCase):
    def test_public_app_does_not_expose_gateway_proxy(self):
        source = APP_FILE.read_text(encoding="utf-8")
        tree = ast.parse(source)

        exposed_routes = []
        for node in ast.walk(tree):
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                for decorator in node.decorator_list:
                    if not isinstance(decorator, ast.Call):
                        continue
                    if not isinstance(decorator.func, ast.Attribute):
                        continue
                    if decorator.func.attr != "route":
                        continue
                    if decorator.args and isinstance(decorator.args[0], ast.Constant):
                        route = decorator.args[0].value
                        if isinstance(route, str) and route.startswith("/__gateway"):
                            exposed_routes.append(route)

        self.assertEqual(
            exposed_routes,
            [],
            f"Public gateway proxy routes still exist: {exposed_routes}",
        )


if __name__ == "__main__":
    unittest.main()
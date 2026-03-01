import unittest

from explore.app import app


class TestRouteContract(unittest.TestCase):
    def test_auth_route_shape(self) -> None:
        route_pairs = {
            (method, route.path)
            for route in app.router.routes
            if hasattr(route, "methods")
            for method in route.methods
        }

        self.assertIn(("POST", "/auth/login"), route_pairs)
        self.assertIn(("POST", "/auth/logout"), route_pairs)
        self.assertNotIn(("POST", "/auth/redis/login"), route_pairs)
        self.assertNotIn(("POST", "/auth/redis/logout"), route_pairs)


if __name__ == "__main__":
    unittest.main()

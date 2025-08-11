from django.conf import settings
from django.test import TestCase
from django.urls import reverse
from debug_toolbar import APP_NAME


from django_plugin_debug_toolbar import _inject_middleware


class TestDjangoPluginDebugToolbar(TestCase):
    def test_simple_view_works(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, b"Hello world")

    def test_installed_apps_injected(self):
        self.assertIn("debug_toolbar", settings.INSTALLED_APPS)

    def test_internal_ips_injected(self):
        self.assertIn("127.0.0.1", settings.INTERNAL_IPS)

    def test_toolbar_middleware_injected(self):
        self.assertEqual(
            settings.MIDDLEWARE,
            [
                "django.middleware.locale.LocaleMiddleware",
                "django.middleware.gzip.GZipMiddleware",
                "debug_toolbar.middleware.DebugToolbarMiddleware",
                "django.middleware.security.SecurityMiddleware",
            ],
        )

    def test_debug_toolbar_panel_page_served(self):
        path = reverse(f"{APP_NAME}:render_panel")
        response = self.client.get(f"{path}?request_id=1&panel_id=SettingsPanel")
        self.assertEqual(response.status_code, 200)


class TestToolbarMiddlewareInjection(TestCase):
    def test_inject_middleware(self):
        test_cases = [
            {
                "description": "No middleware",
                "initial_middleware": [],
                "expected_middleware": [
                    "debug_toolbar.middleware.DebugToolbarMiddleware"
                ],
            },
            {
                "description": "Unknown middleware",
                "initial_middleware": ["a", "b"],
                "expected_middleware": [
                    "debug_toolbar.middleware.DebugToolbarMiddleware",
                    "a",
                    "b",
                ],
            },
            {
                "description": "Must go after GZipMiddleware",
                "initial_middleware": ["django.middleware.gzip.GZipMiddleware"],
                "expected_middleware": [
                    "django.middleware.gzip.GZipMiddleware",
                    "debug_toolbar.middleware.DebugToolbarMiddleware",
                ],
            },
            {
                "description": "Must go after GZipMiddleware even if it's preceeded by unknown middleware",
                "initial_middleware": ["a", "django.middleware.gzip.GZipMiddleware"],
                "expected_middleware": [
                    "a",
                    "django.middleware.gzip.GZipMiddleware",
                    "debug_toolbar.middleware.DebugToolbarMiddleware",
                ],
            },
            {
                "description": "Must go after GZipMiddleware but before following unknown middleware",
                "initial_middleware": [
                    "a",
                    "django.middleware.gzip.GZipMiddleware",
                    "b",
                ],
                "expected_middleware": [
                    "a",
                    "django.middleware.gzip.GZipMiddleware",
                    "debug_toolbar.middleware.DebugToolbarMiddleware",
                    "b",
                ],
            },
            {
                "description": "Must go after the last instance of the known special middlewares",
                "initial_middleware": [
                    "a",
                    "django.middleware.gzip.GZipMiddleware",
                    "b",
                    "x_forwarded_for.middleware.XForwardedForMiddleware",
                    "d",
                ],
                "expected_middleware": [
                    "a",
                    "django.middleware.gzip.GZipMiddleware",
                    "b",
                    "x_forwarded_for.middleware.XForwardedForMiddleware",
                    "debug_toolbar.middleware.DebugToolbarMiddleware",
                    "d",
                ],
            },
            {
                "description": "Must go after XForwardedForMiddleware",
                "initial_middleware": [
                    "a",
                    "x_forwarded_for.middleware.XForwardedForMiddleware",
                    "b",
                    "django.middleware.gzip.GZipMiddleware",
                    "xff.middleware.XForwardedForMiddleware",
                    "d",
                ],
                "expected_middleware": [
                    "a",
                    "x_forwarded_for.middleware.XForwardedForMiddleware",
                    "b",
                    "django.middleware.gzip.GZipMiddleware",
                    "xff.middleware.XForwardedForMiddleware",
                    "debug_toolbar.middleware.DebugToolbarMiddleware",
                    "d",
                ],
            },
        ]

        for test_case in test_cases:
            with self.subTest(test_case=test_case):
                initial_middleware = test_case["initial_middleware"]
                expected_middleware = test_case["expected_middleware"]
                self.assertEqual(
                    _inject_middleware(initial_middleware), expected_middleware
                )

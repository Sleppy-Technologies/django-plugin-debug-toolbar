import djp


@djp.hookimpl
def installed_apps():
    return ["debug_toolbar"]


@djp.hookimpl
def urlpatterns():
    from debug_toolbar.toolbar import debug_toolbar_urls
    from debug_toolbar.settings import get_config

    if get_config()["IS_RUNNING_TESTS"]:
        # Django sets DEBUG to False when testing, but we need it to be True
        # so the debug toolbar takes effect.
        from django.conf import settings

        settings.DEBUG = True

    return debug_toolbar_urls()


@djp.hookimpl
def settings(current_settings: dict):
    # "First, ensure that 'django.contrib.staticfiles' is in your
    # INSTALLED_APPS setting, and configured properly"
    installed_apps: list = current_settings.setdefault("INSTALLED_APPS", [])
    if "django.contrib.staticfiles" not in installed_apps:
        installed_apps.append("django.contrib.staticfiles")

    current_settings.setdefault("STATIC_URL", "static/")

    # "Second, ensure that your TEMPLATES setting contains a DjangoTemplates
    # backend whose APP_DIRS options is set to True"
    templates: list[dict] = current_settings.setdefault("TEMPLATES", [])
    django_templates = next(
        (
            template
            for template in templates
            if "DjangoTemplates" in template.get("BACKEND", "")
        ),
        None,
    )
    if django_templates is None:
        raise ValueError(
            "DjangoTemplates backend not found in TEMPLATES setting. "
            "Please ensure it is configured correctly."
        )
    django_templates["APP_DIRS"] = True

    # "The Debug Toolbar is shown only if your IP address is listed in
    # Django’s INTERNAL_IPS setting. This means that for local development,
    # you must add "127.0.0.1" to INTERNAL_IPS."
    internal_ips = current_settings.setdefault("INTERNAL_IPS", [])
    if "127.0.0.1" not in internal_ips:
        internal_ips.append("127.0.0.1")

    # "The Debug Toolbar is mostly implemented in a middleware. Add it to your
    # MIDDLEWARE setting"
    # "The order of MIDDLEWARE is important. You should include the Debug
    # Toolbar middleware as early as possible in the list. However, it must
    # come after any other middleware that encodes the response’s content,
    # such as GZipMiddleware."
    current_settings["MIDDLEWARE"] = _inject_middleware(current_settings["MIDDLEWARE"])


def _inject_middleware(current_middleware: list[str]) -> list[str]:
    """Inject DebugToolbarMiddleware early, but not too early."""
    TOOLBAR_MUST_GO_AFTER = [
        "django.middleware.gzip.GZipMiddleware",
        "xff.middleware.XForwardedForMiddleware",
        "x_forwarded_for.middleware.XForwardedForMiddleware",
    ]
    position = max(
        _next_index_or_start(current_middleware, mw) for mw in TOOLBAR_MUST_GO_AFTER
    )

    return [
        *current_middleware[:position],
        "debug_toolbar.middleware.DebugToolbarMiddleware",
        *current_middleware[position:],
    ]


def _next_index_or_start(lst: list, item):
    try:
        return lst.index(item) + 1
    except ValueError:
        return 0

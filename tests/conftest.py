from django.conf import settings
import django


def pytest_configure():
    settings.configure(
        STATIC_URL="/static/"
    )
    django.setup()

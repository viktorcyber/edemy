from .base import *


REST_FRAMEWORK.update({
    "TEST_REQUEST_DEFAULT_FORMAT": "json"
})

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": ":memory:",
    }
}


REST_FRAMEWORK.update({"TEST_REQUEST_DEFAULT_FORMAT": "json"})


# Disable migrations for speed
class DisableMigrations:
    def __contains__(self, item):
        return True

    def __getitem__(self, item):
        return None


MIGRATION_MODULES = DisableMigrations()

# Faster password hashing
PASSWORD_HASHERS = [
    "django.contrib.auth.hashers.MD5PasswordHasher",
]

CORS_ALLOW_ALL_ORIGINS = True

# Cache
CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.locmem.LocMemCache",
        "LOCATION": "unique-test",
    }
}

from .base import *


INTERNAL_IPS = ["127.0.0.1", "192.168.1.3"]

ALLOWED_HOSTS = ["*"]

CORS_ALLOW_ALL_ORIGINS = True

INSTALLED_APPS += ["debug_toolbar", "silk"]

MIDDLEWARE += [
    "debug_toolbar.middleware.DebugToolbarMiddleware",
    "silk.middleware.SilkyMiddleware",
]

DEBUG_TOOLBAR_CONFIG = {
    "SHOW_TOOLBAR_CALLBACK": lambda request: (
        DEBUG or "debug_toolbar.middleware.show_toolbar_with_docker"
    )
}

ELASTICSEARCH_DSL_INDEX_SETTINGS.update(
    {
        "number_of_replicas": 0,  # Number of replica shards (0 for development)
    }
)

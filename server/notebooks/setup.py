import os
import sys


def init(verbose=False):
    sys.path.append(os.path.abspath(".."))
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.local")
    os.environ.setdefault("INNGEST_DEV", "1")
    os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "true"
    os.environ.setdefault(
        "DATABASE_URL",
        "postgresql://neondb_owner:npg_HFL3T9AsDiMo@ep-snowy-mountain-aziy9g7m-pooler.c-3.ap-southeast-1.aws.neon.tech/neondb?sslmode=require&channel_binding=require",
    )
    import django

    django.setup()

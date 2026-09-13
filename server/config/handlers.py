import sentry_sdk

from rest_framework.views import exception_handler


class SentryExceptionHandler:
    def __call__(self, exc, context):
        response = exception_handler(exc, context)
        sentry_sdk.capture_exception(exc)
        return response


sentry_exception_handler = SentryExceptionHandler()

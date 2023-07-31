from django.utils.deprecation import MiddlewareMixin
from django.views.decorators.csrf import csrf_protect


class CsrfProtectMiddleware(MiddlewareMixin):
    def process_view(self, request, callback, callback_args, callback_kwargs):
        if request.path.startswith("/admin") or request.path.startswith("/__debug__"):
            return csrf_protect(callback)(request, *callback_args, **callback_kwargs)

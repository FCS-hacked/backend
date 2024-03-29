from auditlog.context import set_actor, disable_auditlog

from unauth.drf_custom_authentication import UnauthAuthentication


class AuditlogMiddleware:
    """
    Middleware to couple the request's user to log items. This is accomplished by currying the
    signal receiver with the user from the request (or None if the user is not authenticated).
    """

    def __init__(self, get_response=None):
        self.get_response = get_response

    @staticmethod
    def _get_remote_addr(request):
        if request.headers.get("X-Forwarded-For"):
            # In case of proxy, set 'original' address
            remote_addr = request.headers.get("X-Forwarded-For").split(",")[0]
            # Remove port number from remote_addr
            return remote_addr.split(":")[0]
        else:
            return request.META.get("REMOTE_ADDR")

    def __call__(self, request):
        remote_addr = self._get_remote_addr(request)

        user_tuple = UnauthAuthentication().authenticate(request)
        if user_tuple:
            context = set_actor(actor=user_tuple[0], remote_addr=remote_addr)
        else:
            context = disable_auditlog()

        with context:
            return self.get_response(request)

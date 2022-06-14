from uuid import UUID

from django.utils.translation import ugettext_lazy as _
from rest_framework import exceptions
from rest_framework.authentication import BaseAuthentication, \
    get_authorization_header

from accounts.models import User


class APIKeyAuthentication(BaseAuthentication):
    """
    Simple token based authentication.

    Clients should authenticate by passing the token key in the "Authorization"
    HTTP header, prepended with the string "Mobile ".  For example:

        x-api-key: feff76b8-1e82-4328-9e8d-96400f43713d
    """

    def authenticate(self, request):
        api_key = request.META.get('HTTP_X_API_KEY')

        try:
            UUID(api_key)
        except (ValueError, TypeError):
            msg = _('Invalid api key format. Not an UUID string.')
            raise exceptions.AuthenticationFailed(msg)

        if not api_key:
            msg = _('Invalid api key header. No credentials provided.')
            raise exceptions.AuthenticationFailed(msg)

        return self.authenticate_credentials(api_key)

    def authenticate_credentials(self, key):
        try:
            user = User.objects.get(api_key=key)
        except User.DoesNotExist:
            raise exceptions.AuthenticationFailed(_('Invalid token.'))

        return user, None

from allauth_2fa.adapter import OTPAdapter
from allauth_2fa.middleware import BaseRequire2FAMiddleware
from composed_configuration.authentication.adapter import EmailAsUsernameAccountAdapter


# composed-configuration already overrides the ACCOUNT_ADAPTER, so we need to subclass it to add 2FA
class TwoFactorAuthAdapter(OTPAdapter, EmailAsUsernameAccountAdapter):
    pass


class RequireTwoFactorAuthMiddleware(BaseRequire2FAMiddleware):
    def require_2fa(self, request):
        return True

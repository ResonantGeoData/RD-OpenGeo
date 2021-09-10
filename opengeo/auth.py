from allauth_2fa.adapter import OTPAdapter
from composed_configuration.authentication.adapter import EmailAsUsernameAccountAdapter


# composed-configuration already overrides the ACCOUNT_ADAPTER, so we need to subclass it to add 2FA
class TwoFactorAuthAdapter(OTPAdapter, EmailAsUsernameAccountAdapter):
    pass

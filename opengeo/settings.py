from pathlib import Path
from typing import Type

from composed_configuration import (
    ComposedConfiguration,
    ConfigMixin,
    CorsMixin,
    DevelopmentBaseConfiguration,
    HerokuProductionBaseConfiguration,
    ProductionBaseConfiguration,
    TestingBaseConfiguration,
)
from configurations import values
from rgd.configuration import ResonantGeoDataBaseMixin


class TwoFactorAuthMixin(ConfigMixin):
    @staticmethod
    def before_binding(configuration: Type[ComposedConfiguration]):
        configuration.INSTALLED_APPS += [
            # Configure the django-otp package.
            'django_otp',
            'django_otp.plugins.otp_totp',
            'django_otp.plugins.otp_static',
            # Enable two-factor auth.
            'allauth_2fa',
        ]
        configuration.MIDDLEWARE += [
            'django_otp.middleware.OTPMiddleware',
            'allauth_2fa.middleware.AllauthTwoFactorMiddleware',
            'opengeo.auth.RequireTwoFactorAuthMiddleware',
        ]

    ACCOUNT_ADAPTER = 'opengeo.auth.TwoFactorAuthAdapter'


class OpenGeoMixin(ResonantGeoDataBaseMixin, CorsMixin, TwoFactorAuthMixin, ConfigMixin):
    WSGI_APPLICATION = 'opengeo.wsgi.application'
    ROOT_URLCONF = 'opengeo.urls'

    BASE_DIR = Path(__file__).resolve(strict=True).parent.parent

    # Override to allow anyone to sign up
    RGD_AUTO_APPROVE_SIGN_UP = values.Value(default=True)

    @staticmethod
    def before_binding(configuration: Type[ComposedConfiguration]):
        # Install local apps first, to ensure any overridden resources are found first
        configuration.INSTALLED_APPS = [
            'opengeo.core.apps.CoreConfig',
        ] + configuration.INSTALLED_APPS

        # Install additional apps
        configuration.INSTALLED_APPS += [
            's3_file_field',
            'rules.apps.AutodiscoverRulesConfig',  # TODO: need this?
            # To ensure that exceptions inside other apps' signal handlers do not affect the
            # integrity of file deletions within transactions, CleanupConfig should be last.
            'django_cleanup.apps.CleanupConfig',
            'rgd',
            'rgd_3d',
            'rgd_fmv',
            'rgd_geometry',
            'rgd_imagery',
        ]

    # To use endpoints from external origin
    CORS_ORIGIN_ALLOW_ALL = True


class DevelopmentConfiguration(OpenGeoMixin, DevelopmentBaseConfiguration):
    pass


class TestingConfiguration(OpenGeoMixin, TestingBaseConfiguration):
    CELERY_TASK_ALWAYS_EAGER = True
    CELERY_TASK_EAGER_PROPAGATES = True


class ProductionConfiguration(OpenGeoMixin, ProductionBaseConfiguration):
    pass


class HerokuProductionConfiguration(OpenGeoMixin, HerokuProductionBaseConfiguration):
    # Use different env var names (with no DJANGO_ prefix) for services that Heroku auto-injects
    DATABASES = values.DatabaseURLValue(
        environ_name='DATABASE_URL',
        environ_prefix=None,
        environ_required=True,
        engine='django.contrib.gis.db.backends.postgis',
        conn_max_age=600,
        ssl_require=True,
    )

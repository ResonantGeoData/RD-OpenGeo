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


class MemachedCloudMixin(ConfigMixin):
    MEMCACHED_URL = values.Value(
        default=None, environ_name='MEMCACHEDCLOUD_SERVERS', environ_prefix=None
    )
    MEMCACHED_USERNAME = values.Value(
        default=None, environ_name='MEMCACHEDCLOUD_USERNAME', environ_prefix=None
    )
    MEMCACHED_PASSWORD = values.Value(
        default=None, environ_name='MEMCACHEDCLOUD_PASSWORD', environ_prefix=None
    )
    MEMCACHED_BINARY = values.Value(default=True)
    SESSION_ENGINE = 'django.contrib.sessions.backends.cached_db'

    @classmethod
    def post_setup(cls):
        super().post_setup()

        if cls.MEMCACHED_URL:
            caches = {
                'default': {
                    'BACKEND': 'django.core.cache.backends.memcached.PyLibMCCache',
                    'LOCATION': cls.MEMCACHED_URL,
                    'OPTIONS': {
                        'binary': cls.MEMCACHED_BINARY,
                    },
                }
            }

            if cls.MEMCACHED_USERNAME and cls.MEMCACHED_PASSWORD:
                caches['default']['OPTIONS']['username'] = cls.MEMCACHED_PASSWORD
                caches['default']['OPTIONS']['password'] = cls.MEMCACHED_USERNAME

            cls.CACHES = caches


class OpenGeoMixin(ResonantGeoDataBaseMixin, CorsMixin, ConfigMixin):
    WSGI_APPLICATION = 'opengeo.wsgi.application'
    ROOT_URLCONF = 'opengeo.urls'

    BASE_DIR = Path(__file__).resolve(strict=True).parent.parent

    # Override to allow anyone to sign up
    RGD_AUTO_APPROVE_SIGN_UP = values.Value(default=True)

    @staticmethod
    def mutate_configuration(configuration: Type[ComposedConfiguration]):
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


class HerokuProductionConfiguration(OpenGeoMixin, MemachedCloudMixin, HerokuProductionBaseConfiguration):
    # Use different env var names (with no DJANGO_ prefix) for services that Heroku auto-injects
    DATABASES = values.DatabaseURLValue(
        environ_name='DATABASE_URL',
        environ_prefix=None,
        environ_required=True,
        engine='django.contrib.gis.db.backends.postgis',
        conn_max_age=600,
        ssl_require=True,
    )

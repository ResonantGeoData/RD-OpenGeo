import re

from django.conf import settings
from django.contrib import admin
from django.urls import include, path, re_path
from django.views.generic.base import RedirectView
from drf_yasg import openapi
from drf_yasg.inspectors.view import SwaggerAutoSchema
from drf_yasg.views import get_schema_view
from rest_framework import permissions
import uritemplate  # noqa: F401


def drf_yasg_get_summary_and_description(self):
    """Return an operation summary and description.

    This is a modified form of the function in drf_yasg.

    When getting descriptions from view docstrings or when there is no summary,
    the resultant summary is prefixed with the method.  When taking
    descriptions from docstrings, change newlines to improve how the default
    swagger client displays them.
    """
    description = self.overrides.get('operation_description', None)
    summary = self.overrides.get('operation_summary', None)
    method = self.operation_keys[-1].replace('_', ' ').capitalize()
    if description is None:
        description = self._sch.get_description(self.path, self.method) or ''
        description = description.strip().replace('\r', '')

        if description and summary is None:
            # description from docstring... do summary magic
            summary, description = self.split_summary_from_description(description)
            # Replace single newlines with spaces and multiple newlines with
            # single newlines.
            description = re.sub(
                r'\r',
                '\n',
                re.sub(r'\n', ' ', re.sub(r'\n\n+', '\r', re.sub(r'\r', '', description))),
            )
            if summary:
                info = summary.rstrip('.')
                summary = f'{method} {info}'
            else:
                info = ' '.join(self.operation_keys[:-1])
                summary = f'{method} {info}'
    if summary is None:
        summary = f'{method} {description}'
    summary = summary[:120]

    return summary, description


# Modify drf_yasg's method of generating summaries and descriptions to work
# better with our views.
SwaggerAutoSchema.get_summary_and_description = drf_yasg_get_summary_and_description


urlpatterns = [
    path('accounts/', include('allauth.urls')),
    path('oauth/', include('oauth2_provider.urls', namespace='oauth2_provider')),
    path('admin/', admin.site.urls),
    path('api/s3-upload/', include('s3_file_field.urls')),
    path('', include('rgd.urls')),
    path('', include('rgd_3d.urls')),
    path('', include('rgd_fmv.urls')),
    path('', include('rgd_geometry.urls')),
    path('', include('rgd_imagery.urls')),
    # Redirect homepage to RGD core app homepage
    path(r'', RedirectView.as_view(url='rgd', permanent=False), name='index'),
]

schema_view = get_schema_view(
    openapi.Info(
        title='ResonantGeoData API',
        default_version='v1',
        description='ResonantGeoData',
        # terms_of_service='https://www.google.com/policies/terms/',
        contact=openapi.Contact(email='kitware@kitare.com'),
        license=openapi.License(name='Apache 2.0'),
    ),
    public=False,
    permission_classes=(permissions.AllowAny,),
    patterns=urlpatterns,
)

urlpatterns += [
    re_path(
        r'^swagger(?P<format>\.json|\.yaml)$',
        schema_view.without_ui(cache_timeout=0),
        name='schema-json',
    ),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]

if settings.DEBUG:
    import debug_toolbar

    urlpatterns = [path('__debug__/', include(debug_toolbar.urls))] + urlpatterns

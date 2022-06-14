import os
from django.urls import path, include
from django.contrib import admin
from drf_spectacular.views import SpectacularSwaggerView, SpectacularAPIView

urlpatterns = [
    path('api/', include('api.urls')),
]

urlpatterns += (
    path('admin/', admin.site.urls),
)

is_docs_allowed = (os.environ.get('APP_ENVIRONMENT') in ['develop', 'staging'])
if is_docs_allowed:
    urlpatterns += [
        path(
            'docs/',
            SpectacularSwaggerView.as_view(url_name='docs-openapi'),
            name='docs-ui'
        ),
        path(
            'docs/openapi.yaml',
            SpectacularAPIView.as_view(),
            name='docs-openapi'
        ),
    ]

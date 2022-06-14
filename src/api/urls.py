from django.urls import include, path

from api.views import HealthView

urlpatterns = [
    path('accounts/', include('accounts.urls')),
    path('classifier/', include('classifier.urls')),
    path('health/', HealthView.as_view(), name='health'),
]

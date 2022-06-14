from django.urls import path

from classifier import views

app_name = 'classifier'
urlpatterns = [
    path(
        'start-model-training/',
        views.StartUserModelTrainingView.as_view(),
        name='start-model-training',
    ),
    path(
        'get-model-training-status/',
        views.GetUserModelTrainingStatusView.as_view(),
        name='get-model-training-status',
    ),
    path(
        'get-model-training-data/',
        views.GetUserModelTrainingDataView.as_view(),
        name='get-model-training-data',
    ),
]

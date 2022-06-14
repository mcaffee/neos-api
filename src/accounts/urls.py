from django.urls import path

from accounts import views

app_name = 'accounts'
urlpatterns = [
    path(
        'save-user-character-sign/',
        views.SaveUserCharacterSignView.as_view(),
        name='save-user-character-sign',
    ),
]

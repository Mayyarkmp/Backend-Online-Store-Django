from django.urls import path, include
from . import views


app_name = 'core'

urlpatterns = [
    path('languages/', views.get_supported_languages, name='supported_languages'),
    path("media/", include("core.media.urls", namespace="media")),
]

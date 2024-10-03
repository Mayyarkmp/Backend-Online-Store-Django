from django.urls import path
from .views import FileUploadView,MediaListView

app_name = 'media'

urlpatterns = [
    path("", MediaListView.as_view(), name="media"),
    path('upload/', FileUploadView.as_view(), name="upload")
]
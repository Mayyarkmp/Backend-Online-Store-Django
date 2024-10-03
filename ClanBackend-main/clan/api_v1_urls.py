from django.urls import path, include
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

app_name = 'clan'

urlpatterns = [
    path("", include("core.urls", namespace="core")),
    path('auth/', include('users.auth.urls', namespace='auth')),
    path('users/', include('users.urls', namespace='users')),
    path('autherization/', include('permissions.urls', namespace="permissions")),
    path('chat/', include('chat.urls', namespace="chat")),
    path('branches/', include("branches.urls", namespace="branches")),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
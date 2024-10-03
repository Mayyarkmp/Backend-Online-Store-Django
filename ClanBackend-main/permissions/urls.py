from rest_framework import routers

from permissions import views

app_name = 'permissions'

router = routers.DefaultRouter()
router.register(r'roles', views.RoleViewSet)
router.register(r'permissions', views.PermissionViewSet)
urlpatterns = []
urlpatterns += router.urls

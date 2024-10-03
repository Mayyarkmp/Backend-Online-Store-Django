from rest_framework.routers import DefaultRouter
from .views import RoomViewSet

app_name = 'chat'
router = DefaultRouter()
router.register(r'rooms', RoomViewSet)

urlpatterns = router.urls
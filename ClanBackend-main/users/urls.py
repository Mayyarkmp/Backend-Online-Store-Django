
from rest_framework import routers
from users.views import UserViewSet, UserAddressViewSet,CardIDViewSet, UserInfoViewSet

app_name = 'users'

router = routers.DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'user-addresses', UserAddressViewSet)
router.register(r'crad-ids', CardIDViewSet)
router.register(r'user-info', UserInfoViewSet)



urlpatterns = [

]
urlpatterns += router.urls
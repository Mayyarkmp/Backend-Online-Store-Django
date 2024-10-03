from django.urls import path
from rest_framework.routers import DefaultRouter

from .views import BranchViewSet

app_name = 'branches'

router = DefaultRouter()
router.register('branches', BranchViewSet)

urlpatterns = []
urlpatterns += router.urls
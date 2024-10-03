from rest_framework.viewsets import ModelViewSet

from permissions.dynamic import DynamicPermission, BaseModelViewSet
from users.models import User, UserAddress, UserInfo, CardID
from users.serializers import UserSerializer, UserAddressSerializer, UserInfoSerializer, CardIDSerializer
from permissions.queryset import BranchDataFetcher



class UserViewSet(BaseModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [DynamicPermission]

    def get_queryset(self):
        return BranchDataFetcher(self.request.user, self.queryset.model).fetch_data()


class UserAddressViewSet(BaseModelViewSet):
    serializer_class = UserAddressSerializer
    queryset = UserAddress.objects.all()
    permission_classes = [DynamicPermission]
    
    def get_queryset(self):
        return BranchDataFetcher(self.request.user, self.queryset.model).fetch_data()


class UserInfoViewSet(BaseModelViewSet):
    serializer_class = UserInfoSerializer
    queryset = UserInfo.objects.all()
    permission_classes = [DynamicPermission]
    
    def get_queryset(self):
        return BranchDataFetcher(self.request.user, self.queryset.model).fetch_data()


class CardIDViewSet(BaseModelViewSet):
    serializer_class= CardIDSerializer
    queryset = CardID.objects.all()
    permission_classes = [DynamicPermission]

    def get_queryset(self):
        return BranchDataFetcher(self.request.user, self.queryset.model).fetch_data()


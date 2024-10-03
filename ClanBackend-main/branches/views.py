from rest_framework import generics, status, viewsets
from rest_framework.response import Response


from branches.models import Branch
from branches.serializers import BranchSerializer


class BranchViewSet(viewsets.ModelViewSet):
    queryset = Branch.objects.all()
    serializer_class = BranchSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = request.user
        serializer.save(owner=user)

        return Response({
            "message": "Successfully create Branch",
            "data": serializer.data
        }, status=status.HTTP_201_CREATED)

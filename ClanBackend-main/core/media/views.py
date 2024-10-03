from rest_framework.views import APIView
from rest_framework.response import Response

from permissions.dynamic import DynamicPermission
from rest_framework.permissions import IsAuthenticated, AllowAny
from .models import Media
from django.contrib.contenttypes.models import ContentType
from rest_framework.parsers import MultiPartParser, FormParser


class FileUploadView(APIView):
    permission_classes = [AllowAny,]
    parser_classes = [MultiPartParser, FormParser]

    @staticmethod
    def post(request, *args, **kwargs):
        file_obj = request.FILES['file']
        media_file = Media.objects.create(file=file_obj)
        return Response({"uid": media_file.uid, "file": media_file.file.url})


class MediaListView(APIView):
    permission_classes = (AllowAny,)

    @staticmethod
    def get(request, *args, **kwargs):
        query = Media.objects.all()
        model_filter = request.query_params.get('model')

        if model_filter:
            content_type = ContentType.objects.get(model=model_filter)
            query = query.filter(content_type=content_type)

        result = [{"uid": media.uid, "file": media.file.url} for media in query]
        return Response(result)
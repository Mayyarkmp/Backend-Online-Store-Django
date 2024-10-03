from pip._vendor.chardet.metadata.languages import Language
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response


# Create your views here.

@api_view(['GET'])
def get_supported_languages(request):
    supported_languages = [
        {
            "language" : "ar",
            "name" : {
                "ar": "العربية",
                "en": "English"
            }
        },
        {
            "language" : "en",
            "name" : {
                "ar": "الانجليزية",
                "en": "English",
            }
        }
    ]

    return Response(supported_languages, status=status.HTTP_200_OK)

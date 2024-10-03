from storages.backends.s3boto3 import S3Boto3Storage
from django.conf import settings
from minio_storage.storage import MinioStaticStorage,MinioMediaStorage


class StaticS3Boto3Storage(MinioStaticStorage):
    location = settings.STATICFILES_LOCATION
    base_url = "static/"

    def __init__(self,
                 location=None,
                 base_url=None,
                 file_permissions_mode=None,
                 directory_permissions_mode=None,
                 allow_overwrite=False,
                 *args,
                 **kwargs):
        if settings.MINIO_ACCESS_URL:
            self.secure_urls = False
            self.custom_domain = settings.MINIO_ACCESS_URL
        super(StaticS3Boto3Storage, self).__init__(*args, **kwargs)


class S3MediaStorage(MinioMediaStorage):
    def __init__(self, *args, **kwargs):
        if settings.MINIO_ACCESS_URL:
            self.secure_urls = False
            self.custom_domain = settings.MINIO_ACCESS_URL
        super(S3MediaStorage, self).__init__(*args, **kwargs)

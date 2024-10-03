import os
from . import BASE_DIR

# TODO: Make sure for configuration S3 Storage when test app

USE_S3 = 'True' == os.environ.get('USE_S3', False)
STATIC_ROOT = BASE_DIR / 'static'
STATIC_URL = 'http://localhost/static/'
MEDIA_URL = 'http://localhost/media/'

if USE_S3:
    DEFAULT_FILE_STORAGE = "storages.backends.s3.S3Storage"
    STATICFILES_STORAGE = 'storages.backends.s3.S3Storage'
    AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID')
    AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY')
    AWS_STORAGE_BUCKET_NAME = os.environ.get('AWS_STORAGE_BUCKET_NAME')
    AWS_S3_ENDPOINT_URL = os.environ.get('AWS_S3_ENDPOINT_URL')
    AWS_DEFAULT_ACL = None
    AWS_QUERYSTRING_AUTH = True
    AWS_S3_FILE_OVERWRITE = False

else:
    DEFAULT_FILE_STORAGE = "minio_storage.storage.MinioMediaStorage"
    STATICFILES_STORAGE = "minio_storage.storage.MinioStaticStorage"
    MINIO_STORAGE_ENDPOINT = os.environ.get('MINIO_STORAGE_ENDPOINT')
    MINIO_STORAGE_STATIC_URL = os.environ.get("MINIO_STORAGE_STATIC_URL")
    MINIO_STORAGE_MEDIA_URL = os.environ.get("MINIO_STORAGE_MEDIA_URL")
    MINIO_STORAGE_ACCESS_KEY = os.environ.get('MINIO_STORAGE_ACCESS_KEY')
    MINIO_STORAGE_SECRET_KEY = os.environ.get('MINIO_STORAGE_SECRET_KEY')
    MINIO_STORAGE_USE_HTTPS = "True" == os.environ.get("MINIO_STORAGE_USE_HTTPS")
    MINIO_STORAGE_MEDIA_OBJECT_METADATA = {"Cache-Control": "max-age=1000"}
    MINIO_STORAGE_MEDIA_BUCKET_NAME = 'media'
    MINIO_STORAGE_MEDIA_BACKUP_BUCKET = 'recycle-bin'
    MINIO_STORAGE_MEDIA_BACKUP_FORMAT = '%c/'
    MINIO_STORAGE_AUTO_CREATE_MEDIA_BUCKET = True
    MINIO_STORAGE_STATIC_BUCKET_NAME = 'static'
    MINIO_STORAGE_REGION = os.environ.get('MINIO_STORAGE_REGION')

STORAGES = {
    "staticfiles": {
        "BACKEND": DEFAULT_FILE_STORAGE,
    },
    "default": {
        "BACKEND": STATICFILES_STORAGE,
    },
}
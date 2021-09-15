from .base import *

ALLOWED_HOSTS = ["*"]
DEBUG = False

DEFAULT_FILE_STORAGE = "config.storage.S3MediaStorage"
STATICFILES_STORAGE = "config.storage.S3StaticStorage"

AWS_ACCESS_KEY_ID = os.environ.get("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.environ.get("AWS_SECRET_ACCESS_KEY")
AWS_S3_REGION_NAME = "ap-northeast-1"
AWS_STORAGE_BUCKET_NAME = "starscope-b"
AWS_S3_CUSTOM_DOMAIN = (
    f"{AWS_STORAGE_BUCKET_NAME}.s3.{AWS_S3_REGION_NAME}.amazonaws.com"
)
AWS_DEFAULT_ACL = "public-read"


STATIC_URL = f"https://{AWS_S3_CUSTOM_DOMAIN}.static/"
STATIC_ROOT = os.path.join(BASE_DIR, "static")
STATICFILES_DIRS = []


DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.mysql",
        "HOST": "starscope-database.ctmb7reo1s7l.ap-northeast-1.rds.amazonaws.com",
        "PORT": "3306",
        "NAME": "starscope-database",
        "PASSWORD": os.environ.get("DATABASE_PASSWORD"),
    }
}
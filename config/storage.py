from storages.backends.s3boto3 import S3Boto3Storage


class StaticStorage(S3Boto3Storage):
    location = 'public/static'


class MediaStorage(S3Boto3Storage):
    location = 'public/media'
    file_overwrite = False


class PrivateMediaStorage(S3Boto3Storage):
    location = 'private/media'
    file_overwrite = False

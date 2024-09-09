from oss2 import Auth, Bucket

from esExportRpc.config.conf import ALI_OSS_ENDPOINT, ALI_OSS_BUCKET_NAME, ALI_OSS_ACCESS_KEY_ID, \
    ALI_OSS_ACCESS_KEY_SECRET


def uploadFileToAliOss(fileName, objectTargetPathPrefix=r"export/"):
    auth = Auth(ALI_OSS_ACCESS_KEY_ID, ALI_OSS_ACCESS_KEY_SECRET)
    bucket = Bucket(auth, ALI_OSS_ENDPOINT, ALI_OSS_BUCKET_NAME)
    objectTargetPath = objectTargetPathPrefix + fileName
    bucket.put_object_from_file(objectTargetPath, fileName)

    fileObjectUrl = f"https://{ALI_OSS_BUCKET_NAME}.oss-cn-hangzhou.aliyuncs.com/{objectTargetPath}"

    return fileObjectUrl

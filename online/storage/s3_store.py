# Placeholder S3 store helper for model/artifact export. In production use boto3.
def upload_model(path, bucket, key):
    print('Upload', path, 'to', bucket, key)

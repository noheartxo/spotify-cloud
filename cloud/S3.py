import boto3
import botocore.exceptions

class S3: 
    def __init__(self, region):
        self.region = region
        self.s3_client = boto3.client('s3', region_name=region)

    def list_buckets(self):
        buckets = self.s3_client.list_buckets()
        print('Existing Buckets:')
        for idx, bucket in enumerate(buckets['Buckets']):
            print(f'  {idx+1} - {bucket["Name"]}')

    def create_bucket(self, bucket_name):
        location = {
            'LocationConstraint': self.region
        }

        PublicAccessConfig = {
            'BlockPublicAcls': True,
            'IgnorePublicAcls': True,
            'BlockPublicPolicy': True,
            'RestrictPublicBuckets': True
        }
        try:
            self.s3_client.create_bucket(Bucket=bucket_name, CreateBucketConfiguration=location)
            self.s3_client.put_public_access_block(
                Bucket=bucket_name, 
                PublicAccessBlockConfiguration=PublicAccessConfig
            )
        except botocore.exceptions.ClientError as e:
            print(e)
        except botocore.exceptions.NoRegionError or botocore.exceptions.InvalidRegionError as e:
            print(e)
        
    def delete_bucket(self, bucket_name):
        self.s3_client.delete_bucket(Bucket=bucket_name)

    def delete_file_from_bucket(self, bucket_name, key):
        self.s3_client.delete_object(Bucket=bucket_name, Key=key)

    def upload_to_bucket(self, bucket_name, filename, key):
        try:
            self.s3_client.upload_file(filename, bucket_name, Key=key)
        except botocore.exceptions.ClientError as e:
            print(e)


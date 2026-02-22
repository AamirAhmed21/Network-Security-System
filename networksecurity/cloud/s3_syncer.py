import os
import sys

from networksecurity.exception.exception import NetworkSecurityException 

class S3Syncer:

    def sync_folder_to_s3(self, local_folder: str, bucket_url: str):
        try:
            command = f"aws s3 sync {local_folder} {bucket_url}"
            os.system(command)
        except Exception as e:
            raise NetworkSecurityException(e, sys) from e
    def sync_folder_from_s3(self, bucket_url: str, local_folder: str):
        try:
            command = f"aws s3 sync {bucket_url} {local_folder}"
            os.system(command)
        except Exception as e:
            raise NetworkSecurityException(e, sys) from e
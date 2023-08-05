"""Core module for AWS S3 related operations"""
from sallron.util import settings
import pickle
import boto3
import os

def send_to_s3(key_path, obj_path):
    """
    Utility function to send objects to S3

    Args:
        key_path (str): Path to AWS keys
        obj_path (str): Path to object to be sent
    """

    # ensure everything needed is set
    if key_path and obj_path and settings.LOGGING_BUCKET:

        with open(key_path, "rb") as f:
            keys = pickle.load(f)

        s3 = boto3.session.Session(
            aws_access_key_id=keys.get("aws_access_key_id"),
            aws_secret_access_key=keys.get("aws_secret_access_key_id"),
            region_name="us-east-2"
        ).resource("s3")

        bucket = s3.bucket(settings.LOGGING_BUCKET)

        # note it expects a obj_path following path/to/obj.txt format
        # gets the last name of this sequence
        bucket.upload_file(obj_path, obj_path.split('/')[-1])

        # remove the current log file
        os.remove(obj_path)

    else:
        
        pass
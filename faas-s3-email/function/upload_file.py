"""
This file contains a function to upload local files to Amazon S3.
"""

import boto3
import datetime
import base64
from io import BytesIO


def upload_file(aws_access_key_id, aws_secret_access_key, filename_s3, image_data, bucket_name, human_detected):
    """
    Upload byte64 encoded JPEG image data as a new file in Amazon S3 and return its link.
    Depending on the image classification results, the file will be placed either
    in 'human' or 'false_positive' directory in the S3 bucket.

    :param aws_access_key_id
    :param aws_secret_access_key
    :param filename_s3: Filename that will appear in S3
    :param image_data: byte64 encoded JPEG image data
    :param bucket_name: Name of the S3 bucket
    :param human_detected: Result of the image classification
    :return: Link to the uploaded file
    """

    # Create an S3 client
    s3 = boto3.client('s3', aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key)

    if human_detected:
        filename_s3 = "human/{}".format(filename_s3)
    else:
        filename_s3 = "false_positive/{}".format(filename_s3)

    # Uploads the given file using a managed uploader, which will split up large
    # files automatically and upload parts in parallel.
    print("Uploading file {} to Amazon S3".format(filename_s3))
    image_decoded = base64.b64decode(image_data)
    s3.upload_fileobj(BytesIO(image_decoded), bucket_name, filename_s3, ExtraArgs={'ContentType': "image/jpeg", 'ACL': "public-read"})

    # Generate url
    url = s3.generate_presigned_url('get_object', Params = {'Bucket': bucket_name, 'Key': filename_s3}, ExpiresIn = 7*24*3600)

    return url

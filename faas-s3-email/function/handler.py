import json
import ConfigParser
from upload_file import *
from send_email import *


def handle(req):
    json_req = json.loads(req)
    image = json_req['image']
    detected_objects = json_req['detected_objects']

    # Read config file
    config = ConfigParser.ConfigParser()
    config.read('s3-email.cfg')

    aws_access_key_id = config.get('S3', 'aws_access_key_id')
    aws_secret_access_key = config.get('S3', 'aws_secret_access_key')
    bucket_name = config.get('S3', 'bucket', "rpizero-smart-camera-archive")
    user = config.get('Email', 'user')
    pwd = config.get('Email', 'pwd')

    human_detected = False
    for item in detected_objects:
        if item['class'] == 'person' and item['score'] > 0.5:
            human_detected = True
            break
    print("human_detected = {}".format(human_detected))

    # Upload image to S3 and remove the local copy
    url = upload_file(aws_access_key_id, aws_secret_access_key, image, bucket_name, human_detected)

    # Send e-mail notification
    if human_detected:
        subject = "Human detected"
        # Send only the top 10 identified objects
        body = "\n".join(["{0}: {1:.2f}".format(item['class'], item['score']) for item in detected_objects[:10]])
        # Send the link to the image in S3
        body += "\n\n{}".format(url)
        send_email(user, pwd, user, subject, body, image)

"""
This file contains a function to send e-mails.
"""

from __future__ import print_function
import smtplib
import base64
import re
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage


def send_email(user, pwd, recipient, subject, body, image_data):
    """
    Send an e-mail with a JPEG image attached.

    :param user: gmail account
    :param pwd: password
    :param recipient: recipient e-mail address (or a list of e-mail addresses)
    :param body: message text
    :param image_data: byte64 encoded JPEG image data
    """

    gmail_user = user
    gmail_pwd = pwd
    FROM = user
    TO = recipient if type(recipient) is list else [recipient]
    SUBJECT = subject
    TEXT = body

    #message = """From: %s\nTo: %s\nSubject: %s\n\n%s
    #""" % (FROM, ", ".join(TO), SUBJECT, TEXT)
    msgRoot = MIMEMultipart()
    msgRoot["From"] = FROM
    msgRoot["To"] = ", ".join(TO)
    msgRoot["Subject"] = SUBJECT
    msgText = MIMEText(TEXT)
    msgRoot.attach(msgText)
    image_decoded = base64.b64decode(image_data)
    msgImg = MIMEImage(image_decoded, 'jpeg')
    # Find a filename in the message text and use it for the attached image.
    filename = re.findall('/([^/]+\.jpg)', TEXT)[0]
    msgImg.add_header("Content-Disposition", "attachment", filename=filename)
    msgRoot.attach(msgImg)

    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.ehlo()
        server.starttls()
        server.login(gmail_user, gmail_pwd)
        #server.sendmail(FROM, TO, message)
        server.sendmail(FROM, TO, msgRoot.as_string())
        server.close()
        print("successfully sent the mail")
    except:
        print("failed to send mail")

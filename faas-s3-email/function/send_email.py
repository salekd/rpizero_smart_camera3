"""
This file contains a function to send e-mails.
"""

from __future__ import print_function
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


def send_email(user, pwd, recipient, subject, body):
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
    msgText = MIMEText(TEXT, 'html')
    msgRoot.attach(msgText)

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

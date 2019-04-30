import datetime
import smtplib
import pandas as pd

import email.utils
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


message1 = ""

# This code check the present day file with yesterday file and notify the recipient
try:
    today_file = pd.read_csv("/home/ec2-user/filename/filename_{}.csv"
                         .format(datetime.datetime.now().date()))
except:
    message1 = "Today's file is not downloaded.... There might be some issue in the website. Kindly Check."
    print(msg)

# sending the notification mail

SENDER = '<sender email>'
SENDERNAME = '<sender name>'

# Replace recipient@example.com with a "To" address. If your account
# is still in the sandbox, this address must be verified.
RECIPIENT  = '<recipient email>'

# Replace smtp_username with your Amazon SES SMTP user name.
USERNAME_SMTP = "<SES SMTP user name>"

# Replace smtp_password with your Amazon SES SMTP password.
PASSWORD_SMTP = "<SES SMTP Password>"

# (Optional) the name of a configuration set to use for this message.
# If you comment out this line, you also need to remove or comment out
# the "X-SES-CONFIGURATION-SET:" header below.
# CONFIGURATION_SET = "ConfigSet"

# If you're using Amazon SES in an AWS Region other than US West (Oregon),
# replace email-smtp.us-west-2.amazonaws.com with the Amazon SES SMTP
# endpoint in the appropriate region.
HOST = "email-smtp.us-west-2.amazonaws.com"
PORT = 587

# The subject line of the email.
SUBJECT = 'filename Data File'

message = '''\
            Today's file is correctly downloaded.
        '''

# Create message container - the correct MIME type is multipart/alternative.
msg = MIMEMultipart('alternative')
msg['Subject'] = SUBJECT
msg['From'] = email.utils.formataddr((SENDERNAME, SENDER))
msg['To'] = RECIPIENT
# Comment or delete the next line if you are not using a configuration set
# msg.add_header('X-SES-CONFIGURATION-SET',CONFIGURATION_SET)



# Attach parts into message container.
# According to RFC 2046, the last part of a multipart message, in this case
# the HTML message, is best and preferred.

# Try to send the message.
try:
    server = smtplib.SMTP(HOST, PORT)
    server.ehlo()
    server.starttls()
    #stmplib docs recommend calling ehlo() before & after starttls()
    server.ehlo()
    server.login(USERNAME_SMTP, PASSWORD_SMTP)
	    if msg == "":

        part1 = MIMEText(message,'plain')
        msg.attach(part1)
        server.sendmail(SENDER, RECIPIENT, msg.as_string())
    else:

        part2 = MIMEText(message1,'plain')
        msg.attach(part2)
        server.sendmail(SENDER, RECIPIENT, msg.as_string())
    server.close()


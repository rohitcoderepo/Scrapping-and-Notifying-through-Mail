import datetime
import smtplib
import pandas as pd

import email.utils
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText




# This code check the present day file with yesterday file and notify the recipient
today_file = pd.read_csv("/home/ec2-user/filename/filename_{}.csv"
                         .format(datetime.datetime.now().date()))



yester_file = None

last_uploaded_day = datetime.date.today().toordinal()

while yester_file is None:
    if yester_file is None:
            last_uploaded_day -= 1
    else:
            last_uploaded_day = last_uploaded_day

    try:
        yester_file = pd.read_csv("/home/ec2-user/filename/filename_{}.csv"
                          .format(datetime.date.fromordinal(last_uploaded_day)))

    except:
        yester_file = None



today_file = today_file[['Subject','TrackingNo','From','On']]
yester_file = yester_file[['Subject','TrackingNo','From','On']]

# create a list with file name
yester_list_files = yester_file["Subject"].tolist()
todays_file_list = today_file["Subject"].tolist()

# Checking for new file
msg, msg1, msg2, msg3 = "","","",""
file_name = []
tracking_name = []
sender = []
date = []
i = 0

for index,rows in today_file.iterrows():
    if rows[0] not in yester_list_files:
        print('New File Found named "{}"'.format(rows[0]))

        file_name.append(rows[0])
        tracking_name.append(rows[1])
        sender.append(rows[2])
        date.append(rows[3])
        i = i + 1

Date_old = {k: g["On"].tolist() for k,g in yester_file.groupby("Subject")}
Date_new = {k: g["On"].tolist() for k,g in today_file.groupby("Subject")}

modified_date = []
for key,value in Date_new.items():
    for key1,value1 in Date_old.items():
        if key == key1:
            for j in range(0,len(value)):
                if value[j] not in value1:
                    lst = key
                    modified_date.append(lst)

modified_msg3 = 'File/files uploaded date changed : {}'.format(modified_date)

if i != 0:
    msg = 'New {} Files Found named "{}"'.format(i,file_name)

    msg1 = 'Tracking Number : {}'.format(tracking_name)

    msg2 = 'From : {}'.format(sender)

    msg3 = 'On : {}'.format(date)


if msg == "" and len(modified_date) == 0:
    flag = 0
    status = "No Change"

else:
    flag = 1
    status = "Change"

# creating a flag to check if there is any change or not


try:
    check_file = pd.read_csv("/home/ec2-user/filename/Daily_Check_filenameInfo.csv")

    check_file = check_file.append({'Date':datetime.datetime.now().date() , 'Status': status},ignore_index=True)

    check_file.to_csv("/home/ec2-user/filename/Daily_Check_filenameInfo.csv",index=False)

except:
    d = {'Date':['2019-03-28'],'Status':['No Change']}

    check_file = pd.DataFrame(d)
    check_file.to_csv("/home/ec2-user/filename/Daily_Check_filenameInfo.csv")

# sending the notification mail

SENDER = '<sender email>'
SENDERNAME = '<sender name>'

# Replace recipient@example.com with a "To" address. If your account
# is still in the sandbox, this address must be verified.
RECIPIENT  = '<recipient email>'

# Replace smtp_username with your Amazon SES SMTP user name.
USERNAME_SMTP = "<SES SMTP user name>"

# Replace smtp_password with your Amazon SES SMTP password.
PASSWORD_SMTP = "<SES SMTP password>"

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
SUBJECT = 'filename Message Board'

# The email body for recipients with non-HTML email clients.
message = """ \
               The Following are the changes in filename Message Board:

              {} \n

              {} \n
              {} \n
              {} \n
              {} \n
        """.format(modified_msg3,msg, msg1, msg2, msg3)

# The HTML body of the email.

message1 = """ \
              There is no new message in the file as compared to yesterday's file.

           """

# Create message container - the correct MIME type is multipart/alternative.
msg = MIMEMultipart('alternative')
msg['Subject'] = SUBJECT
msg['From'] = email.utils.formataddr((SENDERNAME, SENDER))
msg['To'] = RECIPIENT
# Comment or delete the next line if you are not using a configuration set
# msg.add_header('X-SES-CONFIGURATION-SET',CONFIGURATION_SET)

# Record the MIME types of both parts - text/plain and text/html.

part1 = MIMEText(message,'plain')
part2 = MIMEText(message1,'plain')

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
    if flag == 1:

        part1 = MIMEText(message,'plain')
        msg.attach(part1)
        server.sendmail(SENDER, RECIPIENT, msg.as_string())
    else:

        part2 = MIMEText(message1,'plain')
        msg.attach(part2)
        server.sendmail(SENDER, RECIPIENT, msg.as_string())
    server.close()
# Display an error message if something goes wrong.
except Exception as e:
    print ("Error: ", e)
else:
    print ("Email sent!")

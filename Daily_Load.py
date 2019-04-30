import requests
from lxml import html as lh
import datetime
import pandas as pd
import smtplib
import email.utils
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

#specify the credentials
payload = {"userName": '<username>' , "password": '<password>'}

# specify the url
URL = 'login url'

msg = 'page url'


# Extracting all the elements with tag <tr>
session_requests = requests.session()

result = session_requests.post(URL, data = payload)

message1 = ""
try:

    result = session_requests.get(msg)

    tree = lh.fromstring(result.content)
    tr_elements = tree.xpath("//tr")
except:
    message1 = "Error in accessing the message web page"
    print(msg)


#Create empty list
col=[]
i=0
#For each row, store each first element (header) and an empty list
for t in tr_elements[0]:
    i+=1
    name=t.text_content()
    # print ('%d:"%s"'%(i,name))
    col.append((name,[]))

for j in range(1,len(tr_elements)):
    #T is our j'th row
    T=tr_elements[j]



    #i is the index of our column
    i=0

    #Iterate through each element of the row
    for t in T.iterchildren():
        data=t.text_content()
        #Check if row is empty
        if i>0:
        #Convert any numerical value to integers
            try:
                data=int(data)
            except:
                pass
        #Append the data to the empty list of the i'th column
        col[i][1].append(data)
        #Increment i for the next column
        i+=1


Dict={title:column for (title,column) in col}
df=pd.DataFrame(Dict)

# Changing the column name and dropping columns which are of no importance
lt = list(df.columns)
new = []
for i in range(len(lt)):
    lt[i] = 'Columns'+ str(i)
    j = lt[i]
    new.append(j)
df.columns = new

df.drop(['Columns0', 'Columns1', 'Columns2'],axis=1,inplace=True)
df = df.rename(index=str,columns = {'Columns3':'Subject','Columns4':'TrackingNo','Columns5':'From','Columns6':'On'})

#transfer the file to specified location

df.to_csv("/home/ec2-user/filename/filename_{}.csv".format(datetime.datetime.now().date()))

SENDER = '<sender email>'
SENDERNAME = 'sender username'

RECIPIENT = '<recipient email>'

# Replace smtp_username with your Amazon SES SMTP user name.
USERNAME_SMTP = "<SES SMTP username>"


# Replace smtp_password with your Amazon SES SMTP password.
PASSWORD_SMTP = "<SES SMTP Password>"


HOST = "email-smtp.us-west-2.amazonaws.com"
PORT = 587

# The subject line of the email.
SUBJECT = 'filename Data Accessing Issue'

# Create message container - the correct MIME type is multipart/alternative.
msg = MIMEMultipart('alternative')
msg['Subject'] = SUBJECT
msg['From'] = email.utils.formataddr((SENDERNAME, SENDER))
msg['To'] = RECIPIENT
# Comment or delete the next line if you are not using a configuration set
# msg.add_header('X-SES-CONFIGURATION-SET',CONFIGURATION_SET)

# Record the MIME types of both parts - text/plain and text/html.
message = '''
            The Message web page has been successfully accessed.
         '''

part1 = MIMEText(msg,'plain')


try:
    server = smtplib.SMTP(HOST, PORT)
    server.ehlo()
    server.starttls()
    #stmplib docs recommend calling ehlo() before & after starttls()
    server.ehlo()
    server.login(USERNAME_SMTP, PASSWORD_SMTP)
    if message1 == "":

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

import datetime

import pandas as pd



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
list_files = yester_file["Subject"].tolist()


# Checking for new file
msg, msg1, msg2, msg3 = "","","",""
for index,rows in today_file.iterrows():
    if rows[0] not in list_files:
        # print('New File Found named "{}"'.format(rows[0]))

        msg = 'New File Found named "{}"'.format(rows[0])

old_dict = yester_file.set_index('Subject').to_dict()

# Checking if there is any change in file type
for key,value in old_dict.items():
    if key == 'TrackingNo':
        for index, row in today_file.iterrows():

            for name1,value1 in value.items():
                if name1 == row[0]:

                    if value1 != row[1]:

                        # print("{} file type mismatched".format(name1))

                        msg1 = "{} TrackingNo changed from {} to {}".format(name1,value1, row[1])

# Checking if there is any change in size
    elif key == 'From':
        for name2,value2 in value.items():
            for index, row in today_file.iterrows():
                if name2 == row[0]:
                    if value2 != row[2]:
                        msg2 = "{} uploaded a file {} ".format(row[2],name2)

# Checking if there is any change in uploaded date
    elif key == 'On':
        for name3,value3 in value.items():
            for index, row in today_file.iterrows():
				if name3 == row[0]:
                    if value3 != row[3]:
                        # print("{} file uploaded date changed".format(name3))

                        msg3 = "{} file uploaded date changed to {}".format(name3,row[3])

# creating a flag to check if there is any change or not

if msg == "" and msg1 == "" and msg2 == "" and msg3 == "":
    flag = 0
    status = "No Change"
else:
    flag = 1
    status = "Change"

try:
    check_file = pd.read_csv("/home/ec2-user/filename/Daily_Check_filenameInfo.csv")

    check_file = check_file.append({'Date':datetime.datetime.now().date() , 'Status': status},ignore_index=True)

    check_file.to_csv("/home/ec2-user/filename/Daily_Check_filenameInfo.csv",index=False)

except:
    d = {'Date':['2019-03-28'],'Status':['No Change']}

    check_file = pd.DataFrame(d)
    check_file.to_csv("/home/ec2-user/filename/Daily_Check_filenameInfo.csv")


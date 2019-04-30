import requests
from lxml import html as lh
import datetime
import pandas as pd

#specify the credentials
payload = {"userName": 'xxxxxxx' , "password": 'xxxxxxxx'}

# specify the url
URL = 'url'

msg = 'url_page'


# Extracting all the elements with tag <tr>
session_requests = requests.session()

result = session_requests.post(URL, data = payload)

result = session_requests.get(msg)

tree = lh.fromstring(result.content)
tr_elements = tree.xpath("//tr")


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

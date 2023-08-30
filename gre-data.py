import pymysql
import random
import string
from datetime import datetime


def varchar(num):
    return "VARCHAR(" + str(num) + ")"


def createTable(cursor):
    sql = "CREATE TABLE "
    tableName = input("Please input table name: ")
    sql = sql + tableName + "("
    while (1):
        print("\nInput 'end' to end.")
        colName = input("Please input col name and attribute: ")
        if (colName == "end"):
            break
        sql = sql + colName + ", "

    sql = sql[:-2] + ")"
    print("sql: ", sql)
    #
    # cursor.execute(sql)
    # data = cursor.fetchone()

    print("Result: ", data)


def random_str(randomlength=16):
    """
    生成一个指定长度的随机字符串
    """
    str_list = [random.choice(string.digits + string.ascii_letters) for i in range(randomlength)]
    random_str = ''.join(str_list)
    return random_str


def random_int(randomlength=16):
    """
    生成一个指定长度的随机数字
    """
    str_list = [random.choice(string.digits) for i in range(randomlength)]
    random_str = ''.join(str_list)
    return random_str

def random_time():
    """
    生成一个time
    """
    year = random.randint(2015, 2018)
    month = random.randint(1, 12)
    day = random.randint(1, 28)
    hour = random.randint(1, 12)
    min = random.randint(0, 59)
    sec = random.randint(0, 59)
    timeStamp = datetime(year, month, day, hour, min, sec)
    return timeStamp



def insertData(cursor, db, n):
    print("\nUsage:")
    print("First, input table name")
    print("Second, input one col name")
    print("Then, input the colname's type. here is two type to choose: 'int' and 'char' ")
    print("These type's length are 6 (default)\n")
    print("Then, input the next colname and its type while the last colname")
    sql = "insert into "
    tableName = input("\nPlease input table name:")
    sql = sql + tableName + "("
    coltype = []
    flag = 1
    while (1):
        print("\nInput 'end' to end.")
        colName = input("Please input col name:")
        if (colName == 'end'):
            break;
        sql = sql + colName + ", "
        ctype = input("Please input col type:")
        if (ctype.count('int')==1):
            coltype.append(0)
        elif (ctype.count('char')==1):
            coltype.append(1)
        elif (ctype.count('time')==1):
            coltype.append(2)
        else:
            flag = 0;
            print("col type error!")
            print("Program exit!!")
            break;

    sql = sql[:-2] + ") values("
    tmpsql = sql
    if (flag == 1):
        for k in range(0, n):
            sql = tmpsql
            for i in coltype:
                if (i == 0):
                    sql = sql + random_int(1) + ", "
                elif(i==1):
                    sql = sql + "'" + random_str(6) + "'" + ", "
                else:
                    sql = sql + "'" + random_time().strftime("%Y-%m-%d %H:%M:%S") + "'" + ", "

            sql = sql[:-2] + ")"
            print("sql: ", sql)

            # cursor.execute(sql)
            # db.commit()
            print("Success ")
    else:
        print("Program encounter error!!")


'''
2022.1.14

'''
if __name__ == '__main__':
    # 打开数据库连接
    db = pymysql.connect(host='localhost',
                         user='root',
                         password='Root@123',
                         database='eapp')
    # 使用 cursor() 方法创建一个游标对象 cursor
    cursor = db.cursor()

    while (1):
        print("\nWelcome !!")
        print("1. Create Tbale ")
        print("2. Insert Data ")
        print("0. Exit ")
        num = input("Please input execute code:")
        if (num == '0'):
            print("Program exit !!")
            break;
        if (num == '1'):
            createTable(cursor)
        elif (num == '2'):
            n = input("Please input the number of data: ")
            insertData(cursor, db, int(n))
            print()

    # 关闭数据库连接
    db.close()


import pymysql;
import random
import string
from datetime import datetime


def random_str(randomlength):

    """
    生成一个指定长度的随机字符串
    """
    str_list = [random.choice(string.digits + string.ascii_letters) for i in range(randomlength)]
    random_str = ''.join(str_list)
    return random_str


def random_int(randomlength):
    """
    生成一个指定长度的随机数字
    """
    str_list = [random.choice(string.digits) for i in range(randomlength)]
    random_str = ''.join(str_list)
    return random_str


def random_time():
    """
    生成一个timestamp
    """
    year = random.randint(2015, 2018)
    month = random.randint(1, 12)
    day = random.randint(1, 28)
    hour = random.randint(1, 12)
    min = random.randint(0, 59)
    sec = random.randint(0, 59)
    timeStamp = datetime(year, month, day, hour, min, sec)
    return timeStamp

class GetMysqlTableComments():
    def __init__(self, host, user, password, database,port,charset):
        self.db = pymysql.connect(host=host, user=user, password=password, port=port, database=database, charset=charset)
        self.cursor = self.db.cursor()


    def get_tables_insert(self, database_name):
        sqlstr = ''
        # 查询mysql表名和注释
        self.cursor.execute(
            'select table_name,table_comment from information_schema.TABLES where TABLE_SCHEMA=%s order by table_name',
            database_name)
        return_tables = self.cursor.fetchall()

        # INSERT INTO `eapp_community`. `t_task_manager`(`id`, `updated_id`, `updated_by`)
        # VALUES(57, '商城消费', 0, 20, '2023-09-01 00:00:00', 'admin', '2023-08-04 14:43:08', 0, 1691131387816001, 1, 2);
        for tabledata in return_tables:
            return_columns = self.get_columns_insert(tabledata[0])
            sqlstr = sqlstr +'\n-- '+tabledata[1]+'\n'
            sqlstr = sqlstr + 'insert into ' +  tabledata[0] + '(' + return_columns +'\n'

        return sqlstr



    def get_columns_insert(self, table_name):
        # 查询mysql表字段注释
        self.cursor.execute('select column_name,COLUMN_TYPE,EXTRA,COLUMN_KEY from information_schema.COLUMNS where TABLE_NAME=%s', table_name)
        return_columns = self.cursor.fetchall()
        columnstr = ''

        coltype = []
        for columndata in return_columns:
            # TODO: 跳过所有自增id字段,唯一索引UNI，联合索引 MUL
            if ((columndata[0] == 'id' and columndata[2] == 'auto_increment') or columndata[3] =='UNI' or columndata[3] =='MUL' ):
                print(columndata[0])
                continue

            #列名加上`是为了防止列名使用了mysql关键字时会报sql语法错误
            columnstr = columnstr+"`"+columndata[0]+"`, "
            # 处理数据类型
            ctype = columndata[1]
    #         text,bit(1)decimal(10, 0)
            if (ctype.count('int') == 1):
                #todo: 数据look like is: 0int(5),为了方便后面截取数据类型的真实长度。
                coltype.append('0'+ctype)
            elif (ctype[:7] == 'varchar'):
                coltype.append('1'+ctype)
            elif (ctype.count('time') == 1):
                coltype.append('2'+ctype)
            elif (ctype[:4]=='text'):
                coltype.append('3'+ctype)
            elif (ctype[:7]=='decimal'):
                coltype.append('4'+ctype)
            elif (ctype[:3] == 'bit'):
                coltype.append('5'+ctype)
            elif (ctype[:4] == 'char'):
                coltype.append('6'+ctype)
            else:
                print("col type error!-------------"+ table_name+","+ ctype)
                # break;

        # 循环写入文件
        rows=100000
        outFile = open('outfile/'+table_name+'_insert_'+ str(rows) +'.sql', 'w+')
        for k in range(0, rows):
            valstr = ''
            for i in coltype:
                # TODO: 生成数据，可以进一步优化，精细化。
                #int
                if (i[:1] == '0'):
                    valstr = valstr + random_int(1) + ", "
                #varchar
                elif (i[:1] == '1'):
                    if(i.count('(')==1):
                        randomlength = int(i[i.index('(') + 1: i.index(')')])
                        valstr = valstr + "'" + random_str(randomlength > 50 and 50 or randomlength) + "'" + ", "
                elif(i[:1]=='2'):
                    valstr = valstr + "'" + random_time().strftime("%Y-%m-%d %H:%M:%S") + "'" + ", "
                # text
                elif(i[:1]=='3'):
                    valstr = valstr + "'" + random_str(50) + "'" + ", "
                # decimal
                elif (i[:1] == '4'):
                    valstr = valstr + random_int(3) + ", "
                # bit
                elif (i[:1] == '5'):
                    valstr = valstr + "1" + ", "
                # char
                elif (i[:1] == '6'):
                    valstr = valstr + "'1'" + ", "
                else:
                    #,...
                    valstr = valstr + random_int(1) + ", "

            valstr = valstr[:-2]
            sqlstr_insert = 'insert into ' + table_name + '(' + columnstr[:-2] + ') values (' + valstr +');\n'
            # print("valstr: ", valstr)
            outFile.write(sqlstr_insert)
        outFile.close()
        # 去掉最后一列的逗号和换行符
        return columnstr[:-2] + ") values (" + valstr +");"


    def closedb(self):
        self.cursor.close()
        # 关闭数据库
        self.db.close()


if __name__ == '__main__':
    #数据库地址
    host = '127.0.0.1'
    #数据库端口
    port=3306
    #数据库用户名
    user = 'root'
    #密码
    password = 'Root@123'
    #数据库名称
    database = 'eapp'
    #字符集
    charset = 'utf8'
    my_database = GetMysqlTableComments(host, user, password, database,port,charset)
    # 生成select语句
    # sqlstr = my_database.get_tables(database)
    # 生成insert语句
    sqlstr_insert = my_database.get_tables_insert(database)
    my_database.closedb()
    #生成的sql打印到控制台
    print(sqlstr_insert)
    #生成的sql保存到文件
    file_path='get_mysql.sql'
    with open(file_path,'w') as file:
        file.write(sqlstr_insert)

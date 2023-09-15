import pymysql
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
        delstr=''
        str = []
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
            if(return_columns !=''):
                sqlstr = sqlstr + 'insert into ' +  tabledata[0] + '(' + return_columns +'\n'


                cols = return_columns.split(',')
                for co in cols:
                    if (co.count('time`')==1):
                        # print(co)
                        delstr = delstr + 'delete from ' + tabledata[0] + " where substring("+ co[co.find('`') + 1: co.rfind('`')]+",1,4) in ('2015','2016','2017','2018');\n"
                        break

        str.append(sqlstr)
        str.append(delstr)
        return str



    def get_columns_insert(self, table_name):
        # 查询mysql表字段注释
        self.cursor.execute('select column_name,COLUMN_TYPE,EXTRA,COLUMN_KEY from information_schema.COLUMNS where TABLE_NAME=%s', table_name)
        return_columns = self.cursor.fetchall()
        columnstr = ''

        # 检查列表中是否存在包含'time'的字段，判断是否有create\update time常规字段
        if any(columndata[1].lower().count('time')==1 for columndata in return_columns):
            ()
        else:
            print(table_name+"  表中没有包含'time'的时间字段,无法清除数据，造数据时跳过此表" )
            # return ''

        if any(columndata[0].lower() == 'id' for columndata in return_columns):
            ()
        else:
            print(table_name+"  表中没有id字段")
            # return ''



        coltype = []
        for columndata in return_columns:
            # TODO: 跳过所有自增id字段,唯一索引UNI，联合索引 MUL,主键PRI
            set_null = False

            # column_name,COLUMN_TYPE,EXTRA,COLUMN_KEY
            if (columndata[3].upper() in ('PRI','UNI' ,'MUL' )):
                # print(table_name+"有唯一约束："+columndata[0])
                set_null =True
            if (columndata[3] == 'PRI' and (columndata[2].lower() != 'auto_increment' or columndata[0].lower() != 'id')):
                print(table_name+"  表有PRI主键字段，但非自增： "+columndata[0]+"   "+columndata[2]+"   "+columndata[1])
                set_null=True
            if (columndata[1] in( 'timestamp','float','double')):
                print(table_name+"  表有包含监控字段： "+columndata[0]+"   "+columndata[2]+"   "+columndata[1])

            if set_null == True:
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
                print(table_name+"  表中字段    " +columndata[0] +" 处理未定义   "+ ctype)
                # break;

        # TODO: 循环生成文件-----------
        rows=100
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
                # time
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



    # # 数据库地址 Eapp
    # host = '172.25.125.12'
    # port=3306
    # user = 'eapp'
    # password = 'ZTRnsmHHZgq4Ra3m'
    # database = 'eapp_community'

    #
    #数据库地址 俄罗斯TSP
    host = '172.25.116.188'
    port=3306
    user = 'international_tsp'
    password = 'L3o19ZSwHC8t0LCw'
    database = 'chery_international_tsp_russia'
    #
    dbs = ['chery_int_tsp_rus_app','chery_int_tsp_rus_hu','chery_int_tsp_rus_manage','chery_international_tsp_russia']
    # dbs=['eapp_community','eapp_config','eapp_market','eapp_notify','eapp_pay','eapp_shop','eapp_sys','eapp_user','xxl_job']

    for database in dbs:
        print(database+"库")
        #字符集
        charset = 'utf8'
        my_database = GetMysqlTableComments(host, user, password, database,port,charset)
        # 生成select语句
        # sqlstr = my_database.get_tables(database)
        # 生成insert语句
        sqlstr_insert = my_database.get_tables_insert(database)
        my_database.closedb()
        #生成的sql打印到控制台
        # print(sqlstr_insert)
        #生成的sql保存到文件
        file_path='get_mysql.sql'
        with open(file_path,'w') as file:
            file.write(sqlstr_insert[0])

        #生成删除sql脚本,保存到文件
        file_path='del_data.sql'
        with open(file_path,'w') as file:
            file.write(sqlstr_insert[1])
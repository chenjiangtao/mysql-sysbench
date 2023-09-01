import os
import pymysql

if __name__ == '__main__':

    db = pymysql.connect(host='',
                         user='',
                         password='',
                         charset="utf8mb4",
                         database='')
    # 使用 cursor() 方法创建一个游标对象 cursor
    cursor = db.cursor()

    # 数据源目录
    path = 'outfile/'

    sqlstr_del ='';
    for dirpath, dirnames, filenames in os.walk(path):
        for file in filenames:
            ofile = os.path.join(dirpath, file)
            # print(ofile)
            if(file[-4:]=='.sql'):
                print(ofile)
                # load 方式
                # os.system('mysql -h172.25.125.12 -ueapp -pZTRnsmHHZgq4Ra3m -D eapp_community < ' + ofile)

                # 打开 SQL 文件并执行
                with open(ofile, 'r') as f:
                    line = f.readline()
                    while line:
                        # print(line)
                        try:
                            cursor.execute(line)
                        except Exception as e:
                            print(line)
                            print("异常数据:",e)
                        line = f.readline()

                f.close()

    # 提交更改
    db.commit()
    # 关闭数据库连接
    db.close()




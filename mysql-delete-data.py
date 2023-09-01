import pymysql

if __name__ == '__main__':
    # 打开数据库连接
    db = pymysql.connect(host='localhost',
                         user='root',
                         password='123',
                         charset="utf8mb4",
                         database='eapp')
    # 使用 cursor() 方法创建一个游标对象 cursor
    cursor = db.cursor()
    # 打开 SQL 文件并执行
    with open('del_data.sql', 'r') as f:
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





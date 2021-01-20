# -*- coding:utf-8 -*-

import uuid
import random
import time
from datetime import datetime
import pymysql as mysql
from threading import Thread, current_thread

host = "127.0.0.1"
port = 3306
username = "svc"
password = "svc123"
charset = "utf-8"
db = "svc"

class QuickInsert(object):
    def __init__(self):
        super(QuickInsert, self).__init__()

    @staticmethod
    def connect():
        return mysql.connect(host=host, port=port, user=username, passwd=password, db=db)

    def strTimeProp(self, start, end, prop, frmt):
        stime = time.mktime(time.strptime(start, frmt))
        etime = time.mktime(time.strptime(end, frmt))
        ptime = stime + prop * (etime - stime)
        return int(ptime)

    def randomTimestamp(self, frmt='%Y-%m-%d %H:%M:%S'):
        start = '2016-06-02 12:12:12'
        end = '2020-07-27 00:00:00'
        return self.strTimeProp(start, end, random.random(), frmt)

    def randomDate(self, frmt='%Y-%m-%d'):
        start = '2016-06-02'
        end = '2020-07-27'
        return self.strTimeProp(start, end, random.random(), frmt)

    def createPhone(self):
        for k in range(10):
            prelist = ["130", "131", "132", "133", "134", "135", "136", "137", "138", "139",
                       "147", "150", "151", "152", "153", "155", "156", "157", "158", "159",
                       "186", "187", "188", "189"]
            return random.choice(prelist) + "".join(random.choice("0123456789") for i in range(8))

    def getCardName(self):
        for k in range(10):
            prelist = ["圣诞咖啡快乐会员星礼包红杯字母款", "大杯香草风味星冰乐电子券", "星巴克星情月饼礼盒",
                       "大杯冷萃冰咖啡(手机银行)", "2020 年Roastery 专用咖啡乐园券", "大杯摩卡", "实用主义商品福袋",
                       "香草风味拿铁大杯电子券", "星巴克夏日活力早餐套餐电子券", "摩卡可可碎片星冰乐"]
            return random.choice(prelist)

    def getCardStatus(self):
        for k in range(10):
            prelist = ["01-已使用", "04-未激活", "03-未激活", "06-激活", "10-系统作废",
                       "0-已使用", "20-作废"]
            return random.choice(prelist)

    def getIsReplace(self):
        for k in range(10):
            prelist = ["Y", "N"]
            return random.choice(prelist)

    def insert_data(self, times, sql_b, s_id):
        startTime = datetime.now()
        print(current_thread().getName(), "开始时间", startTime)

        start_id = s_id
        sql_batch = sql_b
        print(current_thread().getName() + "开始于：" + str(start_id) + "，times：" + str(times))
        cursor = self.conn.cursor()

        for x in range(times):
            insert_user_sql = """
            INSERT INTO T_BALANCE_REPORT (`ID`,`ACCOUNT_ID`,`CARD_NO`,`CARD_NAME`,`CARD_STATUS`,`UPDATE_DATE`,`TRADING_DATE`,`BALANCE`,`INIT_AMOUNT`,`INIT_DATE`,`VALID_END_DATE`,`IS_REPLACE`,`OLD_CARD_NO`)
            VALUES ( %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s );
                """

            user_values, order_values = [], []
            # user_values = []
            for i in range(sql_batch):

                timestamp = self.randomTimestamp()
                time_local = time.localtime(timestamp)
                createTime = time.strftime("%Y-%m-%d %H:%M:%S", time_local)
                radomDate = time.strftime("%Y-%m-%d", time_local)
                user_id = str(uuid.uuid4())

                user_values.append((
                    # 参数
                    start_id,
                    start_id,
                    start_id,
                    self.getCardName() + str(start_id),
                    self.getCardStatus(),
                    createTime,
                    createTime,
                    random.randint(1, 30000) / random.randint(1, 17),
                    random.randint(100, 10000),
                    radomDate,
                    radomDate,
                    self.getIsReplace(),
                    # self.createPhone()
                    "".join(random.choice("0123456789") for i in range(8))
                ))

                start_id = start_id + 1

            cursor.executemany(insert_user_sql, user_values)
            # cursor.executemany(insert_user_sql, order_values)
            self.conn.commit()
            print(current_thread().getName() + "--写入点：" + str((x * 10000) + start_id))

        cursor.close()
        endTime = datetime.now()
        print(current_thread().getName(), "结束时间", endTime, "共持续", (endTime - startTime).seconds, "秒")


if __name__ == "__main__":

    # index = 3
    # quickInsert.insert_data("thread-" + str(index), 1000, (index * 10000) + 1)
    #########################################
    # 写入总数为：threads * times * sql_batch #
    # offset    : 偏移量，默认是0。如果数据库有数据，可以设一个起始点（偏移量）
    # threads   : 线程数
    # times     : 每个线程执行commit的次数
    # sql_batch : 每次commit多少数据
    # 例：要造一亿数据
    #   threads = 5
    #   times = 2000
    #   sql_batch = 10000
    #########################################
    offset = 0
    threads = 3
    times = 10
    sql_batch = 10000

    print("----------------本次写入总数：" + str(threads * times * sql_batch))

    for i in range(threads):
        start_id = (i * times * sql_batch) + offset
        quickInsert = QuickInsert()
        quickInsert.conn = QuickInsert.connect()

        t = Thread(target=quickInsert.insert_data, args=(times, sql_batch, start_id + 1))
        t.start()



# mysql sysbench
mysql sysbench是一款压测数据生成工具

## python3 生成压测数据说明
### quick_insert.py

使用程序方式批量插入数据的脚本，需要引入依赖包 pymysql

### quick_insert_threads.py

多线程批量插入数据的脚本，需要引入依赖包 pymysql

参数配置说明：

```
写入总数为：threads * times * sql_batch
offset    : 偏移量，默认是0。如果数据库有数据，可以设一个起始点（偏移量）
threads   : 线程数
times     : 每个线程执行commit的次数
sql_batch : 每次commit多少数据
例：要造一亿数据
    threads = 5
    times = 2000
    sql_batch = 10000
```

### quick_sql_insert.py

生成 insert 批量插入脚本，与上面的方式类似，只不过生成的文件需要手动执行。

### quick_txt_load.py

生成逗号分隔的 txt 文件，之后需要使用 `load data infile` 命令导入数据。


## 使用方法
### 配置数据源

```yaml
host = "127.0.0.1"
port = 3306
username = "root"
password = "123"
charset = "utf-8"
db = "test"
```
### 启动单线程版

```shell
python3 quick_insert.py &
```

### 启动多线程版

```shell
python3 quick_insert_threads.py &
```

# 根据mysql数据库中的表自动生成数据
python3 mysql-insert.py

# 说明
***测试可以直接使用sql/tab.sql建表，也可以改成自己的表结构***

- [生成mysql亿级压测数据程序](https://blog.csdn.net/evane1890/article/details/112911724)


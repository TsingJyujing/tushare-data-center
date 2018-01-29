# Tushare Data Center

## 简介

TuShare数据中心样例代码，仅仅存储了日线数据和5min线的数据，不包括均线数据（这种东西难道不应该用的时候自己算吗）。
使用的数据库方案是PostgreSQL 9.5/9.6。

目前这个数据中心建立了一个样板给developer们使用：

PostgreSQL连接信息：
- 地址：postgresql.lovezhangbei.top
- 用户名：tusharer
- 密码：tushare@979323
- 端口：15432
- 数据库名：stockdata（但是该账号对所有的数据库有访问权限）

注意每个月一共有1000GB流量的限制，到达975GB的时候我会关闭postgresql对外访问的接口来保护能正常访问服务器。
尽量只取自己要用的数据，数据每日更新的，每天都打包下载没意思……


## `data_appender.py` 使用说明

### 不带参数
不带参数的话，默认先下载近100天的日线数据，再下载近2周的5min线数据。

### 带俩参数
第一个参数为`5`或者`D`，代表5min线数据或者日线数据，第二个参数是下载近N天的数据。

### 在Python中调用：

`update_last_data(table_name: str, ktype: str, push_back_day: int = 10)`

其中`table_name`是目标数据库表的名称，ktype是线的类型，push_back_day是前推日期，从昨天开始推。


## 常见问题

### 如何贡献自己需要的数据
现在只有日线和5min线，但是想要加上自己的数据怎么办呢？
编写表结构，编写Python脚本和需要定期运行的Shell脚本，交给我审核，我帮你设为定时任务。
提交形式不限，可以发布在群里给大家讨论，也可以在github上fork我的项目然后提出一个merge request

### 为什么访问有点慢
第一个因为是PostgreSQL，连接的时候有点慢而已，其实查询数据传输的时候不慢。
因为服务器在国外，所以延迟比较大，最近VPS提供商还和我说最近巴黎所在的节点网络都慢……坑爹啊

### 这个服务器会一直存在吗？
服务器会一直存在，但是这样共享数据的形式不会一直存在，我会尽快开展P2P金融数据共享计划。


## 备注

### 数据库建设说明
执行创建数据库和创建表的SQL脚本即可。

关于权限控制的脚本参考如下：
```sql
CREATE USER tusharer WITH ENCRYPTED PASSWORD 'tushare@979323';
alter user tusharer set default_transaction_read_only=on;
GRANT USAGE ON SCHEMA public to tusharer;
Grant select on all tables in schema public to tusharer;
```

### 数据导入语句
```sh
pg_restore -h 127.0.0.1 -p 5432 -U postgres -W -d stockdata "/root/stockdata.backup"
```

### 定时任务信息
```
25 12   * * *   root    python3 /root/data_appender.py stock_5min_tick 5 3
25 12   * * 6   root    python3 /root/data_appender.py stock_daily_tick D 10
```

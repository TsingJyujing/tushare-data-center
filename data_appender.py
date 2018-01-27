#!/bin/python3

import sys
import traceback
from typing import Callable
import tushare as ts
import psycopg2
import datetime

insert_sql = "INSERT INTO %(table_name)s " \
             "(code, tick, volume, open, close, high, low)" \
             " VALUES ('%(code)s', '%(tick)s', " \
             "%(volume)s, %(open)s, %(close)s," \
             " %(high)s, %(low)s) ON CONFLICT DO NOTHING;"

deltatime_day = datetime.timedelta(seconds=3600 * 24)
daily_tick_format = "%Y-%m-%d"

# I won't write server password here~ LOL~~~
postgresql_config = {
    "host": "127.0.0.1",
    "dbname": "stockdata",
    "port": 5432,
    "username": "postgres",
    "password": "postgres"
}


class PostgreSQLStockDataWriter:
    def __init__(
            self,
            stock_db_name: str = postgresql_config["dbname"],
            host: str = postgresql_config["host"],
            port: int = postgresql_config["port"],
            user: str = postgresql_config["username"],
            password: str = postgresql_config["password"],
    ):
        # initialize stock db connection
        self.conn = psycopg2.connect(
            host=host,
            port=port,
            database=stock_db_name,
            password=password,
            user=user
        )

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.conn.commit()
        self.conn.close()

    def insert_data(
            self,
            table_name: str,
            code: str,
            tick: str,
            volume: str,
            open: str,
            close: str,
            high: str,
            low: str
    ):
        cursor = self.conn.cursor()
        try:
            sql_command = insert_sql % {
                "table_name": table_name,
                "code": code,
                "tick": tick,
                "volume": volume,
                "open": open,
                "close": close,
                "high": high,
                "low": low
            }
            cursor.execute(sql_command)
            self.conn.commit()
        except:
            print(traceback.format_exc(), file=sys.stderr)
        finally:
            cursor.close()


def retry_function(fun: Callable, retry_times: int = 5, print_debug_info: bool = False):
    for i in range(retry_times):
        try:
            fun()
            break
        except:
            if print_debug_info:
                print(traceback.format_exc())


def update_last_data(table_name: str, ktype: str, push_back_day: int = 10):
    now_time = datetime.datetime.now()
    end_day = datetime.datetime(now_time.year, now_time.month, now_time.day, 0, 0) - 1 * deltatime_day
    start_day = datetime.datetime(now_time.year, now_time.month, now_time.day, 0, 0) - push_back_day * deltatime_day
    with PostgreSQLStockDataWriter(host="127.0.0.1", password="postgres") as pg_data:
        # Get stock basic data
        stock_list = ts.get_stock_basics()
        for code, info in stock_list.iterrows():
            def get_stock_data():
                print("Get data of {}, basic info: \n{}".format(code, info))
                data = ts.get_k_data(
                    code,
                    start_day.strftime(daily_tick_format),
                    end_day.strftime(daily_tick_format),
                    ktype=ktype
                )
                for index, row in data.iterrows():
                    pg_data.insert_data(
                        table_name=table_name,
                        code=code,
                        tick=row['date'],
                        volume=row['volume'],
                        open=row['open'],
                        close=row['close'],
                        high=row['high'],
                        low=row['low']
                    )

            retry_function(get_stock_data, 5, True)


if __name__ == "__main__":
    if len(sys.argv) <= 1:
        update_last_data('stock_daily_tick', 'D', 100)
        update_last_data('stock_5min_tick', '5', 14)
    else:
        with open("run_logs.txt", "a") as fp:
            fp.write(
                "Running script in parameters: {} at {}\n".format(
                    " ".join(sys.argv),
                    datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                )
            )
        update_last_data(sys.argv[1], sys.argv[2], int(sys.argv[3]))

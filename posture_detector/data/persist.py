import os
import pandas as pd
import sqlite3


class SensorDB:
    con = None
    cur = None

    @staticmethod
    def init():
        if not SensorDB.cur:
            SensorDB.con = sqlite3.connect(os.environ['sensordbfile'])
            SensorDB.cur = SensorDB.con.cursor()
        SensorDB.cur.execute('''
            CREATE TABLE IF NOT EXISTS  sensor_data (
                datetime DATETIME , 
                trans text, 
                symbol text, 
                qty real, 
                price real
            )
        ''')

    @staticmethod
    def insert():
        SensorDB.cur.execute(f"""
            INSERT INTO sensor_data VALUES 
            ('2006-01-05','BUY','RHAT',100,35.14)
        """)
        SensorDB.con.commit()

    @staticmethod
    def get_latest():
        return False

    @staticmethod
    def get_all_as_df() -> pd.DataFrame:
        df = pd.read_sql_query(
            sql='SELECT * FROM sensor_data',
            con=SensorDB.con,
        )
        return df

    @staticmethod
    def finish():
        SensorDB.con.close()

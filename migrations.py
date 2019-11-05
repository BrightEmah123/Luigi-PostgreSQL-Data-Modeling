import psycopg2
import pandas as pd
from config.config import conn_config
from sql_queries.create_tables import create_sensor_tables
from sql_queries.insert_tables import insert_sensor_tables
from sql_queries.drop_tables import drop_sensor_tables

class ConnDB():
    def __init__(self):
        self.params = conn_config()
        self.connection = psycopg2.connect(**self.params)
        self.cur = self.connection.cursor()
        
    def fill_db(self, out_file):
        self.create_table()
        self.write_to_db()
        self.write_table_to_csv(out_file)
        
    
    def create_table(self):
        self.cur.execute(drop_sensor_tables)
        self.cur.execute(create_sensor_tables)
        self.connection.commit()
            
    def write_to_db(self):
        df = pd.read_csv('sample_dataset.csv')
        data_list = df.values.tolist()
        
        for row in data_list:
            count = int(row[4])
            for i in range(count):
                date = pd.to_datetime(row[0])
                date = date - pd.Timedelta(minutes=i)
                date_string = date.strftime('%Y-%m-%d %H:%M')
                device_id = int(row[1])
                sensor_id = int(row[2])
                reading = int(row[3])
                insert_lists = [date_string,device_id,sensor_id,reading]
                self.cur.execute(insert_sensor_tables,insert_lists)
                self.connection.commit()
        
    def write_table_to_csv(self, out_file):
        sql = 'SELECT * FROM SensorTable;'
        df = pd.read_sql_query(sql, self.connection)
        df.to_csv(out_file, index=False)
        
        self.connection.commit()
        
if __name__ == '__main__':
    sqlCreate = ConnDB()
    sqlCreate.fill_db('create-sql-db.csv')
        
import luigi
import pandas as pd
from migrations import ConnDB
from datetime import datetime
from sql_queries.create_tables import create_SensorsData
from sql_queries.drop_tables import drop_sensors_data_tables


# Luigi Task to populate a Sensor table with the data given in the sample dateset
class CreateDbFromCSV(luigi.Task):
    rundate = datetime.now().strftime('%Y-%m-%d__%H..%M..%S')
    out_file = 'sql-db__{}.csv'.format(str(rundate))
    
    """Since it is the first task in the graph, it does not require any dependencies to finish before running"""
    def requires(self):
        return []
    
    def output(self):
        return luigi.LocalTarget(self.out_file)
        
    def run(self):
        database = ConnDB()
        database.fill_db(self.out_file)
        

class FlattenSqlDB(luigi.Task):
    rundate = datetime.now().strftime('%Y-%m-%d__%H..%M..%S')
    out_file = 'output__{}.csv'.format(str(rundate))
    
    def requires(self):
        return [CreateDbFromCSV()]
    
    def output(self):
        return luigi.LocalTarget(self.out_file)
    
    def run(self):
        database = ConnDB()
        conn = database.connection
        self.generate_flat_sensor_table(conn)
        self.write_flat_table_to_csv(conn, self.out_file)
        
    @staticmethod
    def generate_flat_sensor_table(conn):
        with conn.cursor() as cursor:
            cursor.execute(drop_sensors_data_tables)
            cursor.execute(create_SensorsData)
        conn.commit()
        
    @staticmethod
    def write_flat_table_to_csv(conn, out_file):
        sql = 'SELECT * FROM SensorsData;'
        df = pd.read_sql_query(sql, conn)
        df.to_csv(out_file, index=False)
        
        conn.commit()

if __name__ == '__main__':
    # Call on the last Task in the graph
    luigi.run(["--local-scheduler"], main_task_cls=FlattenSqlDB)

    
# Insert Into SensorTable
insert_sensor_tables = '''
    INSERT INTO SensorTable(
        Time, DeviceID, SensorID, Reading)
            VALUES(%s, %s, %s, %s)
'''
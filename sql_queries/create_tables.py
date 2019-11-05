# Create SensorTable
create_sensor_tables = '''
    CREATE TABLE IF NOT EXISTS SensorTable(
        Time Timestamp NOT NULL,
        DeviceID integer NOT NULL,
        SensorID integer NOT NULL,
        Reading integer NOT NULL,
        PRIMARY KEY (Time, DeviceID, SensorID)
    );
'''
create_SensorsData = '''
    CREATE TABLE IF NOT EXISTS SensorsData(
        Time Timestamp NOT NULL,
        DeviceID integer NOT NULL,
        Sensor1Reading integer NOT NULL,
        Sensor2Reading integer NOT NULL,
        Sensor3Reading integer NOT NULL
    );
    SELECT S.Time, S.DeviceID, S.Reading as Sensor1Reading, T.Reading as Sensor2Reading, U.Reading as Sensor3Reading
        FROM (SELECT S.Time, S.DeviceID, S.Reading FROM SensorTable S WHERE S.SensorID = 1) as S,
                (SELECT S.Time, S.DeviceID, S.Reading FROM SensorTable S WHERE S.SensorID = 2) as T,
                    (SELECT S.Time, S.DeviceID, S.Reading FROM SensorTable S WHERE S.SensorID = 3) as U
        WHERE S.Time = T.Time and T.Time = U.Time and S.DeviceID = T.DeviceID and T.DeviceID = U.DeviceID;
'''
import pyodbc
import psycopg2


def connect_stage_dbb(self):
    conn = pyodbc.connect('Driver={SQL Server};'
                          'Server=10.6.43.12;'
                          'Database=SonyDBB;'
                          'UID=dbb;'
                          'PWD=ws5#VNd%jxz9;'
                          'Trusted connection=NO')
    cursor = conn.cursor()
    cursor.execute('SELECT top 1 * FROM SonyDBB.dbo.requestpayloadreceiver')
    for row in cursor:
        print(row)

# postgresDB

def connect_stage_postgres(self):
    conn = psycopg2.connect(user="supplychainstgdbing",
                            password="caTRIDEmiA",
                            host="10.6.40.101",
                            database="ingestor")
    cursor = conn.cursor()
    postgres_select = "SELECT * From public.watchfolder"
    cursor.execute(postgres_select)
    record = cursor.fetchone()
    for row in record:
        print(row)

import pyodbc
import psycopg2


def connect_stage_dbb():
    conn = pyodbc.connect('Driver={SQL Server};'
                             'Server=10.6.43.12;'
                          'Database=SonyDBB;'
                          'UID=dbb;'
                          'PWD=ws5#VNd%jxz9;'
                            'Trusted connection=NO')
    cursor = conn.cursor()
    cursor.execute('SELECT top 10 * FROM SonyDBB.dbo.title')
    for row in cursor:
        print(row)

connect_stage_dbb()
# -------------------------------------------------------------------------------
# postgresDB

def connect_stage_postgres():

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
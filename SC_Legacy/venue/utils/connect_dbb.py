import pyodbc
import psycopg2


def connect_stage_dbb():
    conn = pyodbc.connect('Driver={SQL Server};'
                      'Server=No;'
                      'Database=SonyDBB;'
                      'UID=dbb;'
                      'PWD=No'
                      'Trusted connection=NO')
    cursor = conn.cursor()
    cursor.execute('SELECT top 10 * FROM SonyDBB.dbo.title')

#    for row in cursor:
#    print(row)

# -------------------------------------------------------------------------------

# postgresDB


def connect_stage_postgres():
    conn = psycopg2.connect(user="",
                            password="",
                            host="ips",
                            database="ingestor")
    cursor = conn.cursor()
    postgres_Select = "SELECT * From public.watchfolder"
    cursor.execute(postgres_Select)
    record = cursor.fetchone()
    for row in record:
       print(record)

import psycopg2
import pandas.io.sql as psql

class BD(object):
    def __init__(self, dbname ="dw_blocketdb_ch", host="", password=""):
            self.dbname = dbname
            self.host = host
            self.password = password

    def query(self, query):
        print("starting database connection")
        conn = psycopg2.connect("dbname='"+self.dbname+"' user='bnbiuser' host="+self.host+" password="+self.password)
        print("sending query")
        df_sql = psql.read_sql(query, conn)
        print("query success")
        conn.close()
        return df_sql
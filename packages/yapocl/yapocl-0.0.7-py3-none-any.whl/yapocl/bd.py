import psycopg2
import pandas.io.sql as psql
from sshtunnel import open_tunnel

class bd(object):
    def __init__(self, ssh_host="", ssh_port=22, ssh_user="", ssh_password="", db_user="", db_password="", db_host="", db_port=5432, db_name=""):
        self.ssh_host = ssh_host
        self.ssh_port = ssh_port
        self.ssh_user = ssh_user
        self.ssh_password = ssh_password
        self.db_user = db_user
        self.db_password = db_password
        self.db_host = db_host
        self.db_port = db_port
        self.db_name = db_name

    def query(self, sql_query):
        with open_tunnel(
            self.ssh_host,
            ssh_port=self.ssh_port,
            ssh_username=self.ssh_user,
            ssh_password=self.ssh_password,
            remote_bind_address=(self.db_host, self.db_port),
            local_bind_address=('localhost', self.db_port)
        ):
            print("starting database connection")
            conn = psycopg2.connect("dbname='"+self.db_name+"' user='"+self.db_user+"' host=localhost password="+self.db_password)
            print("Sending query")
            df_sql = psql.read_sql(sql_query, conn)
            print("query success")
            conn.close()
            return df_sql
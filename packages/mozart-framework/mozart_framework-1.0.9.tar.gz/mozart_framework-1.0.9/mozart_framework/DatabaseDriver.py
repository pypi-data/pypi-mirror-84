# =============================================================
# =================     Library Import    =====================
# =============================================================

import mysql.connector
import psycopg2
import pyodbc


# =============================================================
# =================        Class          =====================
# =============================================================

# Classe de base de dados, um conector geral para todos as bases de dados
# Bases de dados configuradas: MYSQL, PostgreSQL


class DatabaseAutomator:
    conn = None
    cursor = None

    def __init__(self):
        nothing = None


    def connect_sqlserver(self, dbhost, dbname, username, password):
        self.conn = pyodbc.connect('Driver={SQL Server};'
                                   'Server=' + dbhost + ';'
                                                        'Database=' + dbname + ';'
                                                                               'uid=' + username + ';pwd=' + password + '')

        self.cursor = self.conn.cursor()

    def connect_mysql(self, dbhost, dbname, username, password):
        self.conn = mysql.connector.connect(
            host=dbhost,
            user=username,
            passwd=password,
            database=dbname
        )
        self.cursor = self.conn.cursor()

    def connect_postgres(self, dbhost, dbname, username, password):
        self.conn = psycopg2.connect(
            host=dbhost,
            user=username,
            password=password,
            database=dbname
        )
        self.cursor = self.conn.cursor()

    def insert_query(self, insertquery, value):
        self.cursor.execute(insertquery, value)
        self.conn.commit()
        print(self.cursor.rowcount, "was inserted.")

    def execute_query(self, query, value):
        self.cursor.execute(query, value)
        self.conn.commit()
        print(self.cursor.rowcount, "was changed.")

    def execute_query_no_values(self, query):
        self.cursor.execute(query)
        self.conn.commit()
        print(self.cursor.rowcount, "was changed.")

    def insert_many_query(self, insertquery, values):
        self.cursor.executemany(insertquery, values)
        self.conn.commit()

    def select_query(self, query):
        self.cursor.execute(query)
        myresult = self.cursor.fetchall()
        return myresult

    def close_db(self):
        self.conn.close()
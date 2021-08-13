import sqlite3
from sqlite3 import Error
from snap import sn_paths


ITEMS_TABLE_NAME = "CCItems"
EDGE_TYPE_TABLE_NAME = "EdgeTypes"
MAT_TYPE_TABLE_NAME = "MaterialTypes"
SLIDE_TYPE_TABLE_NAME = "SlideTypes"


def connect_db():
    try:
        conn = sqlite3.connect(sn_paths.DB_PATH)
    except Error as e:
        print(e)
        return{'FINISHED'}

    return conn


def query_db(SQL):
    try:
        conn = connect_db()
    except Error as e:
        print(e)
        return{'FINISHED'}

    cur = conn.cursor()
    cur.execute(SQL)
    rows = cur.fetchall()
    conn.close()

    return rows

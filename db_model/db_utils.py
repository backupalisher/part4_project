import psycopg2

from part4_project.env import *


def _query(q):
    print(q)
    con = psycopg2.connect(
        database=PART4_NAME,
        user=PART4_USER,
        password=PART4_PASS,
        host=HOST,
        port=DEFAULT_PORT
    )
    cur = con.cursor()
    try:
        cur.execute(q)
        data = cur.fetchall()
    except psycopg2.DatabaseError as err:
        print("Error: ", err)
    else:
        return data
    finally:
        con.commit()

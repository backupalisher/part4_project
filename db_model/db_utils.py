from django.db import connections


def _query(q):
    print('---------------')
    print(q)
    print('---------------')
    data = None
    with connections['part4'].cursor() as c:
        try:
            c.execute("BEGIN")
            c.execute(q)
            data = c.fetchall()
            c.execute("COMMIT")
            c.close()
        finally:
            c.close()
            return data

import psycopg2


def get_connection():
    return psycopg2.connect(host="localhost", dbname="postgres", user="postgres", password="2000", port=5432)


# conn = get_connection()
# cur = conn.cursor()

# cur.execute("""SELECT * FROM person WHERE age > 32""")

# print(cur.fetchone())

# conn.commit()
# cur.close()
# conn.close()
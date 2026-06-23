import psycopg2


def get_connection():
    return psycopg2.connect(host="localhost", dbname="postgres", user="postgres", password="2000", port=5432)

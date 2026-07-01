import psycopg2
from psycopg2.extensions import connection


def get_connection() -> connection:
    """Starts connection with DB"""
    return psycopg2.connect(host="localhost", dbname="postgres", user="postgres", password="2000", port=5432)


conn = get_connection()
cur = conn.cursor()
import psycopg2


def get_connection() -> None:
    """Starts connection with DB"""
    return psycopg2.connect(host="localhost", dbname="postgres", user="postgres", password="2000", port=5432)

import os

import mysql.connector
from mysql.connector import Error


def get_db_config():
    return {
        "host": os.getenv("MYSQL_HOST", "127.0.0.1"),
        "port": int(os.getenv("MYSQL_PORT", "3306")),
        "user": os.getenv("MYSQL_USER", "root"),
        "password": os.getenv("MYSQL_PASSWORD", ""),
        "database": os.getenv("MYSQL_DATABASE", "cognitive_load_db"),
    }


def get_db_connection():
    try:
        return mysql.connector.connect(**get_db_config())
    except Error as exc:
        print(f"MySQL connection unavailable: {exc}")
        return None

import psycopg2
from config import get_config

def connect():
    settings = get_config()
    return psycopg2.connect(**settings)

if __name__ == "__main__" :
    conn = connect()
    print("Connected to PhoneBook!")
    conn.close()
from getpass import getpass

def get_config():
    return{
        "host":"localhost",
        "port" : 5432,
        "database" : "phonebook",
        "user" : "postgres",
        "password" : getpass("PostgreSQL password: ")
    }
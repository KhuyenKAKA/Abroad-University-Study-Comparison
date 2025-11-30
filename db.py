import mysql.connector

def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="user",
        password="Tung@09092004",
        database="universities_db_clone"
    )

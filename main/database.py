import mysql.connector

def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",        # default XAMPP password is empty
        database="flowershop"
    )

import mysql.connector

conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="saurabh@123",
    database="health_db"
)
cursor = conn.cursor()
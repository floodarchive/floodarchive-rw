import mysql.connector

db = mysql.connector.connect(
    host = "localhost",
    user = "root",
    password = "",
    database = "floodarchive"
)

cursor = db.cursor(dictionary=True)

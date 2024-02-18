import pymysql.cursors
import json

host = "<paste end point here>"
user = "<master username>"
password = "<master password>"
database = "election" # do not change this

con = pymysql.connect(host = host, user = user,password=password, cursorclass=pymysql.cursors.DictCursor)
try:
    with con.cursor() as cursor:
        cursor.execute("CREATE DATABASE election;")
    con.commit()
    print("Database election created successfully")

finally:
    con.close()

def update_query(query):
    con = pymysql.connect(host = host, user = user,password=password, database = database,cursorclass=pymysql.cursors.DictCursor)

    try:
        with con.cursor() as cursor:
            cursor.execute(query)

        con.commit()

    finally:
        con.close()

update_query("CREATE TABLE voter (id SERIAL PRIMARY KEY,username VARCHAR(255) UNIQUE NOT NULL,password VARCHAR(255) NOT NULL,metamask_id VARCHAR(255) UNIQUE NOT NULL );")
print("Voter table successfully created")

update_query("CREATE TABLE candidates (candidate VARCHAR(255), description TEXT);")
print("Candidates table created successfully")

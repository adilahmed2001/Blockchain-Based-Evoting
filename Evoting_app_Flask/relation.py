import pymysql.cursors
import json

host = "<paste end point here>"
user = "<master username>"
password = "<master password>"
database = "election" # do not change this

def update_query(query):
    con = pymysql.connect(host = host, user = user,password=password, database = database,cursorclass=pymysql.cursors.DictCursor)

    try:
        with con.cursor() as cursor:
            cursor.execute(query)

        con.commit()

    finally:
        con.close()

def select_query(query):
    con = pymysql.connect(host = host, user = user,password=password, database = database,cursorclass=pymysql.cursors.DictCursor)
    try:
        with con.cursor() as cursor:
            cursor.execute(query)
            result = cursor.fetchall()
            return result

    finally:
        con.close()

def get_admin_credentials():
    with open('admin_credentials.json') as file:
        return json.load(file)

def get_voter_credentials(username):
    return select_query(f"select * from voter where username = '{username}';")

def add_user(username, password, metamask_id, phone_number):
    update_query(f"INSERT INTO voter (username, password, metamask_id, phone_number) VALUES ('{username}', '{password}', '{metamask_id}', '{phone_number}');")

def get_all_voters():
    return select_query("select * from voter where username <> 'admin';")

def get_candidates_description():
    return select_query("select * from candidates")

def add_candidate_description(candidate, description):
    return update_query(f"insert into candidates (candidate, description) values ('{candidate}', '{description}')")

def reset_database():
    update_query(f"DELETE FROM candidates;")
    update_query(f"DELETE FROM voter;")

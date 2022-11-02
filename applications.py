import email
from flask import Flask ,render_template,request,redirect
from flask_mail import Mail,Message
import os

import sqlite3
from sqlite3 import Error

app = Flask(__name__)

mail = Mail(app)

SPORTS = [
    "dodgeball",
    "cricket",
    "crossball",
    "games",
    "key"
]

def sql_connection(database):
    try:
        conn = sqlite3.connect(database)
        return conn
    except Error:
        print(Error)

def sql_table(conn,rows):
    cursorobj = conn.cursor()
    # create table
    conn.execute("CREATE TABLE IF NOT EXISTS registrants (id INTEGER,title TEXT NOT NULL,sport TEXT NOT NULL,PRIMARY KEY(id))")

    insertion = "INSERT INTO registrants (title,sport) VALUES(?,?);"
    cursorobj.executemany(insertion,REGISTRANTS)
    conn.commit()
    rows = cursorobj.execute('SELECT * FROM registrants')
    return rows

REGISTRANTS = []

@app.route("/")
def index():
    return render_template("index.html",sports=SPORTS)

@app.route("/register",methods=["POST"])
def register():
    name = request.form.get("email")
    if not name: 
        return render_template("error.html",message="missing email")
    sport = request.form.get("sport")
    if not sport:
        return render_template("error.html",message="missing sport")
    if sport not in SPORTS:
        return render_template("error.html",message="error sport")

    REGISTRANTS.append((name,sport))

    return redirect("/registrants")

@app.route("/registrants")

def registrants():
    database_name = "database.db"
    sqlite_conn = sql_connection(database_name)
    vijay = sql_table(sqlite_conn,REGISTRANTS)
    del REGISTRANTS[0]
    rows = vijay
    return render_template("registrants.html",rows_html=rows)
    
if __name__ == "__main__":
    app.run(debug=True)
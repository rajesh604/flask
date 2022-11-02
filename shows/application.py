from logging import debug
import sqlite3
from flask import Flask,render_template,request,jsonify
from sqlite3 import Error
app = Flask(__name__)

def sql_connection(database):
    try:
        conn = sqlite3.connect(database)
        return conn
    except Error:
        print(Error)

def sql_search(conn):
    cursorobj = conn.cursor()
    # k = [request.args.get("q")]
    shows = cursorobj.execute('SELECT * FROM shows WHERE title LIKE ?',[str(("%" + request.args.get("q") + "%"))])
    conn.commit()
    name = shows.fetchall()

    return name

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/search")
def search():
    database = sql_connection("shows.db")
    shows = sql_search(database)
    # return render_template("search.html",shows=shows)
    return jsonify(shows) # used to jsonify the ouput

if __name__ == "__main__":
    app.run(debug=True)
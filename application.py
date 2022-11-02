from flask import Flask,redirect,render_template,request,session
import flask
from flask_session import Session

app = Flask(__name__)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

@app.route("/")
def index():
    if not session.get("name"): # if there is no name in the session
        redirect("/login")
    return render_template("index1.html")

@app.route("/login",methods=["POST","GET"])
def login():
    if request.method == "POST":
        session["name"] = request.form.get("name")
        return redirect("/")

    return render_template("login.html")

@app.route("/logout")
def logout():
    session["name"] = None
    redirect("/")

if __name__ == "__main__":
    app.run(debug=True)

from flask import Flask, render_template

app = Flask(__name__)


@app.route("/home")
def home_screen():
    return render_template("index.html")


@app.route("/register", endpoint="register")
def signup_screen():
    return render_template("auth/register.html")


@app.route("/login")
def login():
    return render_template("auth/login.html")


@app.route("/logout")
def logout():
    return "Log Out!"


@app.route("/posting")
def posting_screen():
    return render_template("base.html")


@app.route("/commenting")
def commenting_screen():
    return render_template("base.html")


app.run(host="0.0.0.0", port=80)

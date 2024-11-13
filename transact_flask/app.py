from flask import Flask, render_template
import psycopg2

app = Flask(__name__)

# Connect to the database 
conn = psycopg2.connect(database="intro_project", user="postgres", password="transact", host="localhost", port="5432") 

# create a cursor 
cur = conn.cursor() 

# Insert some data into the table 
cur.execute( 
    '''INSERT INTO User (email, name, admin) VALUES \ 
    ('Jimmy@sandiego.edu', 'Jimmy',  TRUE), ('Humpfre@sandiego.edu', 'Humpfre', FALSE), ('Diego@sandiego.edu', 'Diego', FALSE);''') 
cur.execute( 
    '''INSERT INTO Post (contents, user_id, created_at) VALUES \ 
    ('What's your favorite color?', 1, '2024-11-13 01:01:01'), ('Anyone finish their project already?', 2, '2024-11-14 23:59:59');''') 
cur.execute( 
    '''INSERT INTO Comment (contents,, user_id, post_id, created_at) VALUES \ 
    ('Apple', 2, 1, '2024-11-13 01:02:03'), ('Blue', 3, 1, '2024-11-13 02:02:03'), 
    ('Nope', 3, 2, '2024-11-15 03:15:00'), ('RIP', 1, 2, '2024-11-15 09:30:40');''') 

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

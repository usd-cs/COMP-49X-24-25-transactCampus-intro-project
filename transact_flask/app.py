from flask import Flask, g, redirect, render_template, request, session, url_for
import psycopg2

def create_app(test_config=None):
    app = Flask(__name__)
            
    app.secret_key = "transact"  # Required for session management
    
    
    # Connect to the PostgreSQL database
    conn = psycopg2.connect(database="intro_project", user="postgres", password="!Peewee38!", host="localhost", port="5645")
    cur = conn.cursor()

    # Reset tables when restarting app
    cur.execute(
        '''DELETE FROM "Comment"'''
    )

    cur.execute(
        '''DELETE FROM "Post"'''
    )

    cur.execute(
        '''DELETE FROM "User"'''
    )

    # Insert data into the User table and fetch user_ids
    cur.execute(
        '''INSERT INTO "User" (email, name, admin, password) VALUES 
        ('Jimmy@sandiego.edu', 'Jimmy', TRUE, '1234') RETURNING id;'''
    )
    jimmy_id = cur.fetchone()[0]

    cur.execute(
        '''INSERT INTO "User" (email, name, admin, password) VALUES 
        ('Humpfre@sandiego.edu', 'Humpfre', FALSE, '1234') RETURNING id;'''
    )
    humpfre_id = cur.fetchone()[0]

    cur.execute(
        '''INSERT INTO "User" (email, name, admin, password) VALUES 
        ('Diego@sandiego.edu', 'Diego', FALSE, '1234') RETURNING id;'''
    )
    diego_id = cur.fetchone()[0]

    # Insert data into the Post table using fetched user_ids and fetch post_ids
    cur.execute(
        '''INSERT INTO "Post" (contents, user_id, created_at) VALUES 
        ('Whats your favorite color?', %s, '2024-11-13 01:01:01') RETURNING id;''',
        (jimmy_id,)
    )
    post1_id = cur.fetchone()[0]

    cur.execute(
        '''INSERT INTO "Post" (contents, user_id, created_at) VALUES 
        ('Anyone finish their project already?', %s, '2024-11-14 23:59:59') RETURNING id;''',
        (humpfre_id,)
    )
    post2_id = cur.fetchone()[0]

    # Insert data into the Comment table using fetched user_ids and post_ids
    cur.execute(
        '''INSERT INTO "Comment" (contents, user_id, post_id, created_at) VALUES 
        ('Apple', %s, %s, '2024-11-13 01:02:03'), 
        ('Blue', %s, %s, '2024-11-13 02:02:03'), 
        ('Nope', %s, %s, '2024-11-15 03:15:00'), 
        ('RIP', %s, %s, '2024-11-15 09:30:40');''',
        (humpfre_id, post1_id, diego_id, post1_id, diego_id, post2_id, jimmy_id, post2_id)
    )

    conn.commit()
    cur.close()
    conn.close()

    
    @app.route("/home")
    def home_screen():
        return render_template("home.html")

    @app.route("/comment")
    def comment():
        return render_template("comment.html")

    @app.route('/login', methods = ['GET', 'POST'])
    def login():
        if request.method == 'POST':
            session.pop('user_id', None)
            session.pop('email', None)
            session.pop('name', None)
            session.pop('admin', None)
            session.pop('password', None)
            
            email = request.form['email']
            password = request.form['password']
            print(email)
            
            conn = psycopg2.connect(database="intro_project", user="postgres", password="!Peewee38!", host="localhost", port="5645")
            cur = conn.cursor()
            cur.execute('SELECT id, email, name, admin, password FROM "User" WHERE email = %s AND password = %s', (email, password))
            user = cur.fetchone()
            conn.close()
            
            if user:
                session['user_id'] = user[0]
                session['email'] = user[1]
                session['name'] = user[2]
                session['admin'] = user[3]
                session['password'] = user[4]
                return redirect(url_for('home_screen'))
            
            return redirect(url_for('login'))
            
        return render_template("login.html")

    # Configurations or test config can be applied here if needed
    if test_config:
        app.config.from_mapping(test_config)

    return app

# Only run the app if this file is executed directly
if __name__ == "__main__":
    app = create_app()
    app.run(host="0.0.0.0", port=80)
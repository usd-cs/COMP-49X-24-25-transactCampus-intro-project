from flask import Flask, render_template
import psycopg2

def create_app(test_config=None):
    app = Flask(__name__)

    # Connect to the PostgreSQL database
    conn = psycopg2.connect(database="Intro_Project", user="postgres", password="!Peewee38!", host="localhost", port="5645")
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
        ('Jimmy@sandiego.edu', 'Jimmy', TRUE, '1234') RETURNING user_id;'''
    )
    jimmy_id = cur.fetchone()[0]

    cur.execute(
        '''INSERT INTO "User" (email, name, admin, password) VALUES 
        ('Humpfre@sandiego.edu', 'Humpfre', FALSE, '1234') RETURNING user_id;'''
    )
    humpfre_id = cur.fetchone()[0]

    cur.execute(
        '''INSERT INTO "User" (email, name, admin, password) VALUES 
        ('Diego@sandiego.edu', 'Diego', FALSE, '1234') RETURNING user_id;'''
    )
    diego_id = cur.fetchone()[0]

    # Insert data into the Post table using fetched user_ids and fetch post_ids
    cur.execute(
        '''INSERT INTO "Post" (contents, user_id) VALUES 
        ('Whats your favorite color?', %s) RETURNING post_id;''',
        (jimmy_id,)
    )
    post1_id = cur.fetchone()[0]

    cur.execute(
        '''INSERT INTO "Post" (contents, user_id) VALUES 
        ('Anyone finish their project already?', %s) RETURNING post_id;''',
        (humpfre_id,)
    )
    post2_id = cur.fetchone()[0]

    # Insert data into the Comment table using fetched user_ids and post_ids
    cur.execute(
        '''INSERT INTO "Comment" (contents, user_id, post_id) VALUES 
        ('Apple', %s, %s), 
        ('Blue', %s, %s), 
        ('Nope', %s, %s), 
        ('RIP', %s, %s);''',
        (humpfre_id, post1_id, diego_id, post1_id, diego_id, post2_id, jimmy_id, post2_id)
    )

    conn.commit()
    cur.close()
    conn.close()

    @app.route("/home")
    def home_screen():
        return render_template("main.html")

    @app.route("/comment")
    def comment():
        return render_template("comment.html")

    @app.route("/login")
    def login():
        return render_template("login.html")

    # Configurations or test config can be applied here if needed
    if test_config:
        app.config.from_mapping(test_config)

    return app

# Only run the app if this file is executed directly
if __name__ == "__main__":
    app = create_app()
    app.run(host="0.0.0.0", port=80)
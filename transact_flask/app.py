from flask import Flask, render_template
import psycopg2

def create_app(test_config=None):
    app = Flask(__name__)

    # Connect to the PostgreSQL database
    conn = psycopg2.connect(database="intro_project", user="postgres", password="transact", host="localhost", port="5432")
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
        return render_template("main.html")

    @app.route("/comment")
    def comment():
        return render_template("comment.html")

    @app.route("/login")
    def login():
        return render_template("login.html")
    
    @app.route("/delete_post/<int:post_id>", methods=["POST"])
    def delete_post(post_id):
        # Check if user is logged in and is an admin
        if "user_id" not in session or not session.get("admin", False):
            return redirect(url_for("login"))

        # Connect to the database and delete the post
        conn = get_db_connection()
        cur = conn.cursor()
        # Delete associated comments first to maintain referential integrity
        cur.execute("""DELETE FROM "Comment" WHERE post_id = %s;""", (post_id,))
        # Delete the post
        cur.execute("""DELETE FROM "Post" WHERE id = %s;""", (post_id,))
        conn.commit()
        cur.close()
        conn.close()

        # Redirect to the admin page after deletion
        return redirect(url_for("admin"))


    # Configurations or test config can be applied here if needed
    if test_config:
        app.config.from_mapping(test_config)

    return app

# Only run the app if this file is executed directly
if __name__ == "__main__":
    app = create_app()
    app.run(host="0.0.0.0", port=80)
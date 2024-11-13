from flask import Flask, render_template, request, redirect, url_for
import psycopg2
from datetime import datetime


def create_app(test_config=None):
    app = Flask(__name__)

    # Connect to the PostgreSQL database
    conn = psycopg2.connect(
        database="intro_project",
        user="postgres",
        password="8412",
        host="localhost",
        port="5432",
    )
    cur = conn.cursor()

    # Reset tables when restarting app
    cur.execute('''DELETE FROM "Comment"''')

    cur.execute('''DELETE FROM "Post"''')

    cur.execute('''DELETE FROM "User"''')

    # Insert data into the User table and fetch user_ids
    cur.execute(
        """INSERT INTO "User" (email, name, admin, password) VALUES \
        ('Jimmy@sandiego.edu', 'Jimmy', TRUE, '1234') RETURNING id;"""
    )
    jimmy_id = cur.fetchone()[0]

    cur.execute(
        """INSERT INTO "User" (email, name, admin, password) VALUES \
        ('Humpfre@sandiego.edu', 'Humpfre', FALSE, '1234') RETURNING id;"""
    )
    humpfre_id = cur.fetchone()[0]

    cur.execute(
        """INSERT INTO "User" (email, name, admin, password) VALUES \
        ('Diego@sandiego.edu', 'Diego', FALSE, '1234') RETURNING id;"""
    )
    diego_id = cur.fetchone()[0]

    # Insert data into the Post table using fetched user_ids and fetch post_ids
    cur.execute(
        """INSERT INTO "Post" (contents, user_id, created_at) VALUES \
        ('Whats your favorite color?', %s, '2024-11-13 01:01:01') RETURNING id;""",
        (jimmy_id,),
    )
    post1_id = cur.fetchone()[0]

    cur.execute(
        """INSERT INTO "Post" (contents, user_id, created_at) VALUES \
        ('Anyone finish their project already?', %s, '2024-11-14 23:59:59') RETURNING id;""",
        (humpfre_id,),
    )
    post2_id = cur.fetchone()[0]

    # Insert data into the Comment table using fetched user_ids and post_ids
    cur.execute(
        """INSERT INTO "Comment" (contents, user_id, post_id, created_at) VALUES \
        ('Apple', %s, %s, '2024-11-13 01:02:03'), 
        ('Blue', %s, %s, '2024-11-13 02:02:03'), 
        ('Nope', %s, %s, '2024-11-15 03:15:00'), 
        ('RIP', %s, %s, '2024-11-15 09:30:40');""",
        (
            humpfre_id,
            post1_id,
            diego_id,
            post1_id,
            diego_id,
            post2_id,
            jimmy_id,
            post2_id,
        ),
    )

    conn.commit()

    cur.close()
    conn.close()

    @app.route("/")
    def home():
        conn = get_db_connection()
        cur = conn.cursor()

        # Fetch posts with user names and any associated comments
        cur.execute("""
            SELECT p.id, p.contents, u.name, p.created_at
            FROM "Post" p
            JOIN "User" u ON p.user_id = u.id
            ORDER BY p.created_at DESC;
        """)
        posts = cur.fetchall()

        # Organize posts for template
        post_data = []
        for post in posts:
            post_id, content, user_name, created_at = post
            cur.execute(
                """
                SELECT c.contents, u.name
                FROM "Comment" c
                JOIN "User" u ON c.user_id = u.id
                WHERE c.post_id = %s
            """,
                (post_id,),
            )
            comments = cur.fetchall()
            post_data.append(
                {
                    "content": content,
                    "user_name": user_name,
                    "created_at": created_at,
                    "comments": [
                        {"content": c[0], "user_name": c[1]} for c in comments
                    ],
                }
            )

        cur.close()
        conn.close()
        return render_template("main.html", posts=post_data)

    @app.route("/add_post", methods=["POST"])
    def add_post():
        # Code to handle the new post
        content = request.form.get("content")
        user_id = 1  # Replace with actual user ID if applicable

        # Connect to the database and insert the new post
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute(
            """INSERT INTO "Post" (contents, user_id, created_at)
            VALUES (%s, %s, %s)""",
            (content, user_id, datetime.now()),
        )
        conn.commit()
        cur.close()
        conn.close()

        # Redirect to the home page to display the new post
        return redirect(url_for("home_screen"))

    @app.route("/public")
    def public_posts():
        conn = get_db_connection()
        cur = conn.cursor()

        # Fetch posts and their authors
        cur.execute("""
            SELECT p.id, p.contents, u.name, p.created_at
            FROM "Post" p
            JOIN "User" u ON p.user_id = u.id
            ORDER BY p.created_at DESC;
        """)
        posts = cur.fetchall()

        # Organize posts with comments
        post_data = []
        for post in posts:
            post_id, content, user_name, created_at = post
            # Fetch comments for each post
            cur.execute(
                """
                SELECT c.contents, u.name
                FROM "Comment" c
                JOIN "User" u ON c.user_id = u.id
                WHERE c.post_id = %s
            """,
                (post_id,),
            )
            comments = cur.fetchall()
            post_data.append(
                {
                    "content": content,
                    "user_name": user_name,
                    "created_at": created_at,
                    "comments": [
                        {"content": c[0], "user_name": c[1]} for c in comments
                    ],
                }
            )

        cur.close()
        conn.close()
        return render_template("public_posts.html", posts=post_data)

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


def get_db_connection():
    conn = psycopg2.connect(
        database="intro_project",
        user="postgres",
        password="8412",
        host="localhost",
        port="5432",
    )
    return conn


# Only run the app if this file is executed directly
if __name__ == "__main__":
    app = create_app()
    app.run(host="0.0.0.0", port=80)

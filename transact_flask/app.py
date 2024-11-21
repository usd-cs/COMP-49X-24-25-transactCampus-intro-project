from flask import Flask, g, redirect, render_template, request, session, url_for
from sqlalchemy import (
    create_engine,
    Column,
    Integer,
    String,
    Boolean,
    Text,
    ForeignKey,
    TIMESTAMP,
)

# from bcrypt import hashpw, gensalt
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
import psycopg2
from datetime import datetime
import base64

Base = declarative_base()


# User model
class User(Base):
    __tablename__ = "User"
    id = Column(Integer, primary_key=True, autoincrement=True)
    email = Column(String, nullable=False)
    name = Column(String, nullable=False)
    admin = Column(Boolean, default=False)
    password = Column(String, nullable=False)

    # Relationship to posts and comments
    posts = relationship("Post", back_populates="user", cascade="all, delete")
    comments = relationship("Comment", back_populates="user", cascade="all, delete")


# Post model
class Post(Base):
    __tablename__ = "Post"
    id = Column(Integer, primary_key=True, autoincrement=True)
    contents = Column(Text, nullable=False)
    user_id = Column(
        Integer, ForeignKey("User.id", ondelete="NO ACTION"), nullable=False
    )
    created_at = Column(TIMESTAMP, nullable=False)

    # Relationship to user and comments
    user = relationship("User", back_populates="posts")
    comments = relationship("Comment", back_populates="post", cascade="all, delete")


# Comment model
class Comment(Base):
    __tablename__ = "Comment"
    id = Column(Integer, primary_key=True, autoincrement=True)
    contents = Column(Text, nullable=False)
    user_id = Column(
        Integer, ForeignKey("User.id", ondelete="NO ACTION"), nullable=False
    )
    post_id = Column(
        Integer, ForeignKey("Post.id", ondelete="NO ACTION"), nullable=False
    )
    created_at = Column(TIMESTAMP, nullable=False)

    # Relationships to user and post
    user = relationship("User", back_populates="comments")
    post = relationship("Post", back_populates="comments")


def create_app(test_config=None):
    app = Flask(__name__)

    DATABASE_URL = "postgresql://postgres:!Peewee38!@localhost:5645/intro_project"

    engine = create_engine(DATABASE_URL)
    Base.metadata.create_all(engine)  # Creates the tables

    DB = sessionmaker(bind=engine)
    db = DB()

    app.secret_key = "transact"

    # Connect to the PostgreSQL database

    # Encrypt passwords
    password1 = encrypt_password("007")
    password2 = encrypt_password("hello")
    password3 = encrypt_password("transact")

    # Add users
    jimmy = User(
        email="Jimmy@sandiego.edu", name="Jimmy", admin=True, password=password1
    )
    humpfre = User(
        email="Humpfre@sandiego.edu", name="Humpfre", admin=False, password=password2
    )
    diego = User(
        email="Diego@sandiego.edu", name="Diego", admin=False, password=password3
    )

    db.add_all([jimmy, humpfre, diego])
    db.commit()

    # Fetch user IDs
    jimmy_id = jimmy.id
    humpfre_id = humpfre.id
    diego_id = diego.id

    # Add posts
    post1 = Post(
        contents="Whats your favorite color?",
        user_id=jimmy_id,
        created_at=datetime(2024, 11, 13, 1, 1, 1),
    )
    post2 = Post(
        contents="Anyone finish their project already?",
        user_id=humpfre_id,
        created_at=datetime(2024, 11, 12, 23, 59, 59),
    )

    db.add_all([post1, post2])
    db.commit()

    # Fetch post IDs
    post1_id = post1.id
    post2_id = post2.id

    # Add comments
    comment1 = Comment(
        contents="Apple",
        user_id=humpfre_id,
        post_id=post1_id,
        created_at=datetime(2024, 11, 13, 1, 2, 3),
    )
    comment2 = Comment(
        contents="Blue",
        user_id=diego_id,
        post_id=post1_id,
        created_at=datetime(2024, 11, 13, 2, 2, 3),
    )
    comment3 = Comment(
        contents="Nope",
        user_id=diego_id,
        post_id=post2_id,
        created_at=datetime(2024, 11, 15, 3, 15, 0),
    )
    comment4 = Comment(
        contents="RIP",
        user_id=jimmy_id,
        post_id=post2_id,
        created_at=datetime(2024, 11, 15, 9, 30, 40),
    )

    db.add_all([comment1, comment2, comment3, comment4])
    db.commit()

    @app.route("/")
    def home():
        posts = db.query(Post).join(User).order_by(Post.created_at.desc()).all()

        post_data = []
        for post in posts:
            comments = (
                db.query(Comment)
                .join(User)
                .filter(Comment.post_id == post.id)
                .order_by(Comment.created_at.desc())
                .all()
            )
            post_data.append(
                {
                    "id": post.id,
                    "content": post.contents,
                    "user_name": post.user.name,
                    "created_at": post.created_at,
                    "comments": [
                        {"content": c.contents, "user_name": c.user.name}
                        for c in comments
                    ],
                }
            )
        return render_template("home.html", posts=post_data)

    @app.route("/admin")
    def admin():
        posts = db.query(Post).join(User).order_by(Post.created_at.desc()).all()

        post_data = []
        for post in posts:
            comments = (
                db.query(Comment)
                .join(User)
                .filter(Comment.post_id == post.id)
                .order_by(Comment.created_at.desc())
                .all()
            )
            post_data.append(
                {
                    "id": post.id,
                    "content": post.contents,
                    "user_name": post.user.name,
                    "created_at": post.created_at,
                    "comments": [
                        {"id": c.id, "content": c.contents, "user_name": c.user.name}
                        for c in comments
                    ],
                }
            )
        return render_template("admin.html", posts=post_data)

    @app.route("/add_post", methods=["POST"])
    def add_post():
        content = request.form.get("content")
        user_id = session.get("user_id")

        if user_id:
            new_post = Post(
                contents=content, user_id=user_id, created_at=datetime.now()
            )
            db.add(new_post)
            db.commit()

            return redirect(
                url_for("admin") if session.get("admin") else url_for("home")
            )
        return redirect(url_for("login"))

    @app.route("/delete_post/<int:post_id>", methods=["POST"])
    def delete_post(post_id):
        if not session.get("admin"):
            return redirect(url_for("home"))

        post = db.query(Post).get(post_id)
        if post:
            db.delete(post)
            db.commit()
        return redirect(url_for("admin"))

    @app.route("/delete_comment/<int:comment_id>", methods=["POST"])
    def delete_comment(comment_id):
        if not session.get("admin"):
            return redirect(url_for("home"))

        comment = db.query(Comment).get(comment_id)
        if comment:
            db.delete(comment)
            db.commit()
        return redirect(url_for("admin"))

    @app.route("/public")
    def public_posts():
        posts = db.query(Post).join(User).order_by(Post.created_at.desc()).all()

        post_data = []
        for post in posts:
            comments = (
                db.query(Comment).join(User).filter(Comment.post_id == post.id).all()
            )
            post_data.append(
                {
                    "content": post.contents,
                    "user_name": post.user.name,
                    "created_at": post.created_at,
                    "comments": [
                        {"content": c.contents, "user_name": c.user.name}
                        for c in comments
                    ],
                }
            )
        return render_template("public_posts.html", posts=post_data)

    @app.route("/comment/<int:post_id>")
    def comment(post_id):
        # Pass the post_id to the template for form submission
        return_to = request.args.get("return_to", "home")
        return render_template("comment.html", post_id=post_id, return_to=return_to)

    @app.route("/add_comment", methods=["POST"])
    def add_comment():
        content = request.form.get("content")
        post_id = request.form.get("post_id")
        user_id = session.get("user_id")

        if user_id:
            new_comment = Comment(
                contents=content,
                user_id=user_id,
                post_id=post_id,
                created_at=datetime.now(),
            )
            db.add(new_comment)
            db.commit()

            return redirect(
                url_for("admin") if session.get("admin") else url_for("home")
            )
        return redirect(url_for("login"))

    @app.route("/login", methods=["GET", "POST"])
    def login():
        if request.method == "POST":
            session.clear()

            email = request.form["email"]
            password = request.form["password"]

            user = (
                db.query(User)
                .filter_by(email=email, password=encrypt_password(password))
                .first()
            )
            if user:
                session["user_id"] = user.id
                session["email"] = user.email
                session["name"] = user.name
                session["admin"] = user.admin

                return redirect(url_for("admin") if user.admin else url_for("home"))
            return redirect(url_for("login"))
        return render_template("login.html")

    # Configurations or test config can be applied here if needed
    if test_config:
        app.config.update(test_config)

    return app


def get_db_connection():
    DATABASE_URL = "postgresql://postgres:!Peewee38!@localhost:5645/intro_project"

    engine = create_engine(DATABASE_URL)
    Base.metadata.create_all(engine)  # Creates the tables

    DB = sessionmaker(bind=engine)
    db = DB()
    return db


def get_mock_db_connection():
    conn = psycopg2.connect(app.config["DATABASE_URI"])
    return conn


def encrypt_password(password: str) -> str:
    # Encrypt password (encode it in base64)
    encoded = base64.urlsafe_b64encode(password.encode()).decode()
    return encoded


# Only run the app if this file is executed directly
if __name__ == "__main__":
    app = create_app()
    app.run(host="0.0.0.0", port=80)

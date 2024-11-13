from flask import Blueprint, request, jsonify, redirect, url_for, current_app
from app import db, Post  # Import `Post` model and `db` from `app.py`

posting_blueprint = Blueprint("posting", __name__)


@posting_blueprint.route("/add_post", methods=["POST"])
def add_post():
    data = request.get_json()
    content = data.get("content")

    if content:
        new_post = Post(author="User", content=content)
        db.session.add(new_post)
        db.session.commit()

        # Return the new post data as JSON
        return jsonify(
            success=True, post={"author": new_post.author, "content": new_post.content}
        )
    else:
        return jsonify(success=False, error="No content provided")

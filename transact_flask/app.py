from flask import Flask, render_template


def create_app(test_config=None):
    
    app = Flask(__name__)
    
    @app.route("/home")
    def home_screen():
        return render_template("main.html")

    @app.route("/comment")
    def logout():
        return render_template("comment.html")

    @app.route("/login")
    def login():
        return render_template("login.html")

    app.run(host="0.0.0.0", port=80)

    return app

var = create_app()
var.run()
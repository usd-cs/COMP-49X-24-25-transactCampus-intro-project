from flask import Flask, render_template

def create_app(test_config=None):
    app = Flask(__name__)

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
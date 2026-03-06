import os
from flask import Flask, render_template, request


def create_app(test_config=None):

    app = Flask(__name__, instance_relative_config=True)
    app.logger.setLevel(20) # Set logger to INFO or higher

    app.config.from_mapping(
        SECRET_KEY="dev",
        DATABASE=os.path.join(app.instance_path, "flaskr.sqlite"),
    )

    if test_config is None:
        app.config.from_pyfile("config.py", silent=True)
    else:
        app.config.from_mapping(test_config)

    os.makedirs(app.instance_path, exist_ok=True)


    @app.route('/')
    def index(name=None, ongoingEvents=[1, 2, 3]):
        return render_template("index.html", person=name, ongoingEvents=ongoingEvents)


    @app.route('/login', methods=['POST', 'GET'])
    def login():
        error: str = ""
        if request.method == 'POST':
            if valid_login(request.form['username'],
                        request.form['password']):
                return log_the_user_in(request.form['username'])
            else:
                error = "Invalid username/password"
                
        return render_template('login.html', error=error)

    from . import db, auth
    db.init_app(app)
    app.register_blueprint(auth.bp)


    return app

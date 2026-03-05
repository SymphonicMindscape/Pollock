from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def index(name=None):
    return render_template("Index.html", person=name)


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
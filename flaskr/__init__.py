from flask import Flask, render_template, request


app = Flask(__name__)
app.logger.setLevel(20) # Set logger to INFO or higher

@app.route('/')
def index(name=None, ongoingEvents=[]):
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
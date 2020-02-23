from flask import Flask, render_template

app = Flask(__name__)


@app.route('/register')
def register():
    return render_template('register.html')


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/lab')
def search():
    return render_template('lab.html')


@app.route('/<code>')
def code(code):
    return render_template('code.html')


@app.route('/home/<username>')
def home(username):
    return render_template('home.html')


@app.route('/login')
def login():
    return render_template('login.html')


@app.route('/home/<username>/check_code')
def check_code(username):
    return render_template('check_code.html')


@app.route('/home/<username>/change')
def change(username):
    return render_template('change.html')


if __name__ == '__main__':
    app.run(debug=True)

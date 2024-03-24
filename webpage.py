from flask import Flask, render_template, request, redirect, url_for
import aws_controller
import dynoTest

app = Flask(__name__)

# Dummy user data for demonstration purposes

users = {'email': 'password',
         'Admin': 'P1'}

@app.route('/')
def home():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login():

    #aws_controller.get_items()
    email = request.form['email']
    password = request.form['password']

    p = dynoTest.checkLoginDetails(email,password)

    if p:
        return redirect(url_for('success'))
    else:
        return render_template('login.html', error=True)

@app.route('/success')
def success():
    return 'Login successful!'

@app.route('/failure')
def failure():
    return 'Login failed!'

if __name__ == '__main__':
    app.run(debug=True, port=80)

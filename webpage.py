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

@app.route('/login', methods=['GET', 'POST'])
def login():

    #print(request.form['action'])
    if request.method == 'GET':
        return render_template('login.html')
    else:
        if request.form['action'] == 'Register':
            return redirect(url_for('register'))
        #aws_controller.get_items()
        email = request.form['email']
        password = request.form['password']

        p = dynoTest.checkLoginDetails(email,password)

        if p:
            return redirect(url_for('success'))
        else:
            return render_template('login.html', error=True)
        

@app.route('/register', methods=['GET','POST'])
def register():

    #print(request.form['action'])

    if request.method == 'GET':
        return render_template('register.html')
    
    if request.form['action'] == 'Login':
        return redirect(url_for('login'))
    elif request.form['action'] == 'Register':
        email = request.form['email']
        password = request.form['password']
        username = request.form['username']
        p = dynoTest.addUser(email,username,password)
        print(p)
        if p:
            return redirect(url_for('login'))
        else:
            return render_template('register.html',error=True)


@app.route('/success')
def success():
    return 'Login successful!'

@app.route('/failure')
def failure():
    return 'Login failed!'

if __name__ == '__main__':
    app.run(debug=True, port=80)

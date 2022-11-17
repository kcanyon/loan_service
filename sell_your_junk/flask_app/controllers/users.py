from flask import render_template, session, redirect, request, flash
from flask_app import app
from flask_app.models.user import User
from flask_bcrypt import Bcrypt
import re

bcrypt = Bcrypt(app)

@app.route('/')
def login_register():
    return render_template('login_registration.html')

# process for user login
@app.route('/login', methods=['POST'])
def login():
    data = {"email": request.form['email']}
    user = User.get_by_email(data)
    if not user:
        flash ("User could not be found with the associated email or password", "login")
        return redirect('/')
    if not bcrypt.check_password_hash(user.password,request.form['password']):
        flash ("Invalid Email or Password", "login")
        return redirect('/')
    session['user_id'] = user.id
    return redirect('/items/dashboard')

# process for user registration
@app.route('/register', methods=['POST'])
def register():
    data = {
        "first_name": request.form["first_name"],
        "last_name": request.form["last_name"],
        "email": request.form["email"],
        "password": request.form["password"],
        "confirm_password": request.form["confirm_password"]
    }
    if User.validate_registration(data):
        pw_hash = bcrypt.generate_password_hash(request.form['password'])
        data['pw_hash'] = pw_hash
        user = User.create_user(data)
        session['user_id'] = user
        print('Success!')
        return redirect('/items/dashboard')
    else:
        return redirect('/')

# logout user
@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')
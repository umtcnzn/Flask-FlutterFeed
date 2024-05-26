from flask import request, jsonify,render_template,flash,session,redirect,url_for
from models.user import User
from sirope import *
from bcrypt import hashpw,checkpw,gensalt

s = Sirope()
def login():
    try:
        if request.method == 'POST':
            username = request.form['username']
            password = request.form['password']

            user:User = s.find_first(User, lambda u: u.username == username)
            if not user:
                flash('Invalid username or password', 'danger')
                return redirect(url_for('auth_routes.login'))
            
            if not checkpw(password.encode('utf-8'), user.password.encode('utf-8')):
                flash('Invalid username or password', 'danger')
                return redirect(url_for('auth_routes.login'))
            
            session['user'] = user.to_dict()
            flash('Login successful', 'success')
            return redirect(url_for('html_routes.home'))
        
        if 'user' in session:
            return redirect(url_for('html_routes.home'))
        
        return render_template('login.html')
    except Exception as e:
        flash(f"An error occurred: {str(e)}", "danger")
        return redirect(url_for('html_routes.home'))


def register():
    try:
        if request.method == 'POST':
            name = request.form['name']
            username = request.form['username']
            email = request.form['email']
            password = request.form['password']

            existing_user = s.find_first(User, lambda u: u.username == username or u.email == email)
                
            if existing_user:
                flash('Username or email already exists!', 'danger')
                return redirect(url_for('auth_routes.register'))
            else:
                hashedPassword = hashpw(password.encode('utf-8'), gensalt()).decode('utf-8')
                user = User(name, username, email, password=hashedPassword)
                s.save(user)
                flash('Registration successful!', 'success')
                return redirect(url_for('auth_routes.login'))
            
        if 'user' in session:
            return redirect(url_for('html_routes.home'))
        
        return render_template('register.html')
    except Exception as e:
        flash(f"An error occurred: {str(e)}", "danger")
        return redirect(url_for('html_routes.home'))


def logout():
    try:
        if not 'user' in session:
            return redirect(url_for('auth_routes.login'))
        session.pop('user', None)
        flash('Logout successful!', 'success')
        return redirect(url_for('auth_routes.login'))
    except Exception as e:
        flash(f"An error occurred: {str(e)}", "danger")
        return redirect(url_for('html_routes.home'))

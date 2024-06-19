from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from app import bcrypt, mongo
from app.forms import LoginForm, RegistrationForm, ComposeForm
from app.models import User
from bson.objectid import ObjectId

main = Blueprint('main', __name__)

@main.route('/')
def home():
    if current_user.is_authenticated:
        return redirect(url_for('main.inbox'))
    return redirect(url_for('main.login'))

@main.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        user_data = mongo.db.users.find_one({'email': email})
        if user_data and bcrypt.check_password_hash(user_data['password'], password):
            user = User(email=user_data['email'], password=user_data['password'], _id=str(user_data['_id']))
            login_user(user)
            flash('Login successful!', 'success')
            return redirect(url_for('main.inbox'))
        else:
            flash('Invalid email or password', 'danger')
    return render_template('login.html', form=form)

@main.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = {
            'email': form.email.data,
            'password': hashed_password
        }
        mongo.db.users.insert_one(user)
        flash('Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('main.login'))
    return render_template('register.html', form=form)

@main.route('/compose', methods=['GET', 'POST'])
@login_required
def compose():
    form = ComposeForm()
    if form.validate_on_submit():
        email = {
            'from': current_user.email,
            'to': form.to.data,
            'subject': form.subject.data,
            'body': form.body.data,
            'timestamp': request.form.get('timestamp')
        }
        mongo.db.emails.insert_one(email)
        flash('Email sent!', 'success')
        return redirect(url_for('main.inbox'))
    return render_template('compose.html', form=form)

@main.route('/inbox')
@login_required
def inbox():
    emails = mongo.db.emails.find({'to': current_user.email})
    return render_template('inbox.html', emails=emails)

@main.route('/sent')
@login_required
def sent():
    emails = mongo.db.emails.find({'from': current_user.email})
    return render_template('sent.html', emails=emails)

@main.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('main.login'))

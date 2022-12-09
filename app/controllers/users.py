from flask import Flask, render_template, request, redirect, Blueprint,session
from app.models.users import User
import pdb

users = Blueprint('users', __name__, template_folder='templates')


@users.route('/')
def landing_page():
    username = ''
    if session['user'] == None:
        log = 'login'
    else:
        username = session['user']['name']
        log = 'logout'
    return render_template('create.html', log = log, username = username)

@users.route('/welcome')
def welcome_user():
    if session['user'] == None:
        return redirect('/')
    
    username = session['user']['name']
    log = 'logout'
    return render_template('welcome.html', username = username, log = log)

@users.route('/register',methods=["POST"])
def register_user():
    if not User.email_free(request.form):
        return redirect('/')
    if not User.validate_user(request.form):
        return redirect('/')
    
    session['user']  = User.create_new(request.form)
    
    return redirect('/welcome')


@users.route('/login',methods=["POST"])
def login():
    
    user_login = User.login(request.form)
    if user_login != False:
        session['user'] = user_login
    else:
        return redirect('/')
    return redirect('/welcome')

@users.route('/log')
def logout():
    session['user'] = None
    return redirect('/')
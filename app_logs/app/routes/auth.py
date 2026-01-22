from flask import Blueprint, render_template, request, redirect, session, url_for
from app import db, logreader
from app.models.applogs import User
from app.utils import string_hash, registered, get_role

auth_bp = Blueprint('auth', __name__, template_folder='../templates')

#login and logout pages
@auth_bp.route('/login')
def login():
    return render_template('login.html')

@auth_bp.route('/auth', methods=['GET', 'POST'])
def auth():
    if request.method == 'POST':

        username = request.form['username']
        passwd = request.form['passwd']

        is_registered, err_msg = registered(username, passwd)
        if is_registered:

            user = User.query.filter_by(username=username).first()

            session['loggedin'] = True
            session['id'] = user.id
            session['username'] = username
            session['rights'] = user.rights
            session['role'] = get_role(user.rights)

            return redirect(url_for('auth.index'))
        else:
            return render_template('login.html', err=err_msg)

    if session.get('loggedin'):
        return redirect(url_for('auth.index'))
    return redirect(url_for('auth.login'))

@auth_bp.route('/logout')
def logout():
    session.pop('loggedin', None)
    session.pop('id', None)
    session.pop('username', None)
    session.pop('rights', None)
    session.pop('role', None)
    return redirect(url_for('auth.login'))

# homepage
@auth_bp.route('/')
def index():
    if session.get('loggedin'):
        return render_template("index.html", table="void")
    return redirect(url_for('auth.login'))
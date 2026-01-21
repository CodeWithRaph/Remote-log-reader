from flask import Blueprint, render_template, request, redirect, session, abort, url_for
from app import db, logreader
from app.models.applogs import Privilege, Role, User, Machine, Log
from app.utils import string_hash, registered, get_role, get_privileges, ip_valide

user_bp = Blueprint('user', __name__, template_folder='../templates')

# users pages
@user_bp.route('/users', methods=['GET'])
def users():
    allowed_session = session.get('loggedin') and session.get('role') == 'Administrateur'

    if allowed_session:
        user = db.session.query(User, Role).join(Role, User.rights == Role.privileges).all()
        table_privilege = get_privileges(Role.query.all())
        return render_template("users.html", table=table_privilege, roles=Role.query.all(), liste=user)
    return abort(403)

@user_bp.route('/selected-user', methods=['POST'])
def selectedUser():
    allowed_session = session.get('loggedin') and session.get('role') == 'Administrateur'

    if allowed_session:
        if request.method == 'POST':
            id = request.form['user_id']

            if request.form['action'] == "edit":
                return redirect(url_for('user.editUsers', id=id))
            elif request.form['action'] == "delete":
                return redirect(url_for('user.deleteUser', id=id))
    return abort(403)

@user_bp.route('/users/edit/<id>', methods=['GET'])
def editUsers(id):
    allowed_session = session.get('loggedin') and session.get('role') == 'Administrateur'

    if allowed_session:
        user = User.query.get(id)
        u_role = get_role(user.rights)

        if user != None:
            return render_template('edit-user.html', user=user, user_role=u_role ,roles=Role.query.all())
        else:
            err_msg = "L'utilisateur demandé n'existe pas."
            return render_template('err.html', err=err_msg)
    return abort(403)

@user_bp.route('/edit-user', methods=['POST'])
def editingUser():
    allowed_session = session.get('loggedin') and session.get('role') == 'Administrateur'

    if allowed_session:
        if request.method == 'POST':
            edited, err_msg = User.edit_user(request.form['user_id'], request.form['username'], request.form['role'])
            if edited:
                return redirect(url_for('user.users'))
            else:
                return render_template('err.html', err=err_msg)
    return abort(403)

@user_bp.route('/users/delete/<id>', methods=['GET'])
def deleteUser(id):
    allowed_session = session.get('loggedin') and session.get('role') == 'Administrateur'

    if allowed_session:
        deleted, err_msg = User.remove_user(id)
        if deleted:
            return redirect(url_for('user.users'))
        else:
            return render_template('err.html', err=err_msg)
    return abort(403)

@user_bp.route('/add-user', methods=['POST'])
def addUser():
    allowed_session = session.get('loggedin') and session.get('role') == 'Administrateur'

    if allowed_session:
        if request.method == 'POST':
            added, err_msg = User.add_user(request.form['username'], request.form['passwd'], request.form['passwd2'], request.form['role'])
            if added:
                return redirect(url_for('user.users'))
            else:
                return render_template('err.html', err=err_msg)
    return abort(403)
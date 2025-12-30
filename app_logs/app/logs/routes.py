from flask import Blueprint, render_template, request, redirect, session, abort, url_for
from app import db, logreader
from app.models.applogs import Privilege, Role, User, Machine, Log
from app.utils import string_hash, registered, get_role, get_privileges, ip_valide

log_bp = Blueprint('log', __name__, template_folder='../templates')

#login and logout pages
@log_bp.route('/login')
def login():
    return render_template('login.html')

@log_bp.route('/auth', methods=['GET', 'POST'])
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

            return redirect(url_for('log.index'))
        else:
            return render_template('login.html', err=err_msg)

    if session.get('loggedin'):
        return redirect(url_for('log.index'))
    return redirect(url_for('log.login'))

@log_bp.route('/logout')
def logout():
    session.pop('loggedin', None)
    session.pop('id', None)
    session.pop('username', None)
    session.pop('rights', None)
    session.pop('role', None)
    return redirect(url_for('log.login'))

# homepage
@log_bp.route('/')
def index():
    if session.get('loggedin'):
        return render_template("index.html", table="void")
    return redirect(url_for('log.login'))

# machines pages
@log_bp.route('/machines', methods=['GET'])
def machines():
    allowed_session = session.get('loggedin') and session.get('role') in ('Gestionnaire', 'Administrateur')

    if allowed_session:
        return render_template("machines.html", table=Machine.query.all(), session_role=session.get('role'))
    return abort(403)

@log_bp.route('/selected-machine', methods=['POST'])
def selectedMachine():
    allowed_session = session.get('loggedin') and session.get('role') in ('Gestionnaire', 'Administrateur')

    if allowed_session:
        if request.method == 'POST':
            id = request.form['host_id']

            if request.form['action'] == "edit":
                return redirect(url_for('log.editMachine', id=id))
            elif request.form['action'] == "delete":
                return redirect(url_for('log.deleteMachine', id=id))
    return abort(403)

@log_bp.route('/machines/edit/<id>', methods=['GET'])
def editMachine(id):
    allowed_session = session.get('loggedin') and session.get('role') in ('Gestionnaire', 'Administrateur')

    if allowed_session:
        machine = Machine.query.get(id)
        if machine != None:
            return render_template('edit-machine.html', machine=machine)
        else:
            err_msg = "La machine demandée n'existe pas."
            return render_template('err.html', err=err_msg)
    return abort(403)

@log_bp.route('/edit-machine', methods=['POST'])
def editingMachine():
    allowed_session = session.get('loggedin') and session.get('role') in ('Gestionnaire', 'Administrateur')

    if allowed_session:
        if request.method == 'POST':
            edited, err_msg = Machine.edit_machine(request.form['host_id'], request.form['host'], request.form['ip'])

            if edited:
                return redirect(url_for('log.machines'))
            else:
                return render_template('err.html', err=err_msg)
    return abort(403)

@log_bp.route('/machines/delete/<id>', methods=['GET'])
def deleteMachine(id):
    allowed_session = session.get('loggedin') and session.get('role') in ('Gestionnaire', 'Administrateur')

    if allowed_session:
        if Machine.remove_machine(id):
            return redirect(url_for('log.machines'))
        else:
            err_msg = "La machine demandée n'existe pas."
            return render_template('err.html', err=err_msg)
    return abort(403)

@log_bp.route('/add-machine', methods=['POST'])
def addMachine():
    allowed_session = session.get('loggedin') and session.get('role') in ('Gestionnaire', 'Administrateur')

    if allowed_session:
        if request.method == 'POST':
            added, err_msg = Machine.add_machine(request.form['host'], request.form['ip'])
            if added:
                return redirect(url_for('log.machines'))
            else:
                return render_template('err.html', err=err_msg)
    return abort(403)

# users pages
@log_bp.route('/users', methods=['GET'])
def users():
    allowed_session = session.get('loggedin') and session.get('role') == 'Administrateur'

    if allowed_session:
        user = db.session.query(User, Role).join(Role, User.rights == Role.privileges).all()
        table_privilege = get_privileges(Role.query.all())
        return render_template("users.html", table=table_privilege, roles=Role.query.all(), liste=user)
    return abort(403)

@log_bp.route('/selected-user', methods=['POST'])
def selectedUser():
    allowed_session = session.get('loggedin') and session.get('role') == 'Administrateur'

    if allowed_session:
        if request.method == 'POST':
            id = request.form['user_id']

            if request.form['action'] == "edit":
                return redirect(url_for('log.editUsers', id=id))
            elif request.form['action'] == "delete":
                return redirect(url_for('log.deleteUser', id=id))
    return abort(403)

@log_bp.route('/users/edit/<id>', methods=['GET'])
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

@log_bp.route('/edit-user', methods=['POST'])
def editingUser():
    allowed_session = session.get('loggedin') and session.get('role') == 'Administrateur'

    if allowed_session:
        if request.method == 'POST':
            edited, err_msg = User.edit_user(request.form['user_id'], request.form['username'], request.form['role'])
            if edited:
                return redirect(url_for('log.users'))
            else:
                return render_template('err.html', err=err_msg)
    return abort(403)

@log_bp.route('/users/delete/<id>', methods=['GET'])
def deleteUser(id):
    allowed_session = session.get('loggedin') and session.get('role') == 'Administrateur'

    if allowed_session:
        if User.remove_user(id):
            return redirect(url_for('log.users'))
        else:
            err_msg = "L'utilisateur demandé n'existe pas."
            return render_template('err.html', err=err_msg)
    return abort(403)

@log_bp.route('/add-user', methods=['POST'])
def addUser():
    allowed_session = session.get('loggedin') and session.get('role') == 'Administrateur'

    if allowed_session:
        if request.method == 'POST':
            added, err_msg = User.add_user(request.form['username'], request.form['passwd'], request.form['passwd2'], request.form['role'])
            if added:
                return redirect(url_for('log.users'))
            else:
                return render_template('err.html', err=err_msg)
    return abort(403)

# logs pages
@log_bp.route('/logs', methods=['GET', 'POST'])
def logs():
    allowed_session = session.get('loggedin')

    if allowed_session:
        if request.method == 'POST':
            machines = request.form.getlist('machines')
            logs = request.form.getlist('files')
            content, errors = logreader.read(machines, logs)
            return render_template('display-logs.html', machines=machines, logs=logs, content=content, errors=errors)
        return render_template('logs.html', machines=Machine.query.all(), files=Log.query.all())
    return abort(403)

@log_bp.route('/manage-logs', methods=['POST'])
def manageLogs():
    allowed_session = session.get('loggedin') and session.get('role') == 'Administrateur'

    if allowed_session:
        if request.method == 'POST':
            action = request.form.get('manage_action')
            if action == 'add':
                new_path = request.form.get('new_log_path', '').strip()
                Log.add_log(new_path)
            elif action == 'delete':
                file_path = request.form.get('file_to_manage')
                if file_path:
                    Log.remove_log(file_path)
        return redirect(url_for('log.logs'))
    return abort(403)

# Error handlers
@log_bp.app_errorhandler(403)
def forbidden(error):
    return render_template('http_error.html', code=403, title='Accès refusé', message=f"Vous n'êtes pas autorisé à accéder à <strong>{request.path}</strong>."), 403

@log_bp.app_errorhandler(404)
def not_found(error):
    return render_template('http_error.html', code=404, title='Page non trouvée', message=f"Le chemin demandé <strong>{request.path}</strong> est introuvable sur ce serveur."), 404

@log_bp.app_errorhandler(405)
def method_not_allowed(error):
    return render_template('http_error.html', code=405, title='Méthode non autorisée', message=f"La requête vers <strong>{request.path}</strong> utilise une méthode HTTP non prise en charge par cette ressource."), 405

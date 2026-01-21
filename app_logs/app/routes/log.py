from flask import Blueprint, render_template, request, redirect, session, abort, url_for
from app import db, logreader
from app.models.applogs import Privilege, Role, User, Machine, Log
from app.utils import string_hash, registered, get_role, get_privileges, ip_valide

log_bp = Blueprint('log', __name__, template_folder='../templates')

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
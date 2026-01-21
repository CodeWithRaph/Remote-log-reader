from flask import Blueprint, render_template, request, redirect, session, abort, url_for
from app import db, logreader
from app.models.applogs import Privilege, Role, User, Machine, Log
from app.utils import string_hash, registered, get_role, get_privileges, ip_valide

machine_bp = Blueprint('machine', __name__, template_folder='../templates')

# machines pages
@machine_bp.route('/machines', methods=['GET'])
def machines():
    allowed_session = session.get('loggedin') and session.get('role') in ('Gestionnaire', 'Administrateur')

    if allowed_session:
        return render_template("machines.html", table=Machine.query.all(), session_role=session.get('role'))
    return abort(403)

@machine_bp.route('/selected-machine', methods=['POST'])
def selectedMachine():
    allowed_session = session.get('loggedin') and session.get('role') in ('Gestionnaire', 'Administrateur')

    if allowed_session:
        if request.method == 'POST':
            id = request.form['host_id']

            if request.form['action'] == "edit":
                return redirect(url_for('machine.editMachine', id=id))
            elif request.form['action'] == "delete":
                return redirect(url_for('machine.deleteMachine', id=id))
    return abort(403)

@machine_bp.route('/machines/edit/<id>', methods=['GET'])
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

@machine_bp.route('/edit-machine', methods=['POST'])
def editingMachine():
    allowed_session = session.get('loggedin') and session.get('role') in ('Gestionnaire', 'Administrateur')

    if allowed_session:
        if request.method == 'POST':
            edited, err_msg = Machine.edit_machine(request.form['host_id'], request.form['host'], request.form['ip'])

            if edited:
                return redirect(url_for('machine.machines'))
            else:
                return render_template('err.html', err=err_msg)
    return abort(403)

@machine_bp.route('/machines/delete/<id>', methods=['GET'])
def deleteMachine(id):
    allowed_session = session.get('loggedin') and session.get('role') in ('Gestionnaire', 'Administrateur')

    if allowed_session:
        if Machine.remove_machine(id):
            return redirect(url_for('machine.machines'))
        else:
            err_msg = "La machine demandée n'existe pas."
            return render_template('err.html', err=err_msg)
    return abort(403)

@machine_bp.route('/add-machine', methods=['POST'])
def addMachine():
    allowed_session = session.get('loggedin') and session.get('role') in ('Gestionnaire', 'Administrateur')

    if allowed_session:
        if request.method == 'POST':
            added, err_msg = Machine.add_machine(request.form['host'], request.form['ip'])
            if added:
                return redirect(url_for('machine.machines'))
            else:
                return render_template('err.html', err=err_msg)
    return abort(403)
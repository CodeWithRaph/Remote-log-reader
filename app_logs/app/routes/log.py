from flask import Blueprint, render_template, request, redirect, session, abort, url_for, jsonify
from app import db, logreader
from app.models.applogs import Machine, Log
import threading

log_bp = Blueprint('log', __name__, template_folder='../templates')

# Simple in-memory task store for background jobs (single-process only)
logtask = {}
log_lock = threading.Lock()

def _background_worker(machines, logs):
    """Background worker that runs the synchronous read and stores results."""
    content, errors = logreader.read(machines, logs)
    result = {
        'status': 'done',
        'machines': machines,
        'logs': logs,
        'content': content,
        'errors': errors
    }
    # update the shared dict under the lock (don't rebind the name)
    with log_lock:
        logtask.clear()
        logtask.update(result)

# logs pages
@log_bp.route('/logs', methods=['GET', 'POST'])
def logs():
    allowed_session = session.get('loggedin')

    if allowed_session:
        if request.method == 'POST':
            machines = request.form.getlist('machines')
            logs = request.form.getlist('files')

            # initialize shared task status and start background thread
            with log_lock:
                logtask.clear()
                logtask.update({'status': 'running', 'machines': machines, 'logs': logs})

            # start background thread
            t = threading.Thread(target=_background_worker, args=(machines, logs), daemon=True)
            t.start()

            # redirect to a loading page that will wait for results
            return redirect(url_for('log.wait'))

        return render_template('logs.html', machines=Machine.query.all(), files=Log.query.all())
    return abort(403)


@log_bp.route('/logs/wait')
def wait():
    """Render a loading page."""
    allowed_session = session.get('loggedin')
    if not allowed_session:
        return abort(403)
    return render_template('loading.html')


@log_bp.route('/logs/status/')
def status():
    """Return JSON with the current task status."""
    allowed_session = session.get('loggedin')
    if not allowed_session:
        return jsonify({'status': 'forbidden'}), 403
    with log_lock:
        task = logtask
    return jsonify({'status': task.get('status', 'unknown')})


@log_bp.route('/logs/result/')
def result():
    """Render the display page when the background job is done."""
    allowed_session = session.get('loggedin')
    if not allowed_session:
        return abort(403)
    with log_lock:
        task = logtask
    if task.get('status') != 'done':
        # not ready yet: redirect back to the waiting page
        return redirect(url_for('log.wait'))

    return render_template('display-logs.html', machines=task.get('machines'), logs=task.get('logs'), content=task.get('content'), errors=task.get('errors'))


@log_bp.route('/manage-logs', methods=['POST'])
def manageLogs():
    allowed_session = session.get('loggedin') and session.get('role') == 'Administrateur'

    if allowed_session:
        if request.method == 'POST':
            action = request.form.get('manage_action')
            if action == 'add':
                new_path = request.form.get('new_log_path', '').strip()
                new_path = new_path.replace(" ", "")
                Log.add_log(new_path)
            elif action == 'delete':
                file_path = request.form.get('file_to_manage')
                if file_path:
                    Log.remove_log(file_path)
        return redirect(url_for('log.logs'))
    return abort(403)
from flask import Blueprint, render_template, request
from app import db, logreader

error_bp = Blueprint('error', __name__, template_folder='../templates')

# Error handlers
@error_bp.app_errorhandler(403)
def forbidden(error):
    return render_template('http_error.html', code=403, title='Accès refusé', message=f"Vous n'êtes pas autorisé à accéder à <strong>{request.path}</strong>."), 403

@error_bp.app_errorhandler(404)
def not_found(error):
    return render_template('http_error.html', code=404, title='Page non trouvée', message=f"Le chemin demandé <strong>{request.path}</strong> est introuvable sur ce serveur."), 404

@error_bp.app_errorhandler(405)
def method_not_allowed(error):
    return render_template('http_error.html', code=405, title='Méthode non autorisée', message=f"La requête vers <strong>{request.path}</strong> utilise une méthode HTTP non prise en charge par cette ressource."), 405

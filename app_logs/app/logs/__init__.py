from flask import Blueprint

from app.logs.routes import log_bp

blueprints = [log_bp]
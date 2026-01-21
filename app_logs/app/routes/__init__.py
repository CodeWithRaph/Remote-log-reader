from flask import Blueprint

from app.routes.auth import auth_bp
from app.routes.error import error_bp
from app.routes.log import log_bp
from app.routes.machine import machine_bp
from app.routes.user import user_bp

blueprints = [auth_bp, error_bp, log_bp, machine_bp, user_bp]
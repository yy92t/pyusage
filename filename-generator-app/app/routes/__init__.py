# filepath: /filename-generator-app/filename-generator-app/app/routes/__init__.py
from flask import Blueprint

# Initialize the routes blueprint
routes_bp = Blueprint('routes', __name__)

from .generator import *  # Import routes from generator.py to register them with the blueprint
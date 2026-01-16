from flask import Blueprint, request, jsonify
from app.services.filename_service import generate_file_name

generator_bp = Blueprint('generator', __name__)

@generator_bp.route('/generate', methods=['POST'])
def generate():
    data = request.json
    prefix = data.get('prefix', '')
    suffix = data.get('suffix', '')
    extension = data.get('extension', 'txt')
    
    file_name = generate_file_name(prefix=prefix, suffix=suffix, extension=extension)
    return jsonify({'file_name': file_name})
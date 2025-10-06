from flask import Blueprint, jsonify
from models import db

health_bp = Blueprint('health', __name__, url_prefix='/api/health')

@health_bp.route('/', methods=['GET'])
def healthcheck():
    try:
        db.session.execute('SELECT 1')
        db_ok = True
    except Exception:
        db_ok = False
    return jsonify({
        'status': 'ok',
        'database': 'ok' if db_ok else 'error',
        'message': 'Budgetter backend is healthy.'
    })

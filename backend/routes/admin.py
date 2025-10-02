from flask import Blueprint, request, jsonify
from backend.models import Complaint
from backend.database import db

admin_bp = Blueprint('admin', __name__)

@admin_bp.route('/complaints', methods=['GET'])
def admin_complaints():
    complaints = Complaint.query.all()
    return jsonify([{
        'id': c.id,
        'user_id': c.user_id,
        'type': c.type,
        'description': c.description,
        'status': c.status,
        'solution': c.solution,
        'created_at': c.created_at,
        'updated_at': c.updated_at
    } for c in complaints])

@admin_bp.route('/update_status', methods=['POST'])
def update_status():
    data = request.json
    complaint = Complaint.query.get(data['complaint_id'])
    if not complaint:
        return jsonify({'message': 'Not found'}), 404
    complaint.status = data['status']
    db.session.commit()
    return jsonify({'message': 'Status updated'})

@admin_bp.route('/add_solution', methods=['POST'])
def add_solution():
    data = request.json
    complaint = Complaint.query.get(data['complaint_id'])
    if not complaint:
        return jsonify({'message': 'Not found'}), 404
    complaint.solution = data['solution']
    db.session.commit()
    return jsonify({'message': 'Solution updated'})

@admin_bp.route('/analytics', methods=['GET'])
def analytics():
    from sqlalchemy import func
    result = db.session.query(Complaint.type, func.count(Complaint.id)).group_by(Complaint.type).all()
    return jsonify({r[0]: r[1] for r in result})

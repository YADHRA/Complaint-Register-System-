import uuid
from flask import Blueprint, request, jsonify
from backend.models import Complaint, FAQ
from backend.database import db
from backend.utils.nlp import categorize_complaint

complaints_bp = Blueprint('complaints', __name__)

def suggest_solution(text):
    faqs = FAQ.query.all()
    for faq in faqs:
        if faq.category in text.lower() or faq.category in categorize_complaint(text):
            return faq.answer
    return "No solution found. Admin will review your complaint."

@complaints_bp.route('/', methods=['POST'])
def submit_complaint():
    data = request.json
    complaint_id = str(uuid.uuid4())
    category = categorize_complaint(data['description'])
    solution = suggest_solution(data['description'])
    complaint = Complaint(
        id=complaint_id,
        user_id=data['user_id'],
        type=category,
        description=data['description'],
        solution=solution
    )
    db.session.add(complaint)
    db.session.commit()
    return jsonify({'complaint_id': complaint_id, 'category': category, 'solution': solution})

@complaints_bp.route('/<int:user_id>', methods=['GET'])
def get_complaints(user_id):
    complaints = Complaint.query.filter_by(user_id=user_id).all()
    return jsonify([{
        'id': c.id,
        'type': c.type,
        'description': c.description,
        'status': c.status,
        'solution': c.solution,
        'created_at': c.created_at,
        'updated_at': c.updated_at
    } for c in complaints])

@complaints_bp.route('/status/<complaint_id>', methods=['GET'])
def complaint_status(complaint_id):
    complaint = Complaint.query.get(complaint_id)
    if not complaint:
        return jsonify({'message': 'Not found'}), 404
    return jsonify({'status': complaint.status, 'solution': complaint.solution})

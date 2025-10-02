from flask import Blueprint, request, jsonify
from models import FAQ
from database import db

faq_bp = Blueprint('faq', __name__)

@faq_bp.route('/', methods=['GET'])
def get_faqs():
    faqs = FAQ.query.all()
    return jsonify([{'question': f.question, 'answer': f.answer, 'category': f.category} for f in faqs])

@faq_bp.route('/', methods=['POST'])
def add_faq():
    data = request.json
    faq = FAQ(question=data['question'], answer=data['answer'], category=data['category'])
    db.session.add(faq)
    db.session.commit()
    return jsonify({'message': 'FAQ added'})

@faq_bp.route('/chatbot', methods=['POST'])
def chatbot():
    data = request.json
    question = data['question']
    faqs = FAQ.query.all()
    for faq in faqs:
        if faq.question.lower() in question.lower():
            return jsonify({'answer': faq.answer})
    return jsonify({'answer': 'Sorry, I do not have an answer. Please contact admin.'})

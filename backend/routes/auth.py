from models import User
from database import db
from utils.auth import hash_password, verify_password
from flask import Blueprint, request, jsonify
auth_bp = Blueprint('auth', __name__)
@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.json
    if not data or not data.get('username') or not data.get('password'):
        return jsonify({'message': 'Missing username or password'}), 400
    if User.query.filter_by(username=data['username']).first():
        return jsonify({'message': 'User exists'}), 400
    user = User(username=data['username'], password=hash_password(data['password']))
    db.session.add(user)
    db.session.commit()
    return jsonify({'message': 'Registered successfully'})
@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.json
    if not data or not data.get('username') or not data.get('password'):
        return jsonify({'message': 'Missing username or password'}), 400
    user = User.query.filter_by(username=data['username']).first()
    if user and verify_password(user.password, data['password']):
        return jsonify({'message': 'Login successful', 'role': user.role, 'user_id': user.id})
    return jsonify({'message': 'Invalid credentials'}), 401
import uuid
from flask import Blueprint, request, jsonify
from backend.models import Complaint, FAQ
from backend.database import db
from backend.utils.nlp import categorize_complaint
complaints_bp = Blueprint('complaints', __name__)
def suggest_solution(text):
    text_lower = text.lower()
    category = categorize_complaint(text)
    # Specific solution mappings based on common complaint keywords
    solutions = {
        'id card': "For lost ID card: 1) Visit the ID Card Section in the Administration Building. 2) File a complaint form with your details. 3) Pay the replacement fee if applicable. 4) Collect your new ID card within 3-5 working days. You may need to bring your fee receipt and a passport-sized photo.",
        'lost card': "For lost ID card: 1) Visit the ID Card Section in the Administration Building. 2) File a complaint form with your details. 3) Pay the replacement fee if applicable. 4) Collect your new ID card within 3-5 working days. You may need to bring your fee receipt and a passport-sized photo.",
        'library': "For library-related issues: 1) Contact the Library Help Desk. 2) For lost books, visit the Library Office to pay the fine. 3) For access issues, contact librarian@institution.edu. 4) Library hours: Mon-Fri 8 AM - 8 PM, Sat 9 AM - 5 PM.",
        'hostel': "For hostel issues: 1) Contact your Hostel Warden immediately. 2) For maintenance, submit a request at the Hostel Office. 3) For room changes, visit during office hours (9 AM - 5 PM). 4) Emergency contact: Hostel Office +XX-XXXX-XXXX.",
        'room': "For room-related issues: 1) Report to your Hostel Warden. 2) For maintenance/repairs, contact the Maintenance Department. 3) For room allocation issues, visit the Hostel Administration Office. 4) Keep your room allotment letter handy.",
        'wifi': "For WiFi/Internet issues: 1) Check if your credentials are correct. 2) Restart your device and router. 3) Contact IT Help Desk at ithelp@institution.edu. 4) Visit IT Department in Admin Block for login issues. 5) WiFi Support: Mon-Sat 9 AM - 6 PM.",
        'internet': "For internet connectivity issues: 1) Verify your network credentials. 2) Check if the service is active in your area. 3) Contact IT Support at ithelp@institution.edu. 4) Visit IT Help Desk in the Admin Building. 5) Call IT Support: +XX-XXXX-XXXX.",
        'transport': "For transport issues: 1) Contact the Transport Office in the Administration Building. 2) For bus pass issues, visit during office hours with your ID. 3) For route/timing queries, check the Transport Notice Board or call +XX-XXXX-XXXX. 4) Report bus breakdowns immediately.",
        'bus': "For bus-related issues: 1) Contact Transport Department. 2) For route changes, check the Transport Notice Board. 3) For bus pass renewal, visit Transport Office with your ID and photo. 4) Emergency Transport Contact: +XX-XXXX-XXXX.",
        'fee': "For fee-related issues: 1) Visit the Accounts Section with your fee receipt. 2) For payment issues, contact accounts@institution.edu. 3) For fee concession/scholarship, visit the Scholarship Cell. 4) Office hours: Mon-Fri 10 AM - 4 PM. 5) Bring your student ID and relevant documents.",
        'exam': "For examination issues: 1) Contact the Examination Department immediately. 2) For hall ticket issues, visit Exam Cell with your ID. 3) For result queries, check the official website or email exam@institution.edu. 4) For revaluation, submit the form within the deadline.",
        'grade': "For grade/marks issues: 1) First contact your Course Instructor. 2) For grade discrepancies, submit a revaluation request within 7 days. 3) Visit the Examination Office with your mark sheets. 4) Email: exam@institution.edu with your details.",
        'light': "For lighting/electrical issues: 1) Report to the Maintenance Department immediately. 2) For classroom issues, inform your Department Office. 3) For hostel issues, contact the Hostel Warden. 4) Maintenance Helpline: +XX-XXXX-XXXX. 5) For urgent issues, call Security: +XX-XXXX-XXXX.",
        'electricity': "For electrical issues: 1) Report immediately to Maintenance Department. 2) Do not attempt to fix it yourself. 3) For emergencies, call Security. 4) Visit the Maintenance Office in Admin Building. 5) Helpline: +XX-XXXX-XXXX.",
        'water': "For water supply issues: 1) Report to the Maintenance Department. 2) For hostel water issues, contact your Warden. 3) For drinking water problems, visit the Admin Office. 4) Emergency: Call Security or Maintenance at +XX-XXXX-XXXX.",
        'toilet': "For toilet/washroom issues: 1) Report immediately to Maintenance Department. 2) For hostel washrooms, contact the Hostel Warden. 3) For classroom facilities, inform the Department Office. 4) Maintenance Helpline: +XX-XXXX-XXXX.",
        'cleanliness': "For cleanliness issues: 1) Report to the Housekeeping Department. 2) For hostel cleanliness, contact your Warden. 3) For classroom/lab cleanliness, inform the Department Head. 4) Submit complaints to housekeeping@institution.edu.",
        'food': "For mess/food complaints: 1) Contact the Mess Committee Representative. 2) Visit the Chief Warden's Office with your complaint. 3) For food quality issues, submit a written complaint. 4) Mess Committee meets every Friday at 5 PM. 5) Email: mess@institution.edu.",
        'canteen': "For canteen issues: 1) Speak with the Canteen Manager. 2) For serious complaints, contact the Chief Warden. 3) For food quality concerns, report to the Student Welfare Office. 4) Feedback box available at the canteen entrance.",
    }
    # Check for keyword matches
    for keyword, solution in solutions.items():
        if keyword in text_lower:
            return solution
    # Category-based fallback solutions
    category_solutions = {
        'academic': "For academic issues: 1) Contact your Course Instructor or Academic Advisor. 2) Visit the Academic Section in your Department. 3) For serious concerns, email the Head of Department. 4) Office hours: Mon-Fri 10 AM - 4 PM.",
        'infrastructure': "For infrastructure issues: 1) Report to the Maintenance Department in the Admin Building. 2) Provide specific details and location. 3) Call Maintenance Helpline: +XX-XXXX-XXXX. 4) For urgent repairs, contact Security. 5) Track your complaint status with the given complaint ID.",
        'hostel': "For hostel-related issues: 1) Contact your Hostel Warden immediately. 2) For room allocation or changes, visit the Hostel Office. 3) For maintenance issues, submit a request form. 4) Emergency contact: Call Security at +XX-XXXX-XXXX.",
        'transport': "For transport-related issues: 1) Visit the Transport Office in Admin Building. 2) For route/timing information, check the notice board. 3) For bus pass issues, bring your student ID and photo. 4) Call Transport Office: +XX-XXXX-XXXX.",
        'administration': "For administrative issues: 1) Visit the relevant section in the Administration Building. 2) Bring necessary documents and your student ID. 3) For document-related queries, contact the Administrative Office. 4) Office hours: Mon-Fri 10 AM - 4 PM.",
    }
    if category in category_solutions:
        return category_solutions[category]
    
    return "Your complaint has been registered. Admin will review and provide a solution soon. For urgent matters, visit the Student Welfare Office in the Administration Building during office hours (Mon-Fri, 10 AM - 4 PM) or call the Help Desk at +XX-XXXX-XXXX."

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

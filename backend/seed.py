from backend.app import create_app
from backend.database import db
from backend.models import User, Complaint, FAQ
from backend.utils.auth import hash_password
import uuid

app = create_app()
with app.app_context():
    db.drop_all()
    db.create_all()

    # Create admin user
    if not User.query.filter_by(username="admin").first():
        admin = User(username="admin", password=hash_password("admin123"), role="admin")
        db.session.add(admin)

    # Create a sample student user
    if not User.query.filter_by(username="alice").first():
        alice = User(username="alice", password=hash_password("alice123"))
        db.session.add(alice)
        db.session.commit()
        c1 = Complaint(
            id=str(uuid.uuid4()),
            user_id=alice.id,
            type="infrastructure",
            description="Lights not working in room",
            status="Pending"
        )
        db.session.add(c1)

    # Add a sample FAQ
    if not FAQ.query.first():
        faq = FAQ(
            question="How do I submit a complaint?",
            answer="Go to your dashboard and click 'Submit Complaint'.",
            category="general"
        )
        db.session.add(faq)

    db.session.commit()
    print("Seeded")
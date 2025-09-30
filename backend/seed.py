# backend/seed.py
from app import create_app
from database import db
from models import User, Complaint
import uuid

app = create_app()
with app.app_context():
    db.create_all()
    if not User.query.filter_by(username="admin").first():
        admin = User(username="admin", password="pbkdf2:sha256:150000$xxx$xxx", role="admin")
        db.session.add(admin)
    if not User.query.filter_by(username="alice").first():
        alice = User(username="alice", password="pbkdf2:sha256:150000$xxx$xxx")
        db.session.add(alice)
        db.session.commit()
        c1 = Complaint(id=str(uuid.uuid4()), user_id=alice.id, type="infrastructure", description="Lights not working in room", status="Pending")
        db.session.add(c1)
        db.session.commit()
    print("Seeded")

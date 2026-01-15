from flask_sqlalchemy import SQLAlchemy
import uuid

db = SQLAlchemy()


class User(db.Model):
    __tablename__ = "users"

    id = db.Column(
        db.String(36),
        primary_key=True,
        unique=True,
        default=lambda: str(uuid.uuid4())
    )
    username = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    role = db.Column(db.String(50), nullable=False)
    salt = db.Column(db.String(36), nullable=False)

    def to_dict(self):
        return {
            "id": self.id,
            "username": self.username,
            "role": self.role
        }

from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class Article(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    date = db.Column(db.String(20), nullable=False)
    excerpt = db.Column(db.Text, nullable=False)
    content = db.Column(db.Text, nullable=False)
    tags = db.Column(db.String(500), default='')  # comma-separated

    def get_tags_list(self):
        return [t.strip() for t in self.tags.split(',') if t.strip()]

    def set_tags_list(self, tags_list):
        self.tags = ','.join(tags_list)


class ResumeSection(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    section_type = db.Column(db.String(50), nullable=False)  # 'about', 'experience', 'skills', etc.
    identifier = db.Column(db.String(100), nullable=True)  # e.g., experience item id
    content = db.Column(db.Text, nullable=False)  # JSON string for complex data
    updated_at = db.Column(db.DateTime, default=db.func.now(), onupdate=db.func.now())


class Experience(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    company = db.Column(db.String(200), nullable=False)
    role = db.Column(db.String(200), nullable=False)
    period = db.Column(db.String(100), default='')
    duration = db.Column(db.String(100), default='')
    description = db.Column(db.Text, default='')  # Markdown content
    sort_order = db.Column(db.Integer, default=0)

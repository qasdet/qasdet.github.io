from flask import Flask, render_template, request, jsonify, redirect, url_for, flash
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from functools import wraps
import json
import os

from config import Config
from models import db, User, Article, ResumeSection, Experience

app = Flask(__name__)
app.config.from_object(Config)

# Initialize extensions
db.init_app(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message = 'Пожалуйста, войдите для доступа к админке'


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


# ============== AUTH ROUTES ==============

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('admin'))

    if request.method == 'POST':
        data = request.get_json() if request.is_json else request.form
        username = data.get('username')
        password = data.get('password')

        if username and password:
            user = User.query.filter_by(username=username).first()
            if user and user.check_password(password):
                login_user(user)
                if request.is_json:
                    return jsonify({'success': True})
                return redirect(url_for('admin'))

        if request.is_json:
            return jsonify({'success': False, 'error': 'Неверный логин или пароль'}), 401

    return render_template('login.html')


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))


# ============== PAGE ROUTES ==============

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/blog')
def blog():
    return render_template('blog.html')


@app.route('/projects')
def projects():
    return render_template('projects.html')


@app.route('/admin')
@login_required
def admin():
    return render_template('admin.html')


# ============== BLOG API (CRUD) ==============

@app.route('/api/articles', methods=['GET'])
def get_articles():
    articles = Article.query.order_by(Article.date.desc()).all()
    return jsonify([{
        'id': a.id,
        'title': a.title,
        'date': a.date,
        'excerpt': a.excerpt,
        'content': a.content,
        'tags': a.get_tags_list()
    } for a in articles])


@app.route('/api/articles', methods=['POST'])
@login_required
def create_article():
    data = request.get_json()

    article = Article(
        title=data['title'],
        date=data.get('date', ''),
        excerpt=data.get('excerpt', ''),
        content=data.get('content', ''),
        tags=data.get('tags', '')
    )
    article.set_tags_list(data.get('tags', []))

    db.session.add(article)
    db.session.commit()

    return jsonify({
        'id': article.id,
        'title': article.title,
        'date': article.date,
        'excerpt': article.excerpt,
        'content': article.content,
        'tags': article.get_tags_list()
    }), 201


@app.route('/api/articles/<int:article_id>', methods=['GET'])
def get_article(article_id):
    article = Article.query.get_or_404(article_id)
    return jsonify({
        'id': article.id,
        'title': article.title,
        'date': article.date,
        'excerpt': article.excerpt,
        'content': article.content,
        'tags': article.get_tags_list()
    })


@app.route('/api/articles/<int:article_id>', methods=['PUT'])
@login_required
def update_article(article_id):
    article = Article.query.get_or_404(article_id)
    data = request.get_json()

    article.title = data.get('title', article.title)
    article.date = data.get('date', article.date)
    article.excerpt = data.get('excerpt', article.excerpt)
    article.content = data.get('content', article.content)

    if 'tags' in data:
        article.set_tags_list(data['tags'])

    db.session.commit()

    return jsonify({
        'id': article.id,
        'title': article.title,
        'date': article.date,
        'excerpt': article.excerpt,
        'content': article.content,
        'tags': article.get_tags_list()
    })


@app.route('/api/articles/<int:article_id>', methods=['DELETE'])
@login_required
def delete_article(article_id):
    article = Article.query.get_or_404(article_id)
    db.session.delete(article)
    db.session.commit()
    return '', 204


# ============== RESUME API ==============

@app.route('/api/resume', methods=['GET'])
def get_resume():
    """Get all resume sections"""
    sections = ResumeSection.query.all()
    return jsonify({
        s.section_type: json.loads(s.content) for s in sections
    })


@app.route('/api/resume/<section_type>', methods=['PUT'])
@login_required
def update_resume_section(section_type):
    """Update a resume section"""
    data = request.get_json()

    section = ResumeSection.query.filter_by(section_type=section_type).first()
    if section:
        section.content = json.dumps(data)
    else:
        section = ResumeSection(
            section_type=section_type,
            content=json.dumps(data)
        )
        db.session.add(section)

    db.session.commit()
    return jsonify({'success': True})


# ============== EXPERIENCE API (CRUD) ==============

@app.route('/api/experience', methods=['GET'])
def get_experiences():
    """Get all experiences ordered by sort_order"""
    experiences = Experience.query.order_by(Experience.sort_order.desc()).all()
    return jsonify([{
        'id': e.id,
        'company': e.company,
        'role': e.role,
        'period': e.period,
        'duration': e.duration,
        'description': e.description,
        'sort_order': e.sort_order
    } for e in experiences])


@app.route('/api/experience', methods=['POST'])
@login_required
def create_experience():
    """Create new experience"""
    data = request.get_json()

    # Get max sort_order
    max_order = db.session.query(db.func.max(Experience.sort_order)).scalar() or 0

    experience = Experience(
        company=data.get('company', ''),
        role=data.get('role', ''),
        period=data.get('period', ''),
        duration=data.get('duration', ''),
        description=data.get('description', ''),
        sort_order=max_order + 1
    )
    db.session.add(experience)
    db.session.commit()

    return jsonify({
        'id': experience.id,
        'company': experience.company,
        'role': experience.role,
        'period': experience.period,
        'duration': experience.duration,
        'description': experience.description,
        'sort_order': experience.sort_order
    }), 201


@app.route('/api/experience/<int:exp_id>', methods=['GET'])
def get_experience(exp_id):
    """Get single experience"""
    experience = Experience.query.get_or_404(exp_id)
    return jsonify({
        'id': experience.id,
        'company': experience.company,
        'role': experience.role,
        'period': experience.period,
        'duration': experience.duration,
        'description': experience.description,
        'sort_order': experience.sort_order
    })


@app.route('/api/experience/<int:exp_id>', methods=['PUT'])
@login_required
def update_experience(exp_id):
    """Update experience"""
    experience = Experience.query.get_or_404(exp_id)
    data = request.get_json()

    experience.company = data.get('company', experience.company)
    experience.role = data.get('role', experience.role)
    experience.period = data.get('period', experience.period)
    experience.duration = data.get('duration', experience.duration)
    experience.description = data.get('description', experience.description)

    db.session.commit()

    return jsonify({
        'id': experience.id,
        'company': experience.company,
        'role': experience.role,
        'period': experience.period,
        'duration': experience.duration,
        'description': experience.description,
        'sort_order': experience.sort_order
    })


@app.route('/api/experience/<int:exp_id>', methods=['DELETE'])
@login_required
def delete_experience(exp_id):
    """Delete experience"""
    experience = Experience.query.get_or_404(exp_id)
    db.session.delete(experience)
    db.session.commit()
    return '', 204


@app.route('/api/experience/reorder', methods=['PUT'])
@login_required
def reorder_experiences():
    """Reorder experiences"""
    data = request.get_json()
    order = data.get('order', [])  # list of {id, sort_order}

    for item in order:
        exp = Experience.query.get(item['id'])
        if exp:
            exp.sort_order = item['sort_order']

    db.session.commit()
    return jsonify({'success': True})


# ============== INIT ==============

def init_app():
    with app.app_context():
        db.create_all()


if __name__ == '__main__':
    init_app()
    app.run(debug=True, port=5000)

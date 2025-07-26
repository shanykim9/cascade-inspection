from flask import render_template, request, redirect, url_for, flash, session, jsonify
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from werkzeug.security import check_password_hash, generate_password_hash
from app import app, db
from models import User
import re

# Initialize Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'index'
login_manager.login_message = '로그인이 필요합니다.'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/')
def index():
    """메인 페이지 - 로그인/회원가입"""
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    return render_template('index.html')

@app.route('/login', methods=['POST'])
def login():
    """로그인 처리"""
    username = request.form.get('username', '').strip()
    password = request.form.get('password', '')
    
    if not username or not password:
        flash('아이디와 패스워드를 모두 입력해주세요.', 'error')
        return redirect(url_for('index'))
    
    user = User.query.filter_by(username=username).first()
    
    if user and user.active_status and check_password_hash(user.password_hash, password):
        login_user(user)
        flash(f'{user.name}님, 환영합니다!', 'success')
        return redirect(url_for('dashboard'))
    else:
        flash('아이디 또는 패스워드가 올바르지 않습니다.', 'error')
        return redirect(url_for('index'))

@app.route('/register')
def register():
    """회원가입 페이지"""
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    return render_template('register.html')

@app.route('/register', methods=['POST'])
def register_post():
    """회원가입 처리"""
    username = request.form.get('username', '').strip()
    password = request.form.get('password', '')
    confirm_password = request.form.get('confirm_password', '')
    name = request.form.get('name', '').strip()
    phone = request.form.get('phone', '').strip()
    employee_id = request.form.get('employee_id', '').strip()
    
    # 입력값 검증
    if not all([username, password, confirm_password, name, phone, employee_id]):
        flash('모든 항목을 입력해주세요.', 'error')
        return redirect(url_for('register'))
    
    if password != confirm_password:
        flash('패스워드가 일치하지 않습니다.', 'error')
        return redirect(url_for('register'))
    
    if len(password) < 6:
        flash('패스워드는 최소 6자 이상이어야 합니다.', 'error')
        return redirect(url_for('register'))
    
    # 사번 형식 검증 (숫자만)
    if not employee_id.isdigit():
        flash('사번은 숫자만 입력 가능합니다.', 'error')
        return redirect(url_for('register'))
    
    # 전화번호 형식 검증
    phone_pattern = re.compile(r'^[0-9-]+$')
    if not phone_pattern.match(phone):
        flash('전화번호 형식이 올바르지 않습니다.', 'error')
        return redirect(url_for('register'))
    
    # 중복 확인
    if User.query.filter_by(username=username).first():
        flash('이미 존재하는 아이디입니다.', 'error')
        return redirect(url_for('register'))
    
    if User.query.filter_by(employee_id=employee_id).first():
        flash('이미 등록된 사번입니다.', 'error')
        return redirect(url_for('register'))
    
    # 새 사용자 생성
    new_user = User()
    new_user.username = username
    new_user.name = name
    new_user.phone = phone
    new_user.employee_id = employee_id
    new_user.password_hash = generate_password_hash(password)
    new_user.role = 'input'  # 기본 권한
    
    db.session.add(new_user)
    db.session.commit()
    
    flash('회원가입이 완료되었습니다. 로그인해주세요.', 'success')
    return redirect(url_for('index'))

@app.route('/dashboard')
@login_required
def dashboard():
    """사용자 대시보드"""
    return render_template('dashboard.html', user=current_user)

@app.route('/logout')
@login_required
def logout():
    """로그아웃"""
    logout_user()
    flash('로그아웃되었습니다.', 'info')
    return redirect(url_for('index'))

@app.route('/api/users')
@login_required
def api_users():
    """사용자 목록 API (관리자만)"""
    if not current_user.has_permission('admin'):
        return jsonify({'error': 'Permission denied'}), 403
    
    users = User.query.all()
    users_data = []
    for user in users:
        users_data.append({
            'id': user.id,
            'username': user.username,
            'name': user.name,
            'phone': user.phone,
            'employee_id': user.employee_id,
            'role': user.role,
            'is_active': user.active_status,
            'created_at': user.created_at.strftime('%Y-%m-%d')
        })
    
    return jsonify(users_data)

@app.route('/api/users/<int:user_id>/role', methods=['PUT'])
@login_required
def update_user_role(user_id):
    """사용자 권한 변경 API (관리자만)"""
    if not current_user.has_permission('admin'):
        return jsonify({'error': 'Permission denied'}), 403
    
    data = request.get_json() or {}
    new_role = data.get('role')
    if new_role not in ['input', 'download', 'admin']:
        return jsonify({'error': 'Invalid role'}), 400
    
    user = User.query.get_or_404(user_id)
    user.role = new_role
    db.session.commit()
    
    return jsonify({'success': True, 'message': f'{user.name}의 권한이 {new_role}로 변경되었습니다.'})

@app.route('/api/users/<int:user_id>/toggle-active', methods=['PUT'])
@login_required
def toggle_user_active(user_id):
    """사용자 활성화/비활성화 API (관리자만)"""
    if not current_user.has_permission('admin'):
        return jsonify({'error': 'Permission denied'}), 403
    
    user = User.query.get_or_404(user_id)
    user.active_status = not user.active_status
    db.session.commit()
    
    status = '활성화' if user.active_status else '비활성화'
    return jsonify({'success': True, 'message': f'{user.name}가 {status}되었습니다.', 'is_active': user.active_status})

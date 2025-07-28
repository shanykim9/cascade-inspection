from flask import render_template, request, redirect, url_for, flash, session, jsonify
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import datetime
import re
from supabase_client import supabase

# Initialize Flask-Login
login_manager = LoginManager()

def init_routes(app, db, User, Inspection):
    """라우트 초기화 함수"""
    login_manager.init_app(app)
    login_manager.login_view = 'index'
    login_manager.login_message = '로그인이 필요합니다.'

    @login_manager.user_loader
    def load_user(user_id):
        # Supabase 사용 시
        if supabase:
            try:
                response = supabase.table('users').select('*').eq('id', user_id).execute()
                if response.data:
                    user_data = response.data[0]
                    user = User()
                    user.id = user_data['id']
                    user.username = user_data['username']
                    user.name = user_data['name']
                    user.phone = user_data['phone']
                    user.employee_id = user_data['employee_id']
                    user.password_hash = user_data['password_hash']
                    user.role = user_data['role']
                    user.active_status = user_data['active_status']
                    user.created_at = user_data['created_at']
                    user.updated_at = user_data['updated_at']
                    return user
            except Exception as e:
                print(f"Supabase user load error: {e}")
        
        # 로컬 SQLite 사용
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
        
        # Supabase 사용 시
        if supabase:
            try:
                response = supabase.table('users').select('*').eq('username', username).execute()
                if response.data:
                    user_data = response.data[0]
                    if user_data['active_status'] and check_password_hash(user_data['password_hash'], password):
                        user = User()
                        user.id = user_data['id']
                        user.username = user_data['username']
                        user.name = user_data['name']
                        user.phone = user_data['phone']
                        user.employee_id = user_data['employee_id']
                        user.password_hash = user_data['password_hash']
                        user.role = user_data['role']
                        user.active_status = user_data['active_status']
                        user.created_at = user_data['created_at']
                        user.updated_at = user_data['updated_at']
                        login_user(user)
                        flash(f'{user.name}님, 환영합니다!', 'success')
                        return redirect(url_for('dashboard'))
            except Exception as e:
                print(f"Supabase login error: {e}")
        
        # 로컬 SQLite 사용
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
        
        # Supabase 사용 시
        if supabase:
            try:
                # 중복 확인
                response = supabase.table('users').select('id').eq('username', username).execute()
                if response.data:
                    flash('이미 존재하는 아이디입니다.', 'error')
                    return redirect(url_for('register'))
                
                response = supabase.table('users').select('id').eq('employee_id', employee_id).execute()
                if response.data:
                    flash('이미 등록된 사번입니다.', 'error')
                    return redirect(url_for('register'))
                
                # 새 사용자 생성
                new_user_data = {
                    'username': username,
                    'name': name,
                    'phone': phone,
                    'employee_id': employee_id,
                    'password_hash': generate_password_hash(password),
                    'role': 'input',
                    'active_status': True
                }
                
                response = supabase.table('users').insert(new_user_data).execute()
                flash('회원가입이 완료되었습니다. 로그인해주세요.', 'success')
                return redirect(url_for('index'))
                
            except Exception as e:
                print(f"Supabase register error: {e}")
                flash('회원가입 중 오류가 발생했습니다.', 'error')
                return redirect(url_for('register'))
        
        # 로컬 SQLite 사용
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

    # 점검 관련 라우트들
    @app.route('/inspection/new', methods=['GET'])
    @login_required
    def new_inspection():
        """새 점검 입력 페이지"""
        if not current_user.has_permission('input'):
            flash('점검 데이터 입력 권한이 없습니다.', 'error')
            return redirect(url_for('dashboard'))
        return render_template('inspection_form.html')

    @app.route('/inspection/new', methods=['POST'])
    @login_required
    def create_inspection():
        """점검 데이터 저장"""
        if not current_user.has_permission('input'):
            flash('점검 데이터 입력 권한이 없습니다.', 'error')
            return redirect(url_for('dashboard'))
        
        try:
            # 폼 데이터 가져오기
            equipment_type = request.form.get('equipment_type', '').strip()
            equipment_id = request.form.get('equipment_id', '').strip()
            inspection_date_str = request.form.get('inspection_date', '')
            temperature = request.form.get('temperature')
            pressure = request.form.get('pressure')
            water_level = request.form.get('water_level')
            gas_consumption = request.form.get('gas_consumption')
            efficiency = request.form.get('efficiency')
            status = request.form.get('status', 'normal')
            notes = request.form.get('notes', '').strip()
            
            # 필수 필드 검증
            if not all([equipment_type, equipment_id, inspection_date_str]):
                flash('장비 유형, 장비 번호, 점검 날짜는 필수 입력 항목입니다.', 'error')
                return redirect(url_for('new_inspection'))
            
            # 날짜 파싱
            try:
                inspection_date = datetime.fromisoformat(inspection_date_str.replace('Z', '+00:00'))
            except ValueError:
                flash('점검 날짜 형식이 올바르지 않습니다.', 'error')
                return redirect(url_for('new_inspection'))
            
            # 숫자 필드 변환
            def safe_float(value):
                return float(value) if value and value.strip() else None
            
            # Supabase 사용 시
            if supabase:
                try:
                    new_inspection_data = {
                        'user_id': current_user.id,
                        'equipment_type': equipment_type,
                        'equipment_id': equipment_id,
                        'inspection_date': inspection_date.isoformat(),
                        'temperature': safe_float(temperature),
                        'pressure': safe_float(pressure),
                        'water_level': safe_float(water_level),
                        'gas_consumption': safe_float(gas_consumption),
                        'efficiency': safe_float(efficiency),
                        'status': status,
                        'notes': notes
                    }
                    
                    response = supabase.table('inspections').insert(new_inspection_data).execute()
                    flash(f'{equipment_type} {equipment_id} 점검 데이터가 성공적으로 저장되었습니다.', 'success')
                    return redirect(url_for('dashboard'))
                    
                except Exception as e:
                    print(f"Supabase inspection save error: {e}")
                    flash('점검 데이터 저장 중 오류가 발생했습니다.', 'error')
                    return redirect(url_for('new_inspection'))
            
            # 로컬 SQLite 사용
            inspection = Inspection()
            inspection.user_id = current_user.id
            inspection.equipment_type = equipment_type
            inspection.equipment_id = equipment_id
            inspection.inspection_date = inspection_date
            inspection.temperature = safe_float(temperature)
            inspection.pressure = safe_float(pressure)
            inspection.water_level = safe_float(water_level)
            inspection.gas_consumption = safe_float(gas_consumption)
            inspection.efficiency = safe_float(efficiency)
            inspection.status = status
            inspection.notes = notes
            
            db.session.add(inspection)
            db.session.commit()
            
            flash(f'{equipment_type} {equipment_id} 점검 데이터가 성공적으로 저장되었습니다.', 'success')
            return redirect(url_for('dashboard'))
            
        except Exception as e:
            db.session.rollback()
            flash('점검 데이터 저장 중 오류가 발생했습니다.', 'error')
            return redirect(url_for('new_inspection'))

    @app.route('/inspection/list')
    @login_required
    def list_inspections():
        """점검 데이터 목록 조회"""
        if not current_user.has_permission('download'):
            flash('점검 데이터 조회 권한이 없습니다.', 'error')
            return redirect(url_for('dashboard'))
        
        # Supabase 사용 시
        if supabase:
            try:
                if current_user.has_permission('admin'):
                    response = supabase.table('inspections').select('*, users(name)').order('inspection_date', desc=True).execute()
                else:
                    response = supabase.table('inspections').select('*, users(name)').eq('user_id', current_user.id).order('inspection_date', desc=True).execute()
                
                inspections = []
                for item in response.data:
                    inspection = Inspection()
                    inspection.id = item['id']
                    inspection.user_id = item['user_id']
                    inspection.equipment_type = item['equipment_type']
                    inspection.equipment_id = item['equipment_id']
                    inspection.inspection_date = datetime.fromisoformat(item['inspection_date'].replace('Z', '+00:00'))
                    inspection.temperature = item['temperature']
                    inspection.pressure = item['pressure']
                    inspection.water_level = item['water_level']
                    inspection.gas_consumption = item['gas_consumption']
                    inspection.efficiency = item['efficiency']
                    inspection.status = item['status']
                    inspection.notes = item['notes']
                    inspection.created_at = datetime.fromisoformat(item['created_at'].replace('Z', '+00:00'))
                    
                    # 사용자 정보 추가
                    user = User()
                    user.name = item['users']['name']
                    inspection.user = user
                    
                    inspections.append(inspection)
                
                return render_template('inspection_list.html', inspections=inspections)
                
            except Exception as e:
                print(f"Supabase inspection list error: {e}")
                flash('점검 데이터 조회 중 오류가 발생했습니다.', 'error')
                return redirect(url_for('dashboard'))
        
        # 로컬 SQLite 사용
        if current_user.has_permission('admin'):
            inspections = Inspection.query.order_by(Inspection.inspection_date.desc()).all()
        else:
            inspections = Inspection.query.filter_by(user_id=current_user.id).order_by(Inspection.inspection_date.desc()).all()
        
        return render_template('inspection_list.html', inspections=inspections)

    @app.route('/api/inspections')
    @login_required
    def api_inspections():
        """점검 데이터 API (다운로드용)"""
        if not current_user.has_permission('download'):
            return jsonify({'error': 'Permission denied'}), 403
        
        # Supabase 사용 시
        if supabase:
            try:
                if current_user.has_permission('admin'):
                    response = supabase.table('inspections').select('*, users(name)').order('inspection_date', desc=True).execute()
                else:
                    response = supabase.table('inspections').select('*, users(name)').eq('user_id', current_user.id).order('inspection_date', desc=True).execute()
                
                inspections_data = []
                for item in response.data:
                    inspections_data.append({
                        'id': item['id'],
                        'equipment_type': item['equipment_type'],
                        'equipment_id': item['equipment_id'],
                        'inspection_date': item['inspection_date'][:19].replace('T', ' '),
                        'temperature': item['temperature'],
                        'pressure': item['pressure'],
                        'water_level': item['water_level'],
                        'gas_consumption': item['gas_consumption'],
                        'efficiency': item['efficiency'],
                        'status': item['status'],
                        'notes': item['notes'],
                        'inspector': item['users']['name'],
                        'created_at': item['created_at'][:19].replace('T', ' ')
                    })
                
                return jsonify(inspections_data)
                
            except Exception as e:
                print(f"Supabase API inspections error: {e}")
                return jsonify({'error': 'Database error'}), 500
        
        # 로컬 SQLite 사용
        if current_user.has_permission('admin'):
            inspections = Inspection.query.order_by(Inspection.inspection_date.desc()).all()
        else:
            inspections = Inspection.query.filter_by(user_id=current_user.id).order_by(Inspection.inspection_date.desc()).all()
        
        inspections_data = []
        for inspection in inspections:
            inspections_data.append({
                'id': inspection.id,
                'equipment_type': inspection.equipment_type,
                'equipment_id': inspection.equipment_id,
                'inspection_date': inspection.inspection_date.strftime('%Y-%m-%d %H:%M'),
                'temperature': inspection.temperature,
                'pressure': inspection.pressure,
                'water_level': inspection.water_level,
                'gas_consumption': inspection.gas_consumption,
                'efficiency': inspection.efficiency,
                'status': inspection.status,
                'notes': inspection.notes,
                'inspector': inspection.user.name,
                'created_at': inspection.created_at.strftime('%Y-%m-%d %H:%M')
            })
        
        return jsonify(inspections_data)

    @app.route('/api/users')
    @login_required
    def api_users():
        """사용자 목록 API (관리자만)"""
        if not current_user.has_permission('admin'):
            return jsonify({'error': 'Permission denied'}), 403
        
        # Supabase 사용 시
        if supabase:
            try:
                response = supabase.table('users').select('*').execute()
                users_data = []
                for user_data in response.data:
                    users_data.append({
                        'id': user_data['id'],
                        'username': user_data['username'],
                        'name': user_data['name'],
                        'phone': user_data['phone'],
                        'employee_id': user_data['employee_id'],
                        'role': user_data['role'],
                        'is_active': user_data['active_status'],
                        'created_at': user_data['created_at'][:10]
                    })
                return jsonify(users_data)
                
            except Exception as e:
                print(f"Supabase API users error: {e}")
                return jsonify({'error': 'Database error'}), 500
        
        # 로컬 SQLite 사용
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
        
        # Supabase 사용 시
        if supabase:
            try:
                response = supabase.table('users').update({'role': new_role}).eq('id', user_id).execute()
                if response.data:
                    user_name = response.data[0]['name']
                    return jsonify({'success': True, 'message': f'{user_name}의 권한이 {new_role}로 변경되었습니다.'})
                else:
                    return jsonify({'error': 'User not found'}), 404
                    
            except Exception as e:
                print(f"Supabase update user role error: {e}")
                return jsonify({'error': 'Database error'}), 500
        
        # 로컬 SQLite 사용
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
        
        # Supabase 사용 시
        if supabase:
            try:
                # 현재 상태 확인
                response = supabase.table('users').select('active_status, name').eq('id', user_id).execute()
                if not response.data:
                    return jsonify({'error': 'User not found'}), 404
                
                current_status = response.data[0]['active_status']
                user_name = response.data[0]['name']
                new_status = not current_status
                
                # 상태 업데이트
                response = supabase.table('users').update({'active_status': new_status}).eq('id', user_id).execute()
                
                status = '활성화' if new_status else '비활성화'
                return jsonify({'success': True, 'message': f'{user_name}가 {status}되었습니다.', 'is_active': new_status})
                
            except Exception as e:
                print(f"Supabase toggle user active error: {e}")
                return jsonify({'error': 'Database error'}), 500
        
        # 로컬 SQLite 사용
        user = User.query.get_or_404(user_id)
        user.active_status = not user.active_status
        db.session.commit()
        
        status = '활성화' if user.active_status else '비활성화'
        return jsonify({'success': True, 'message': f'{user.name}가 {status}되었습니다.', 'is_active': user.active_status})

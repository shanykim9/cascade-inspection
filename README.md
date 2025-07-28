# 캐스케이드 시스템 점검

캐스케이드 보일러, 온수기를 점검 관리하는 웹 애플리케이션입니다.

## 🚀 기능

- **사용자 관리**: 회원가입, 로그인, 권한 관리
- **권한 시스템**: 입력권한, 다운로드권한, 관리자권한
- **관리자 기능**: 사용자 권한 변경, 활성화/비활성화
- **반응형 디자인**: 모바일/데스크톱 지원

## 📋 요구사항

- Python 3.11 이상
- pip 또는 uv

## 🛠️ 설치 및 실행

### 1. 의존성 설치

```bash
# uv 사용 (권장)
uv sync

# 또는 pip 사용
pip install -r requirements.txt
```

### 2. 환경 변수 설정

`.env` 파일을 생성하고 다음 내용을 추가하세요:

```bash
# env.example 파일을 복사하여 .env 파일 생성
cp env.example .env
```

`.env` 파일을 편집하여 실제 값으로 변경:

```env
# Flask 설정
SESSION_SECRET=your-super-secret-key-change-this-in-production

# Supabase 설정 (선택사항)
SUPABASE_URL=your-supabase-url
SUPABASE_ANON_KEY=your-supabase-anon-key

# 데이터베이스 설정
DATABASE_URL=sqlite:///cascade_system.db
```

### 3. 애플리케이션 실행

```bash
python main.py
```

또는

```bash
uv run python main.py
```

### 4. 브라우저에서 접속

```
http://localhost:5000
```

## 👤 기본 관리자 계정

- **아이디**: admin
- **패스워드**: admin123

## 🔧 개발 환경 설정

### 데이터베이스 초기화

애플리케이션을 처음 실행하면 자동으로 SQLite 데이터베이스가 생성되고 기본 관리자 계정이 생성됩니다.

### 로그 확인

애플리케이션은 DEBUG 레벨로 로깅을 설정하므로 콘솔에서 상세한 로그를 확인할 수 있습니다.

## 📁 프로젝트 구조

```
cascade-inspection/
├── app.py              # Flask 애플리케이션 설정
├── main.py             # 애플리케이션 실행 파일
├── models.py           # 데이터베이스 모델
├── routes.py           # 라우트 정의
├── supabase_client.py  # Supabase 클라이언트 (미사용)
├── pyproject.toml      # 프로젝트 의존성
├── env.example         # 환경 변수 예시
├── static/             # 정적 파일
│   ├── css/
│   └── js/
└── templates/          # HTML 템플릿
    ├── base.html
    ├── index.html
    ├── register.html
    └── dashboard.html
```

## 🐛 문제 해결

### 순환 임포트 오류
- `app.py`와 `routes.py` 간의 순환 임포트 문제를 해결했습니다.
- 라우트는 `init_routes()` 함수를 통해 초기화됩니다.

### 의존성 오류
- `python-dotenv`와 `supabase` 패키지가 추가되었습니다.
- `uv sync` 또는 `pip install -r requirements.txt`로 설치하세요.

### 데이터베이스 오류
- SQLite 데이터베이스는 자동으로 생성됩니다.
- `instance/cascade_system.db` 파일이 생성되는지 확인하세요.

## 🔒 보안 고려사항

- 프로덕션 환경에서는 `SESSION_SECRET`을 강력한 랜덤 키로 변경하세요.
- 기본 관리자 계정의 패스워드를 변경하세요.
- HTTPS를 사용하여 통신을 암호화하세요.

## 📝 라이선스

이 프로젝트는 MIT 라이선스 하에 배포됩니다.

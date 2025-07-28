-- Supabase 데이터베이스 테이블 생성 스크립트
-- 이 파일의 내용을 Supabase SQL Editor에서 실행하세요

-- 1. 사용자 테이블 생성
CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(80) UNIQUE NOT NULL,
    name VARCHAR(100) NOT NULL,
    phone VARCHAR(20) NOT NULL,
    employee_id VARCHAR(20) UNIQUE NOT NULL,
    password_hash VARCHAR(256) NOT NULL,
    role VARCHAR(20) NOT NULL DEFAULT 'input',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    active_status BOOLEAN DEFAULT TRUE
);

-- 2. 점검 데이터 테이블 생성
CREATE TABLE IF NOT EXISTS inspections (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id) NOT NULL,
    equipment_type VARCHAR(50) NOT NULL,
    equipment_id VARCHAR(50) NOT NULL,
    inspection_date TIMESTAMP WITH TIME ZONE NOT NULL,
    temperature FLOAT,
    pressure FLOAT,
    water_level FLOAT,
    gas_consumption FLOAT,
    efficiency FLOAT,
    status VARCHAR(20) DEFAULT 'normal',
    notes TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- 3. 기본 관리자 계정 생성
INSERT INTO users (username, name, phone, employee_id, password_hash, role, active_status)
VALUES (
    'admin',
    '관리자',
    '000-0000-0000',
    '000000',
    '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewdBPj4J/vHqKqG', -- admin123
    'admin',
    TRUE
) ON CONFLICT (username) DO NOTHING;

-- 4. Row Level Security (RLS) 설정
ALTER TABLE users ENABLE ROW LEVEL SECURITY;
ALTER TABLE inspections ENABLE ROW LEVEL SECURITY;

-- 5. RLS 정책 설정
-- 사용자는 자신의 데이터만 볼 수 있음
CREATE POLICY "Users can view own data" ON users
    FOR SELECT USING (auth.uid()::text = id::text);

-- 관리자는 모든 데이터를 볼 수 있음
CREATE POLICY "Admins can view all data" ON users
    FOR ALL USING (
        EXISTS (
            SELECT 1 FROM users 
            WHERE id = auth.uid()::integer 
            AND role = 'admin'
        )
    );

-- 점검 데이터 정책
CREATE POLICY "Users can view own inspections" ON inspections
    FOR SELECT USING (user_id = auth.uid()::integer);

CREATE POLICY "Admins can view all inspections" ON inspections
    FOR ALL USING (
        EXISTS (
            SELECT 1 FROM users 
            WHERE id = auth.uid()::integer 
            AND role = 'admin'
        )
    );

-- 6. 인덱스 생성 (성능 향상)
CREATE INDEX IF NOT EXISTS idx_users_username ON users(username);
CREATE INDEX IF NOT EXISTS idx_users_employee_id ON users(employee_id);
CREATE INDEX IF NOT EXISTS idx_inspections_user_id ON inspections(user_id);
CREATE INDEX IF NOT EXISTS idx_inspections_date ON inspections(inspection_date);
CREATE INDEX IF NOT EXISTS idx_inspections_equipment ON inspections(equipment_type, equipment_id); 
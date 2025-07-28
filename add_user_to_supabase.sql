-- 기존 사용자를 Supabase에 추가하는 SQL 스크립트
-- Supabase SQL Editor에서 실행하세요

-- 사용자 추가 (비밀번호: 123456)
INSERT INTO users (username, name, phone, employee_id, password_hash, role, active_status) 
VALUES (
    'testuser',  -- 실제 사용한 아이디로 변경하세요
    '테스트 사용자',  -- 실제 이름으로 변경하세요
    '010-1234-5678',  -- 실제 전화번호로 변경하세요
    '123456',  -- 실제 사번으로 변경하세요
    '$2b$12$LQv3c1yqBWVHxkd0LHAkOeKqGZqKqGZqKqGZqKqGZqKqGZqKqGZqK',  -- 실제 비밀번호 해시로 변경하세요
    'input',
    true
); 
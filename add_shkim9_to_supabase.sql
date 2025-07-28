-- shkim9 사용자를 Supabase에 추가하는 SQL 스크립트
-- Supabase SQL Editor에서 실행하세요

-- 사용자 추가 (비밀번호는 원래 설정한 것으로 변경하세요)
INSERT INTO users (username, name, phone, employee_id, password_hash, role, active_status) 
VALUES (
    'shkim9',
    '김시환',
    '010-9931-7672',
    '10140057',
    '$2b$12$LQv3c1yqBWVHxkd0LHAkOeKqGZqKqGZqKqGZqKqGZqKqGZqKqGZqK',  -- 실제 비밀번호 해시로 변경하세요
    'download',
    true
); 
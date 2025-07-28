#!/usr/bin/env python3
"""
현재 로그인한 사용자 정보를 확인하는 스크립트
"""

import sqlite3
import os

def check_local_users():
    """로컬 SQLite에서 사용자 정보 확인"""
    db_path = "instance/cascade_system.db"
    
    if not os.path.exists(db_path):
        print("❌ 로컬 데이터베이스 파일을 찾을 수 없습니다.")
        return
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # 사용자 목록 조회
        cursor.execute("SELECT id, username, name, phone, employee_id, role FROM users ORDER BY id")
        users = cursor.fetchall()
        
        print("📋 로컬 SQLite 사용자 목록:")
        print("-" * 60)
        for user in users:
            print(f"ID: {user[0]}, 아이디: {user[1]}, 이름: {user[2]}, 전화번호: {user[3]}, 사번: {user[4]}, 권한: {user[5]}")
        
        conn.close()
        
        if users:
            print("\n💡 위 사용자 중 하나를 Supabase에 추가해야 합니다.")
            print("   가장 최근에 가입한 사용자(ID가 큰 번호)가 현재 로그인한 사용자일 가능성이 높습니다.")
        
    except Exception as e:
        print(f"❌ 오류 발생: {e}")

if __name__ == "__main__":
    check_local_users() 
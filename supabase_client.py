import os
from supabase import create_client, Client
import logging
from dotenv import load_dotenv

# 환경 변수 로드
load_dotenv()

def get_supabase_client() -> Client:
    """
    Supabase 클라이언트를 생성하고 반환합니다.
    환경 변수에서 Supabase URL과 API 키를 가져옵니다.
    """
    supabase_url = os.environ.get("SUPABASE_URL")
    supabase_key = os.environ.get("SUPABASE_ANON_KEY")
    
    logging.info(f"Supabase URL: {supabase_url}")
    logging.info(f"Supabase Key: {supabase_key[:20] if supabase_key else 'None'}...")
    
    if not supabase_url or not supabase_key:
        logging.warning("⚠️  Supabase 환경 변수가 설정되지 않았습니다.")
        logging.warning("   로컬 SQLite를 사용합니다.")
        return None
    
    if supabase_url == "your-supabase-url" or supabase_key == "your-supabase-anon-key":
        logging.warning("⚠️  Supabase 환경 변수가 기본값으로 설정되어 있습니다.")
        logging.warning("   실제 Supabase 정보를 입력해주세요.")
        return None
    
    try:
        client = create_client(supabase_url, supabase_key)
        # 연결 테스트 (간단한 쿼리)
        response = client.table('users').select('count', count='exact').limit(1).execute()
        logging.info("✅ Supabase 연결 성공!")
        return client
    except Exception as e:
        logging.error(f"⚠️  Supabase 클라이언트 생성 실패: {e}")
        logging.warning("   로컬 SQLite를 사용합니다.")
        return None

# 전역 변수로 클라이언트 인스턴스 생성
try:
    supabase = get_supabase_client()
except Exception as e:
    logging.error(f"⚠️  Supabase 클라이언트 초기화 실패: {e}")
    supabase = None 
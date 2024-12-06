from google_auth_oauthlib.flow import InstalledAppFlow
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
import os.path
import pickle
from dotenv import load_dotenv
import sys

def get_resource_path(relative_path):
    """Get absolute path to resource, works for dev and for PyInstaller"""
    if getattr(sys, 'frozen', False):
        # PyInstaller로 패키징된 경우
        base_path = sys._MEIPASS
    else:
        # 일반 Python 스크립트로 실행되는 경우
        base_path = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(base_path, relative_path)

# .env 파일 로드
env_path = get_resource_path('config/.env')
load_dotenv(env_path)

# 설정 파일 경로
if getattr(sys, 'frozen', False):
    # PyInstaller로 패키징된 경우
    config_base = get_resource_path('config')
    TOKEN_FILE = os.path.join(config_base, 'token.pickle')
    CREDENTIALS_FILE = os.path.join(config_base, 'credentials.json')
else:
    # 일반 Python 스크립트로 실행되는 경우
    TOKEN_FILE = os.getenv('TOKEN_FILE', 'config/token.pickle')
    CREDENTIALS_FILE = os.getenv('CREDENTIALS_FILE', 'config/credentials.json')

SCOPES = ['https://www.googleapis.com/auth/adsense.readonly']

def get_credentials():
    """OAuth 인증 처리 및 credentials 반환"""
    creds = None

    try:
        if os.path.exists(TOKEN_FILE):
            with open(TOKEN_FILE, 'rb') as token:
                creds = pickle.load(token)

        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                try:
                    creds.refresh(Request())
                except Exception as refresh_error:
                    print(f"토큰 갱신 실패: {refresh_error}")
                    if os.path.exists(TOKEN_FILE):
                        os.remove(TOKEN_FILE)
                    return get_credentials()
            else:
                if not os.path.exists(CREDENTIALS_FILE):
                    raise FileNotFoundError(
                        f"인증 파일을 찾을 수 없습니다: {CREDENTIALS_FILE}"
                    )

                flow = InstalledAppFlow.from_client_secrets_file(
                    CREDENTIALS_FILE,
                    SCOPES
                )
                creds = flow.run_local_server(port=0)

            # 토큰 저장을 위한 디렉토리 생성
            token_dir = os.path.dirname(TOKEN_FILE)
            if not os.path.exists(token_dir):
                os.makedirs(token_dir, exist_ok=True)

            with open(TOKEN_FILE, 'wb') as token:
                pickle.dump(creds, token)

    except Exception as e:
        print(f"인증 처리 중 오류 발생: {str(e)}")
        raise

    return creds

def get_account_name(service):
    """AdSense 계정 이름 가져오기"""
    try:
        accounts_response = service.accounts().list().execute()

        if not accounts_response.get('accounts'):
            raise ValueError('AdSense 계정을 찾을 수 없습니다.')

        return accounts_response['accounts'][0]['name']
    except Exception as e:
        print(f"계정 정보 조회 중 오류 발생: {str(e)}")
        raise

def get_adsense_data():
    """AdSense 대시보드 데이터 조회"""
    try:
        service = build('adsense', 'v2', credentials=get_credentials())
        account_name = get_account_name(service)

        # 오늘 데이터
        today_response = service.accounts().reports().generate(
            account=account_name,
            dateRange='TODAY',
            metrics=['ESTIMATED_EARNINGS']
        ).execute()
        today_earnings = float(today_response['rows'][0]['cells'][0]['value']) if 'rows' in today_response else 0.0

        # 어제 데이터
        yesterday_response = service.accounts().reports().generate(
            account=account_name,
            dateRange='YESTERDAY',
            metrics=['ESTIMATED_EARNINGS']
        ).execute()
        yesterday_earnings = float(yesterday_response['rows'][0]['cells'][0]['value']) if 'rows' in yesterday_response else 0.0

        # 지난 7일 데이터
        seven_days_response = service.accounts().reports().generate(
            account=account_name,
            dateRange='LAST_7_DAYS',
            metrics=['ESTIMATED_EARNINGS']
        ).execute()
        seven_days_earnings = float(seven_days_response['rows'][0]['cells'][0]['value']) if 'rows' in seven_days_response else 0.0

        # 이번 달 데이터
        month_response = service.accounts().reports().generate(
            account=account_name,
            dateRange='MONTH_TO_DATE',
            metrics=['ESTIMATED_EARNINGS']
        ).execute()
        month_earnings = float(month_response['rows'][0]['cells'][0]['value']) if 'rows' in month_response else 0.0

        dashboard_data = {
            'today': {
                'earnings': today_earnings,
                'comparison': {'value': today_earnings - yesterday_earnings, 'percentage': ((today_earnings - yesterday_earnings) / yesterday_earnings * 100) if yesterday_earnings != 0 else 0.0}
            },
            'yesterday': {
                'earnings': yesterday_earnings,
                'comparison': {'value': 0.0, 'percentage': 0.0}  # 일단 0으로 설정
            },
            'last_7_days': {
                'earnings': seven_days_earnings
            },
            'this_month': {
                'earnings': month_earnings,
                'comparison': {'value': 0.0, 'percentage': 0.0}  # 일단 0으로 설정
            }
        }

        return dashboard_data

    except Exception as e:
        print(f"API Error: {str(e)}")
        return {
            'today': {'earnings': 0.0, 'comparison': {'value': 0.0, 'percentage': 0.0}},
            'yesterday': {'earnings': 0.0, 'comparison': {'value': 0.0, 'percentage': 0.0}},
            'last_7_days': {'earnings': 0.0},
            'this_month': {'earnings': 0.0, 'comparison': {'value': 0.0, 'percentage': 0.0}}
        }

    except Exception as e:
        print(f"[ERROR] API Error: {str(e)}")
        return {
            'today': {'earnings': 0.0, 'comparison': {'value': 0.0, 'percentage': 0.0}},
            'yesterday': {'earnings': 0.0, 'comparison': {'value': 0.0, 'percentage': 0.0}},
            'last_7_days': {'earnings': 0.0},
            'this_month': {'earnings': 0.0, 'comparison': {'value': 0.0, 'percentage': 0.0}}
        }
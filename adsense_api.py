from google_auth_oauthlib.flow import InstalledAppFlow
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
import os.path
import pickle
from dotenv import load_dotenv

# .env 파일 로드
load_dotenv()

SCOPES = ['https://www.googleapis.com/auth/adsense.readonly']
TOKEN_FILE = os.getenv('TOKEN_FILE', 'config/token.pickle')
CREDENTIALS_FILE = os.getenv('CREDENTIALS_FILE', 'config/credentials.json')

def get_credentials():
    """OAuth 인증 처리 및 credentials 반환"""
    creds = None
    
    if os.path.exists(TOKEN_FILE):
        with open(TOKEN_FILE, 'rb') as token:
            creds = pickle.load(token)
    
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(CREDENTIALS_FILE, SCOPES)
            creds = flow.run_local_server(port=0)
        
        with open(TOKEN_FILE, 'wb') as token:
            pickle.dump(creds, token)
    
    return creds

def get_account_name(service):
    """AdSense 계정 이름 가져오기"""
    accounts_response = service.accounts().list().execute()
    
    if not accounts_response.get('accounts'):
        raise ValueError('AdSense 계정을 찾을 수 없습니다.')
    
    return accounts_response['accounts'][0]['name']

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

        # 어제 데이터
        yesterday_response = service.accounts().reports().generate(
            account=account_name,
            dateRange='YESTERDAY',
            metrics=['ESTIMATED_EARNINGS']
        ).execute()

        # 지난 7일 데이터
        seven_days_response = service.accounts().reports().generate(
            account=account_name,
            dateRange='LAST_7_DAYS',
            metrics=['ESTIMATED_EARNINGS']
        ).execute()

        # 이번 달 데이터
        month_response = service.accounts().reports().generate(
            account=account_name,
            dateRange='MONTH_TO_DATE',
            metrics=['ESTIMATED_EARNINGS']
        ).execute()

        dashboard_data = {
            'today': {
                'earnings': float(today_response['rows'][0]['cells'][0]['value']) if 'rows' in today_response else 0.0,
                'comparison': {
                    'value': 0.0,
                    'percentage': 0.0
                }
            },
            'yesterday': {
                'earnings': float(yesterday_response['rows'][0]['cells'][0]['value']) if 'rows' in yesterday_response else 0.0,
                'comparison': {
                    'value': 0.0,
                    'percentage': 0.0
                }
            },
            'last_7_days': {
                'earnings': float(seven_days_response['rows'][0]['cells'][0]['value']) if 'rows' in seven_days_response else 0.0
            },
            'this_month': {
                'earnings': float(month_response['rows'][0]['cells'][0]['value']) if 'rows' in month_response else 0.0,
                'comparison': {
                    'value': 0.0,
                    'percentage': None
                }
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
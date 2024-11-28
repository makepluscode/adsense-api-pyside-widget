from google_auth_oauthlib.flow import InstalledAppFlow
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from datetime import datetime, timedelta
import json
import os.path
import pickle

SCOPES = ['https://www.googleapis.com/auth/adsense.readonly']
TOKEN_FILE = 'token.pickle'
CREDENTIALS_FILE = 'credentials.json'

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

        # 잔고 데이터
        try:
            payments_response = service.accounts().payments().list(
                account=account_name
            ).execute()
        except:
            payments_response = {'payments': []}

        dashboard_data = {
            'today': {
                'earnings': float(today_response['rows'][0]['cells'][0]['value']) if 'rows' in today_response else 0.0,
                'comparison': {
                    'value': 0.0,
                    'percentage': 0
                }
            },
            'yesterday': {
                'earnings': float(yesterday_response['rows'][0]['cells'][0]['value']) if 'rows' in yesterday_response else 0.0,
                'comparison': {
                    'value': 0.0,
                    'percentage': 0
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
            },
            'balance': {
                'current': float(payments_response['payments'][0]['amount']) if payments_response.get('payments') else 0.0,
                'last_payment': float(payments_response['payments'][1]['amount']) if len(payments_response.get('payments', [])) > 1 else 0.0
            }
        }

        return dashboard_data

    except Exception as e:
        return {
            'error': str(e),
            'message': 'AdSense API 호출 중 오류가 발생했습니다.',
            'data': {
                'today': {'earnings': 0.0, 'comparison': {'value': 0.0, 'percentage': 0.0}},
                'yesterday': {'earnings': 0.0, 'comparison': {'value': 0.0, 'percentage': 0.0}},
                'last_7_days': {'earnings': 0.0},
                'this_month': {'earnings': 0.0, 'comparison': {'value': 0.0, 'percentage': 0.0}},
                'balance': {'current': 0.0, 'last_payment': 0.0}
            }
        }

if __name__ == '__main__':
    result = get_adsense_data()
    print(json.dumps(result, ensure_ascii=False, indent=2))
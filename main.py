from google_auth_oauthlib.flow import InstalledAppFlow
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from datetime import datetime
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

def get_adsense_earnings():
    """AdSense 수익 정보 조회"""
    try:
        service = build('adsense', 'v2', credentials=get_credentials())
        account_name = get_account_name(service)
        today = datetime.now().strftime('%Y-%m-%d')
        
        response = service.accounts().reports().generate(
            account=account_name,
            dateRange='TODAY',
            metrics=['ESTIMATED_EARNINGS'],
            dimensions=['DATE']
        ).execute()
        
        if 'rows' in response:
            earnings = float(response['rows'][0]['cells'][1]['value'])
            return {
                'date': today,
                'estimated_earnings': earnings,
                'currency': 'USD'
            }
        
        return {
            'date': today,
            'estimated_earnings': 0.0,
            'currency': 'USD',
            'message': '데이터가 없습니다.'
        }
            
    except ValueError as ve:
        return {
            'error': str(ve),
            'message': 'AdSense 계정 접근 오류'
        }
    except Exception as e:
        return {
            'error': str(e),
            'message': 'AdSense API 호출 중 오류가 발생했습니다.'
        }

if __name__ == '__main__':
    result = get_adsense_earnings()
    print(json.dumps(result, ensure_ascii=False, indent=2))
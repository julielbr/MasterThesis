import requests                                                                   # type: ignore #ignore
from urllib.parse import urljoin
         

# LM Studio API-Connection
LM_STUDIO_API_URL = "http://192.168.1.101:1234/v1/chat/completions/"

HEADERS = {"Content-Type": "application/json"}
# Predefined URLs to be checked during scanning
URLS_TO_CHECK = [
    '/admin',
    '/api/Products/1',
    '/api/Users/1'
]

# Login Credentials
LOGIN_CREDENTIALS = {
    'email': 'admin@juice-sh.op',
    'password': 'admin123'
}

# User Roles and their Credentials
ROLES = {
    'guest': None,
    'user': {'email': 'user@juice.sh', 'password': 'user123'},
    'admin': {'email': LOGIN_CREDENTIALS['email'], 'password': 'admin123'}
}

# HTTP Methods to Test, --expand this if time (julle)
HTTP_METHODS = ['GET', 'POST']

def login(role, base_url):
    session = requests.Session()
    if role in ['user', 'admin']:
        login_url = urljoin(base_url, '/rest/user/login')
        response = session.post(login_url, json=ROLES[role])
        if response.status_code == 200:
            print(f'[+] Logged in as {role}')
        else:
            print(f'[-] Failed to log in as {role} (Status: {response.status_code})')
            return None
    return session

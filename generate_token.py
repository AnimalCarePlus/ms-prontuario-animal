import jwt
from datetime import datetime, timedelta, timezone

SECRET_KEY = 'super-secret-key'

def generate_token():
    now = datetime.now(timezone.utc)
    payload = {
        'sub': 'usuario_teste',
        'iat': now,
        'exp': now + timedelta(hours=2)
    }

    token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')

    print("Token JWT gerado:\n")
    print(token)

if __name__ == '__main__':
    generate_token()

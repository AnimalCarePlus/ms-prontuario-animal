import requests
from flask import request, jsonify
from functools import wraps
from dotenv import load_dotenv
import os

load_dotenv()
AUTH_VALIDATE_URL = os.getenv("AUTH_VALIDATE_URL")

def jwt_protected(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        auth_header = request.headers.get("Authorization")

        if not auth_header:
            return jsonify({"message": "Token não fornecido"}), 401

        
        token = auth_header.replace("Bearer ", "").strip()

        try:
            response = requests.get(
                AUTH_VALIDATE_URL,
                headers={"Authorization": token},
                timeout=5
            )

            if response.status_code == 204:
                
                return fn(*args, **kwargs)
            else:
                return jsonify({"message": "Token inválido ou expirado"}), 401

        except requests.RequestException as e:
            return jsonify({"message": "Erro ao validar token", "error": str(e)}), 500

    return wrapper

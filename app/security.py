from datetime import timedelta, datetime
from functools import wraps
from flask import session, jsonify, request
import hashlib, jwt, os

# Função que permite criptografar informações
def encrypt_hash(value: str) -> str:
  hash = hashlib.sha512()
  hash.update(value.encode('UTF-8'))
  
  return hash.hexdigest()

# Função que permite criar um token
def create_token(data: dict) -> str:
  data['exp'] = datetime.utcnow() + timedelta(hours=1)
  token = jwt.encode(payload=data, key=os.environ.get('SECRET_KEY'), algorithm="HS256")

  return token

# Função que permite decodificar o token
def decode_token(data: dict) -> dict:
  try:
    decoded_token = jwt.decode(jwt=data, key=os.environ.get('SECRET_KEY'), algorithms=['HS256'])
  except:
    return None

  return decoded_token

def login_required(f):
  @wraps(f)
  def decorated_function(*args, **kwargs):
    if( session.get('logged') == False or session.get('logged') is None ):
      return jsonify(message="Login is required!"), 401 # Unauthorized
    return f(*args, **kwargs)
  
  return decorated_function

def token_required(f):
  @wraps(f)
  def decorated_function(*args, **kargs):
    if( request.headers.get('X-access-token') is None or decode_token(request.headers.get('X-access-token')) is None ):
      return jsonify(message='Token is required!'), 401 # Unauthorized
    return f(*args, **kargs)
  
  return decorated_function
    
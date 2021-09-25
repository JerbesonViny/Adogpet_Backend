from sqlalchemy.exc import IntegrityError
from flask import jsonify, request, session
import asyncio

from app import app
from app.security import ( 
  encrypt_hash, create_token, decode_token, login_required, token_required
)
from app.database.schemas import User, users_schema
from app.controllers.usercontroller import (
  create_user, authorization
)

loop = asyncio.get_event_loop()

@app.route('/test-token/', methods=['GET',])
def home():
  data = request.headers.get('X-access-token')
  
  if( decode_token(data) is not None ):
    return jsonify(message="Valid token!")
  
  return jsonify(message="This token is invalid!")

@app.route('/register/', methods=['POST',])
def register():
  data = request.json # Captando os dados passados

  # Verificando se todos os campos foram preenchidos
  if( data.get('name') and data.get('email') and data.get('password') ):
    new_user = User(name=data['name'], email=data['email'], password=data['password'])

    try:
      user_uuid = loop.run_until_complete(create_user(new_user))

      if( user_uuid ):
        return jsonify(user_uuid=user_uuid), 201 # Created

      return jsonify(message="Não foi possível criar a sua conta, tente novamente!"), 400 # Bad Request
    except IntegrityError:
      return jsonify(message='Esse e-mail já está em uso, tente novamente com outro!'), 400 # Bad Request

  return jsonify(error="Preencha todos os campos!"), 400 # Bad Request

@app.route('/login/', methods=['POST',])
def login():
  data = request.json # Captando os dados passados

  # Verificando se todos os campos foram preenchidos
  if( data.get('email') and data.get('password') ):
    authorized = loop.run_until_complete(authorization(user=data))

    if( authorized is not None ):
      payload = users_schema.dump([authorized])[0]
      payload['uuid'] = str(payload['uuid'])
      token = create_token(payload)
      session['logged'] = True

      return jsonify(token=token), 200 # OK

    return jsonify(message="Não foi possível autenticar!", token=None), 401 # Unauthorized
    
  return jsonify(message="Preencha todos os campos!", token=None), 400 # Bad Request

@app.route('/logout/', methods=['GET',])
@login_required
@token_required
def logout():
  session.clear()

  return jsonify(message="Logout feito com sucesso!", token=None)
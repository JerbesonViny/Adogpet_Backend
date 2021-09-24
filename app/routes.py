from sqlalchemy.exc import IntegrityError
from flask import jsonify, request
import asyncio

from app import app
from app.security import encrypt_hash
from app.database.schemas import User, users_schema
from app.controllers.usercontroller import (
  create_user, authorization
)

loop = asyncio.get_event_loop()

@app.route('/', methods=['GET',])
def home():
  return jsonify(message="Hello world")

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
      return jsonify(message="Authorized!", data=users_schema.dump([authorized])), 200 # OK

    return jsonify(message="Não foi possível autenticar!"), 401 # Unauthorized
    
  return jsonify(message="Preencha todos os campos!"), 400 # Bad Request
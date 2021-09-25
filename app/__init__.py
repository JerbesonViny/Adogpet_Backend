from dotenv import load_dotenv
from flask import Flask
import os

load_dotenv() # Carregando todas as variáveis de ambiente

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')

from app import routes
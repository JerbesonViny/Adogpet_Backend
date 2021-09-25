from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
import os

# Criando a engine que faz comunicação com o banco
engine = create_async_engine(os.environ.get('DATABASE_URL'), echo=True)

# Sessão async
session = sessionmaker(future=True, class_=AsyncSession, bind=engine)
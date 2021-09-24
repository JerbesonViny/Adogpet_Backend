from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

# Caminho absoluto onde o banco de dados será armazenado
DATABASE_URL = "sqlite+aiosqlite:///app/database/example.db"

# Criando a engine que faz comunicação com o banco
engine = create_async_engine(DATABASE_URL, echo=True)

# Sessão async
session = sessionmaker(future=True, class_=AsyncSession, bind=engine)
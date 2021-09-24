import asyncio

from app.database.configuration import engine
from app.database.schemas import Base

# Função que permite criar as tabelas do banco de dados
async def create_tables():
  # Iniciando a engine e criando uma conexão com a mesma
  async with engine.begin() as conn:
    await conn.run_sync(Base.metadata.drop_all) # Aguardando apagar todas as tabelas
    await conn.run_sync(Base.metadata.create_all) # Aguardando criar todas as tabelas


asyncio.run( create_tables() )
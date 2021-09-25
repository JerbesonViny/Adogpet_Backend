from sqlalchemy.future import select
import asyncio

from app.database.configuration import session
from app.database.schemas import User
from app.security import encrypt_hash
import uuid

async def create_user(user: User) -> int:
  user.password = encrypt_hash(user.password)
  user.uuid = uuid.uuid4()

  async with session() as s:
    try:
      s.add(user)
      await s.commit()
      await s.refresh(user)
    except:
      await s.rollback()
      
      return None
    
    return user.uuid

async def authorization(user: dict) -> list:
  user['password'] = encrypt_hash(user['password'])

  async with session() as s:
    query = await s.execute(
      select(User.uuid, User.name, User.email).where(User.email == user['email'], User.password == user['password'])
    )

    return query.first()

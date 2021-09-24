from sqlalchemy.future import select

from app.database.configuration import session
from app.database.schemas import User
from app.security import encrypt_hash

async def create_user(user: User) -> int:
  user.password = encrypt_hash(user.password)

  async with session() as s:
    s.add(user)
    await s.commit()
    await s.refresh(user)

    return user.id

async def authorization(user: dict) -> list:
  user['password'] = encrypt_hash(user['password'])

  async with session() as s:
    query = await s.execute(
      select(User.id, User.name, User.email).where(User.email == user['email'], User.password == user['password'])
    )

    return query.first()

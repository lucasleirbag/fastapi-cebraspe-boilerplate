import asyncio
import os
import sys

from app.models import User
from app.repositories.user import UserRepository
from core.database import session
from core.database.standalone_session import standalone_session
from core.security.password import PasswordHandler


@standalone_session
async def create_default_user():
    username = os.getenv("DEFAULT_USER_USERNAME")
    email = os.getenv("DEFAULT_USER_EMAIL")
    password = os.getenv("DEFAULT_USER_PASSWORD")
    is_admin = os.getenv("DEFAULT_USER_IS_ADMIN", "true").lower() == "true"
    
    if not username or not email or not password:
        print("❌ Erro: Variáveis de ambiente obrigatórias não foram definidas:")
        print("   - DEFAULT_USER_USERNAME")
        print("   - DEFAULT_USER_EMAIL") 
        print("   - DEFAULT_USER_PASSWORD")
        print("   - DEFAULT_USER_IS_ADMIN (opcional, padrão: true)")
        sys.exit(1)

    user_repo = UserRepository(User, session)
    
    existing_user_email = await user_repo.get_by_email(email)
    if existing_user_email:
        print(f"✅ Usuário padrão já existe (email): {email}")
        return
    
    existing_user_username = await user_repo.get_by_username(username)
    if existing_user_username:
        print(f"✅ Usuário padrão já existe (username): {username}")
        return

    hashed_password = PasswordHandler.hash(password)
    user = await user_repo.create({
        "username": username,
        "email": email,
        "password": hashed_password,
        "is_admin": is_admin,
    })
    await session.commit()
    print(f"🎉 Usuário padrão criado com sucesso!")
    print(f"   Username: {username}")
    print(f"   Email: {email}")
    print(f"   Admin: {'Sim' if is_admin else 'Não'}")


if __name__ == "__main__":
    asyncio.run(create_default_user())

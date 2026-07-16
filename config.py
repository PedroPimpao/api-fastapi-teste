import os
from dotenv import load_dotenv

load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))

if not DATABASE_URL:
    raise RuntimeError(
        "A variavel de ambiente DATABASE_URL nao foi definida. "
        "Crie um arquivo .env com base no .env.example."
    )

import os
from dotenv import load_dotenv


from pathlib import Path
env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)


class Settings:
    PROJECT_TITLE: str = "Blog 🚀"
    PROJECT_DESCRIPTION: str = "SpeakWell 🗣️ Blog Website"
    PROJECT_VERSION: str = "1.0.0"

    # POSTGRES_USER = str = os.getenv("POSTGRES_USER")
    # POSTGRES_PASSWORD = str = os.getenv("POSTGRES_PASSWORD")
    # POSTGRES_SERVER = str = os.getenv("POSTGRES_SERVER", "localhost")
    # POSTGRES_PORT = int = os.getenv("POSTGRES_PORT", 5432)
    # POSTGRES_DB = str = os.getenv("POSTGRES_DB")

    DATABASE_URL = str = os.getenv("DATABASE_URL")
    
    SECRET_KEY = str = os.getenv("SECRET_KEY")
    ALGORITHM = str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES = int = 30
    UPLOAD_DIR = str = os.path.join(os.getcwd(), "uploads")

settings = Settings() #object to access Settings() class

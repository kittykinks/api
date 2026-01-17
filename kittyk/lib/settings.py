import os

from dotenv import load_dotenv


load_dotenv(override=True)


DISCORD_CLIENT_ID = os.getenv("DISCORD_CLIENT_ID")
DISCORD_CLIENT_SECRET = os.getenv("DISCORD_CLIENT_SECRET")
DISCORD_REDIRECT_URI = os.getenv("DISCORD_REDIRECT_URI")


DATABASE_URL = os.getenv("DATABASE_URL", "sqlite://:memory:")


LOGIN_NEXT_URL = os.getenv("LOGIN_NEXT_URL", "/")
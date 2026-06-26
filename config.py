import os
from pathlib import Path
from dotenv import load_dotenv

CAMINHO_BASE = Path(__file__).resolve().parent
load_dotenv(CAMINHO_BASE / ".env")

DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

if not DISCORD_TOKEN:
    raise ValueError("DISCORD_TOKEN não encontrado no arquivo .env")

if not OPENAI_API_KEY:
    raise ValueError("OPENAI_API_KEY não encontrado no arquivo .env")
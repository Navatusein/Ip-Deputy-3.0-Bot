import httpx

from bot.config import load_config

configs = load_config()
client = httpx.Client(base_url=configs.api_url, headers={"X-BOT-TOKEN": configs.api_token})
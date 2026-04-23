import os
import yaml

from loguru import logger
from dotenv import __all__, load_dotenv

load_dotenv()

try:
    with open('config/settings.yaml', 'r', encoding="utf-8") as data:
        config = yaml.load(data, Loader=yaml.FullLoader)

    logger.info("YAML config successfully loaded.")
except Exception as e:
    logger.error(f"Error while loading YAML: {e}")

config['youtrack_token'] = os.getenv('YOUTRACK_TOKEN')
config['telegram_token'] = os.getenv('TELEGRAM_TOKEN')
config['chat_id'] = os.getenv('CHAT_ID')
config['redis_url'] = os.getenv('REDIS_URL')
config['redis_port'] = os.getenv('REDIS_PORT')
config['pastebin_api_key'] = os.getenv('PASTEBIN_API_KEY')
config['chat_thread'] = os.getenv('CHAT_THREAD')

__all__ = ['config']
import yaml
from loguru import logger

try:
    with open('config/settings.yaml', 'r', encoding="utf-8") as data:
        config = yaml.load(data, Loader=yaml.FullLoader)

    logger.info("YAML config successfully loaded.")
except Exception as e:
    logger.error(f"Error while loading YAML: {e}")
from prometheus_client import start_http_server
from loguru import logger

def start_metrics_server(port = 8000):
    start_http_server(port)
    logger.info("Metrics server is up.")
import time

from typing import Any, Awaitable, Callable, Dict
from aiogram import BaseMiddleware
from aiogram.types import CallbackQuery, Message
from prometheus_client import Counter, Histogram

COMMANDS_COUNT = Counter(
    'bot_commands', 
    'Total commands processed', 
    ['handler_name', 'status']
)

LATENCY = Histogram(
    'bot_command_latency_seconds',
    'Latency of command processing in seconds',
    ['handler_name']
)

class MetricsMiddleware(BaseMiddleware):
    async def __call__(
            self, 
            handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
            event: Message, 
            data: Dict[str, Any]
            ) -> Any:
        handler_obj = data.get('handler')
        handler_name = handler_obj.callback.__name__ if handler_obj else 'unknown'

        start_time = time.perf_counter()
        try:
            result = await handler(event, data)
            COMMANDS_COUNT.labels(handler_name=handler_name, status='success').inc()
            return result
        except Exception as e:
            COMMANDS_COUNT.labels(handler_name=handler_name, status='error').inc()
            raise e
        finally:
            latency = time.perf_counter() - start_time
            LATENCY.labels(handler_name=handler_name).observe(latency)

class CallbacksMiddleware(BaseMiddleware):
    async def __call__(
            self, 
            handler: Callable[[CallbackQuery, Dict[str, Any]], Awaitable[Any]],
            event: CallbackQuery, 
            data: Dict[str, Any]
            ) -> Any:
        handler_obj = data.get('handler')
        handler_name = handler_obj.callback.__name__ if handler_obj else 'unknown'

        start_time = time.perf_counter()
        try:
            result = await handler(event, data)
            COMMANDS_COUNT.labels(handler_name=handler_name, status='success').inc()
            return result
        except Exception as e:
            COMMANDS_COUNT.labels(handler_name=handler_name, status='error').inc()
            raise e
        finally:
            latency = time.perf_counter() - start_time
            LATENCY.labels(handler_name=handler_name).observe(latency)
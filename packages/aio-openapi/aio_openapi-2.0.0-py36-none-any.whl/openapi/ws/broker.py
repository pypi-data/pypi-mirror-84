import abc
import asyncio
from typing import Any, Callable, Dict

HandlerType = Callable[[str, Any], None]


class Broker(abc.ABC):
    """Abstract class for pubsub brokers"""

    async def start(self) -> None:
        """
        Start broker
        """

    async def close(self) -> None:
        """
        Close broker
        """

    @abc.abstractmethod
    async def publish(self, channel: str, body: Dict) -> None:
        """Publish a new payload to a channel/exchange"""

    @abc.abstractmethod
    async def subscribe(self, channel: str, handler: HandlerType) -> None:
        """Bind the broker to a channel/exchange"""

    @abc.abstractmethod
    async def unsubscribe(self, channel: str) -> None:
        """Bind the broker to a channel/exchange"""

    def on_connection_lost(self, lost):
        pass


class LocalBroker(Broker):
    """A local broker, mainly for testing"""

    def __init__(self):
        self.binds = set()
        self.messages: asyncio.Queue = asyncio.Queue()
        self.worker = None
        self._stop = False
        self._handlers = set()

    async def start(self):
        if not self.worker:
            self.worker = asyncio.ensure_future(self._work())

    async def publish(self, channel, body):
        asyncio.get_event_loop().call_later(
            0.01, self.messages.put_nowait, (channel, body)
        )

    async def subscribe(self, key: str, handler: HandlerType) -> None:
        self.binds.add(key)
        self._handlers.add(handler)

    async def unsubscribe(self, key):
        self.binds.discard(key)

    async def close(self):
        self._stop = True
        if self.worker:
            self.messages.put_nowait((None, None))
            await self.worker
            self.worker = None

    async def _work(self):
        while True:
            key, body = await self.messages.get()
            if self._stop:
                break
            if key in self.binds:
                for handler in self._handlers:
                    await handler(key, body)

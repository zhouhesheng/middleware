import asyncio
from collections import deque


SS_QUEUE = deque(maxlen=20)


class SoftHardSemaphoreLimit(Exception):
    pass


class SoftHardSemaphore:

    def __init__(self, softlimit, hardlimit):
        self.softlimit = softlimit
        self.hardlimit = hardlimit
        self.softsemaphore = asyncio.Semaphore(value=softlimit)
        self.counter = 0
        self.method = None

    @staticmethod
    def get_queued():
        return list(SS_QUEUE)

    async def __aenter__(self, method):
        if self.counter >= self.hardlimit:
            raise SoftHardSemaphoreLimit(self.hardlimit)
        self.counter += 1
        self.method = method
        SS_QUEUE.append(self.method)
        await self.softsemaphore.acquire()

    async def __aexit__(self, exc_type, exc, tb):
        self.counter -= 1
        try:
            SS_QUEUE.remove(self.method)
        except ValueError:
            pass

        self.softsemaphore.release()

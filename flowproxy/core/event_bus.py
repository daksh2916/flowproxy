import asyncio
from collections import defaultdict

class EventBus:
    def __init__(self):
        self.subscribers = defaultdict(list)

    def subscribe(self, event_type, callback):
        self.subscribers[event_type].append(callback)

    async def emit(self, event_type, data):
        tasks = []
        for callback in self.subscribers[event_type]:
            tasks.append(asyncio.create_task(callback(data)))
        
        if tasks:
            await asyncio.gather(*tasks, return_exceptions=True)
            

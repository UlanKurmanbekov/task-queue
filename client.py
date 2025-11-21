import json
from uuid import uuid4
from typing import Callable, Any

import redis


class Task:
    def __init__(self, func: Callable, task_queue: 'RedisTaskQueue') -> None:
        self._func = func
        self._task_queue = task_queue

    def __call__(self, *args, **kwargs) -> Any:
        return self._func(*args, **kwargs)

    def delay(self, *args, **kwargs) -> str:
        task_id = str(uuid4())
        task = {
            'task_id': task_id,
            'task_name': f'{self._func.__module__}.{self._func.__name__}',
            'args': args,
            'kwargs': kwargs,
            'retries': 3,
            'status': 'pending'
        }
        self._task_queue.enqueue(json.dumps(task))
        return task_id


class RedisTaskQueue:
    def __init__(self, broker_url: str) -> None:
        self.broker = redis.from_url(broker_url)

    def task(self, func: Callable) -> 'Task':
        return Task(func, self)

    def enqueue(self, task: str) -> None:
        self.broker.lpush('tasks', task)

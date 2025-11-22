import json
import importlib
from typing import Any

from client import RedisTaskQueue


class Worker:
    def __init__(self, task_queue: 'RedisTaskQueue'):
        self.task_queue = task_queue

    def set_result(self, key: str, value: Any) -> None:
        self.task_queue.broker.set(key, json.dumps(value), ex=300)

    def run(self) -> None:
        while True:
            _, task = self.task_queue.broker.brpop('tasks', 0)

            try:
                task = json.loads(task)
            except Exception as e:
                print(f'Error {e}')
                continue

            task_id = task['task_id']

            module_name, func_name = task['task_name'].rsplit('.', 1)
            module = importlib.import_module(module_name)
            func = getattr(module, func_name)
            args = task['args']
            kwargs = task['kwargs']

            try:
                result = func(*args, **kwargs)
                self.set_result(f'result:{task_id}', {'status': 'success', 'result': result})
                print(f'The function was completed successfully. ID {task_id}')
            except Exception as e:
                print(f'Error: {e}')
                task['retries'] -= 1
                if task['retries'] > 0:
                    self.task_queue.enqueue(json.dumps(task))
                else:
                    print(f'The number of attempts has been exhausted. ID {task_id}')
                    task['status'] = 'failure'
                    self.set_result(f'result:{task_id}', {'status': 'failure', 'result': str(e)})

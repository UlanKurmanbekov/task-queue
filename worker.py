import json
import importlib

from client import RedisTaskQueue


class Worker:
    def __init__(self, task_queue: 'RedisTaskQueue'):
        self.task_queue = task_queue

    def run(self) -> None:
        while True:
            _, task = self.task_queue.broker.brpop('tasks', 0)
            task = json.loads(task)

            task_id = task['task_id']

            module_name, func_name = task['task_name'].rsplit('.', 1)
            module = importlib.import_module(module_name)
            func = getattr(module, func_name)
            args = task['args']
            kwargs = task['kwargs']

            try:
                result = func(*args, **kwargs)
                self.task_queue.broker.set(f'result:{task_id}', json.dumps(result))
                print(f'The function was completed successfully. ID {task_id}')
            except Exception as e:
                print(f'Error: {e}')
                task['retries'] -= 1
                if task['retries'] > 0:
                    self.task_queue.enqueue(json.dumps(task))
                else:
                    print(f'The number of attempts has been exhausted. ID {task_id}')
                    task['status'] = 'failure'
                    self.task_queue.broker.set(f'result:{task_id}', json.dumps(task))

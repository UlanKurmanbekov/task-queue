import time
from client import RedisTaskQueue

PORT = 6379

task_queue = RedisTaskQueue(f'redis://localhost:{PORT}')


@task_queue.task
def add(x, y):
    return x + y


@task_queue.task
def multiply(x, y):
    return x * y


@task_queue.task
def slow_task(seconds):
    time.sleep(seconds)
    return f"Completed after {seconds} seconds"


@task_queue.task
def failing_task():
    raise ValueError("This task is designed to fail")


@task_queue.task
def process_data(data):
    return {
        'original': data,
        'processed': data.upper() if isinstance(data, str) else data,
        'length': len(data) if hasattr(data, '__len__') else None
    }

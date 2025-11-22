from worker import Worker
from tasks import task_queue


worker = Worker(task_queue)
worker.run()

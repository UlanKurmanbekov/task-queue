# Redis Task Queue

Lightweight distributed task queue implementation using Python and Redis. Educational project.

## Features

- Background task execution
- Automatic retry mechanism (3 attempts)
- Result storage with 5-minute TTL
- Timeout handling

## Requirements

- Python 3.11+
- Redis 5.0+

## Installation

1. Clone the repository:
```bash
git clone https://github.com/UlanKurmanbekov/task-queue.git
cd task-queue
```

2. Install dependencies:
```bash
pip install redis
```

3. Start Redis:
```bash
redis-server
```

## Quick Start

**Terminal 1** - Start worker:
```bash
python run_worker.py
```

**Terminal 2** - Run demo:
```bash
python main.py
```

## Usage

1. Define tasks in `tasks.py`:
```python
from client import RedisTaskQueue

task_queue = RedisTaskQueue('redis://localhost:6379')

@task_queue.task
def add(x, y):
    return x + y
```

2. Use tasks in your code:
```python
from tasks import add

result = add.delay(5, 3)
output = result.get(timeout=10)
print(output)  # {'status': 'success', 'result': 8}
```

## Project Structure

```
task-queue/
├── client.py        # Task queue client
├── worker.py        # Worker implementation
├── tasks.py         # Example tasks
├── main.py          # Demo script
└── run_worker.py    # Worker starter
```

## Usage Examples

### Basic Task
```python
from tasks import add

# Background execution
result = add.delay(2, 3)
output = result.get(timeout=10)
```

### Multiple Tasks
```python
results = [add.delay(i, i*2) for i in range(10)]
outputs = [r.get(timeout=10) for r in results]
```

### Error Handling
```python
try:
    output = result.get(timeout=10)
    if output['status'] == 'success':
        print(output['result'])
except TimeoutError:
    print("Task timed out")
```

## Limitations

Missing:
- Task prioritization
- Monitoring
- Advanced error handling
- Task cancellation


## License

MIT
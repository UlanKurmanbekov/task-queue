from tasks import add, multiply, slow_task, failing_task, process_data


def main():
    print("=" * 60)
    print("Redis Task Queue Demo".center(60))
    print("=" * 60)

    print("\n[1] Adding two numbers asynchronously...")
    result = add.delay(5, 3)
    print(f"    Task ID: {result.task_id}")
    output = result.get(timeout=10)
    print(f"    Result: {output}")

    print("\n[2] Multiplying two numbers...")
    result = multiply.delay(4, 7)
    print(f"    Task ID: {result.task_id}")
    output = result.get(timeout=10)
    print(f"    Result: {output}")

    print("\n[3] Running a slow task (3 seconds)...")
    result = slow_task.delay(3)
    print(f"    Task ID: {result.task_id}")
    print("    Waiting for completion...")
    output = result.get(timeout=10)
    print(f"    Result: {output}")

    print("\n[4] Processing string data...")
    result = process_data.delay("hello world")
    print(f"    Task ID: {result.task_id}")
    output = result.get(timeout=10)
    print(f"    Result: {output}")

    print("\n[5] Queueing multiple tasks...")
    results = []
    for i in range(5):
        r = add.delay(i, i * 2)
        results.append(r)
        print(f"    Queued task {i + 1}: {r.task_id}")

    print("\n    Getting results...")
    for i, r in enumerate(results):
        output = r.get(timeout=10)
        print(f"    Task {i + 1}: {output}")

    print("\n[6] Testing failing task (will retry 3 times)...")
    result = failing_task.delay()
    print(f"    Task ID: {result.task_id}")
    print("    Check worker output to see retry attempts...")
    try:
        output = result.get(timeout=15)
        print(f"    Result: {output}")
    except TimeoutError:
        print("    Task timed out (expected for failing task)")

    print("\n[7] Processing different data types...")

    print("    - Processing list...")
    result = process_data.delay([1, 2, 3, 4, 5])
    output = result.get(timeout=10)
    print(f"      Result: {output}")

    print("    - Processing string...")
    result = process_data.delay("python rocks!")
    output = result.get(timeout=10)
    print(f"      Result: {output}")

    print("\n[8] Chaining operations...")
    result1 = add.delay(10, 5)
    print(f"    First operation (10 + 5): {result1.task_id}")
    output1 = result1.get(timeout=10)
    print(f"    Result 1: {output1}")

    if output1['status'] == 'success':
        result2 = multiply.delay(output1['result'], 2)
        print(f"    Second operation (result * 2): {result2.task_id}")
        output2 = result2.get(timeout=10)
        print(f"    Final Result: {output2}")

    print("\n" + "=" * 60)
    print("Demo completed successfully!".center(60))
    print("=" * 60)


if __name__ == '__main__':
    print("\n⚠️  Make sure Redis is running and worker is started!")
    print("    Start worker with: python run_worker.py\n")

    try:
        main()
    except TimeoutError as e:
        print(f"\n❌ Error: {e}")
        print("   Make sure the worker is running (python run_worker.py)")
    except ConnectionError as e:
        print(f"\n❌ Connection Error: {e}")
        print("   Make sure Redis is running (redis-server)")
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")

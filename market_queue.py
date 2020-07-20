import time
from typing import List

import asyncio
from asyncio import Queue


async def worker(name: str, queue: Queue):

    while not queue.empty():
        sleep_for = await queue.get()
        print(f'{name} is started')
        await asyncio.sleep(sleep_for)
        queue.task_done()
        print(f'{name} has work for {sleep_for:.2f} seconds')


async def get_total_time(queue: List[int], n: int):
    work_queue = asyncio.Queue()

    for work in queue:
        work_queue.put_nowait(work)

    tasks = []
    for i in range(n):
        task = asyncio.create_task(worker(f'worker-{i}', work_queue))
        tasks.append(task)

    started_at = time.monotonic()

    await work_queue.join()
    total_work_for = time.monotonic() - started_at

    for task in tasks:
        task.cancel()

    print(f'{n} workers has works in parallel for {total_work_for:.0f} seconds')
    print('====')


if __name__ == "__main__":
    asyncio.run(get_total_time(queue=[5, 3, 4], n=1))  # 12
    asyncio.run(get_total_time(queue=[10, 2, 3, 3], n=2))  # 2
    asyncio.run(get_total_time(queue=[2, 3, 10], n=2))  # 12

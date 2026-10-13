"""
resilience.py - Các kịch bản Tiêm lỗi (Fault Injection) và Phản ví dụ kinh điển.
Bao gồm:
- F1: Timeout & Graceful degradation
- F4: Queue backpressure (Producer bị dừng khi consumer quá tải)
- F7: BẪY CHẾT NGƯỜI: time.sleep() làm đóng băng toàn bộ Event Loop vs asyncio.sleep()
- F8: Race condition trên biến đếm chung khi thiếu asyncio.Lock
"""

from __future__ import annotations
import time
import asyncio
from typing import List, Dict, Any


async def demo_f7_blocking_trap(use_fix: bool = False, duration_sec: float = 1.0) -> Dict[str, Any]:
    """
    Minh họa Lỗi F7: Gọi blocking time.sleep() bên trong coroutine.
    - Bản Lỗi (use_fix=False): Gọi time.sleep() -> đóng băng hoàn toàn Event Loop,
      khiến các tác vụ nền (như Heartbeat/Timer) bị tê liệt, độ trễ heartbeat vọt lên cao.
    - Bản Chuẩn (use_fix=True): Gọi asyncio.sleep() -> nhường quyền kiểm soát,
      Heartbeat vẫn đập đều đặn 100ms một lần.
    """
    heartbeat_ticks = 0
    t_start = time.perf_counter()

    async def heartbeat():
        nonlocal heartbeat_ticks
        while True:
            heartbeat_ticks += 1
            await asyncio.sleep(0.1)  # Đập mỗi 100ms

    async def worker_job():
        if not use_fix:
            # SAI LẦM: time.sleep chặn đứng cả event loop thread
            time.sleep(duration_sec)
        else:
            # ĐÚNG ĐẮN: asyncio.sleep nhường quyền điều khiển
            await asyncio.sleep(duration_sec)

    hb_task = asyncio.create_task(heartbeat())
    await worker_job()
    hb_task.cancel()
    try:
        await hb_task
    except asyncio.CancelledError:
        pass

    elapsed = time.perf_counter() - t_start
    return {
        "mode": "fixed_async_sleep" if use_fix else "broken_blocking_sleep",
        "elapsed_sec": round(elapsed, 3),
        "heartbeat_ticks": heartbeat_ticks,
        "is_loop_frozen": (heartbeat_ticks <= 1 and not use_fix),
        "explanation": (
            "Loop hoạt động mượt mà, heartbeat đập liên tục." if use_fix
            else "EVENT LOOP BỊ ĐÓNG BĂNG HOÀN TOÀN do time.sleep()! Không tác vụ nào khác được chạy!"
        )
    }


async def demo_f8_race_condition(use_lock: bool = False, num_tasks: int = 100) -> Dict[str, Any]:
    """
    Minh họa Lỗi F8: Race Condition trong async khi có read-await-write.
    Nếu không có Lock, việc xen kẽ context switch giữa read và write làm sai lệch giá trị counter.
    """
    counter = 0
    lock = asyncio.Lock()

    async def increment_task():
        nonlocal counter
        if use_lock:
            async with lock:
                val = counter
                await asyncio.sleep(0.001)  # Nhường quyền giả lập thao tác async
                counter = val + 1
        else:
            val = counter
            await asyncio.sleep(0.001)  # Điểm xen kẽ nguy hiểm: task khác chen vào đọc val cũ
            counter = val + 1

    tasks = [asyncio.create_task(increment_task()) for _ in range(num_tasks)]
    await asyncio.gather(*tasks)

    return {
        "use_lock": use_lock,
        "expected_counter": num_tasks,
        "actual_counter": counter,
        "is_race_detected": counter != num_tasks,
        "message": (
            f"Tính toán chính xác: counter = {counter}" if counter == num_tasks
            else f"XẢY RA RACE CONDITION! Mong đợi {num_tasks} nhưng chỉ đạt {counter} do thiếu Lock!"
        )
    }

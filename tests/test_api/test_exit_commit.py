from __future__ import annotations

import asyncio
import time

from agently_stage import Stage


def test_async_exit_commit():
    run_count = []

    stage = Stage(auto_close=True)

    async def task_func_1(count=1):
        run_count.append(f"task_func_{count}")
        await asyncio.sleep(1)
        if count == 15:
            run_count.append("Done")
            return
        stage.go(task_func_1, count + 1)

    async def test_func_1():
        run_count.append("test_func_1")
        stage.go(task_func_1)

    stage.go(test_func_1)
    time.sleep(1)
    assert "test_func_1" in run_count
    assert "task_func_1" in run_count
    assert "Done" not in run_count

    # 不能正常退出单测说明有问题

# -*- coding: utf-8 -*-
"""This module defines the `Ticker` class."""
import queue
import threading
import time
from typing import Optional


class Ticker:
    """Delivery of ticks at intervals.

    Once started the `Ticker` will periodically make a boolean "tick" of True
    available through the `tick` method. Uncollected ticks will not stack or queue
    up, and the Ticker will continue to tick regardless. When stopped `tick` will
    return False, and any uncollected tick will be lost.

    Example::

        ticker = Ticker()
        ticker.start(5)

        while ticker.tick():
            execute_task()

    """
    def __init__(self) -> None:
        self._lock = threading.Lock()
        self._tick: Optional[queue.LifoQueue] = None

    def _schedule(self, interval: int) -> None:
        time.sleep(interval)
        while True:
            self._lock.acquire()
            # There is a non-zero risk of _tick being set to None between entering the loop and acquiring the lock
            # thus it's better to perform the check here rather than as the while expression.
            if not self._tick:
                break
            # Only use one queue spot for ticking, the second spot is reserved for stopping.
            if self._tick.qsize() == 0:
                self._tick.put(True)
            self._lock.release()
            time.sleep(interval)

    def start(self, interval: int) -> None:
        """Start the ticker.

        Args:
            interval: Time between ticks.

        Raises:
            Exception if already running.

        """
        self._lock.acquire()
        if self._tick:
            raise RuntimeError("Ticker already started")
        self._tick = queue.LifoQueue(2)
        self._lock.release()
        thread = threading.Thread(target=self._schedule, args=(interval,), daemon=True)
        thread.start()

    def tick(self) -> bool:
        """Wait for a tick to be delivered.

        Will return immediately if ticker is stopped.

        Returns:
            True on tick, False if stopped.

        """
        if not self._tick:
            return False
        tick = self._tick.get()
        if not tick:
            self._lock.acquire()
            self._tick = None
            self._lock.release()
        return tick

    def stop(self) -> None:
        """Stop the ticker."""
        self._lock.acquire()
        if self._tick and self._tick.qsize() != 2:
            self._tick.put(False)
        self._lock.release()

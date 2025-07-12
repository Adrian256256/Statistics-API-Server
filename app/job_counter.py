"""Job Counter Module
This module provides a thread-safe job counter for managing job IDs.
It includes a class `JobCounter` that encapsulates the counter and provides methods to increment and retrieve the current value.
"""
from threading import Lock

class JobCounter:
    """
    A thread-safe class for managing the job counter.
    """

    def __init__(self):
        self.counter = 0
        self.lock = Lock()

    def increment_and_get(self):
        """
        Increment the job counter and return the current value.
        """
        with self.lock:
            self.counter += 1
            return self.counter

    def get_value(self):
        """
        Get the current value of the job counter.
        """
        with self.lock:
            return self.counter

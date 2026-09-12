import time
from typing import Callable, Any

def execute_with_timeout(func: Callable, args: tuple = (), timeout_sec: float = 3.0, max_retries: int = 2) -> Any:
    """Executes a function with per-node retries and global timeout enforcement."""
    attempt = 0
    start_time = time.time()
    
    while attempt <= max_retries:
        try:
            if (time.time() - start_time) > timeout_sec:
                raise TimeoutError(f"Global pipeline execution timeout exceeded ({timeout_sec}s)")
                
            return func(*args)
        except Exception as e:
            attempt += 1
            if attempt > max_retries:
                raise e
            time.sleep(0.1)
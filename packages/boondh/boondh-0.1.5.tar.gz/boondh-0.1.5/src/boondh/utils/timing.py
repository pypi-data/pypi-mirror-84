import time
from contextlib import contextmanager
from datetime import datetime
from typing import Iterator

# Simplest - generator-iterator based
@contextmanager
def timer(code_block_name: str) -> Iterator[None]:
    """Prints the time taken to execute a given code block.

    Args:
        code_block_name (str): Description of your codeblock

    Usage:
        with timer("for loop 100,000,000"):
            _ = [x for x in range(100_000_000)]

        prints #=> [for loop 100,000,000] completed in 4 seconds.. 
    """
    start_time = time.time()
    # yields the control to the with statement
    yield
    # executed after with code block execution
    execution_time = time.time() - start_time
    print(f"[{code_block_name}] completed in {execution_time:.0f} seconds..")


# Return Start Date and time
# just to show the use of `as` assignment in the `with` statement
@contextmanager
def timer_v2(code_block_name: str) -> Iterator[datetime]:
    """Prints the time taken to execute a given code block.

    Args:
        code_block_name (str): Description of your codeblock

    Yields:
        str: Execution start date time ISO 8601 format
    """
    start_time = time.time()
    # yields the value to the with statement
    yield datetime.now()
    # executed after with code block execution
    execution_time = time.time() - start_time
    print(f"[{code_block_name}] completed in {execution_time:.0f} seconds..")

if __name__ == "__main__":
    # sample use
    with timer("for loop 100,000,000"):
        _ = [x for x in range(100_000_000)]
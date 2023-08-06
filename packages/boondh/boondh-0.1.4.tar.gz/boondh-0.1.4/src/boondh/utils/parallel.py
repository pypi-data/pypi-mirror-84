from traceback import format_exc
from tqdm import tqdm
from math import sqrt
from inspect import getfullargspec
from multiprocessing import Pool, cpu_count
from functools import partial
from typing import Iterable, List, Tuple, Union, Any, Callable, Dict
import logging

log = logging.getLogger(__name__)


def mp_func(
    func: Callable[..., Any],
    data_arg_name_in_func: str,
    data: Iterable[Any],
    chunksize: Union[str, int] = "auto",
    total: Union[int, None] = None,
    ordered: bool = True,
    *args: Tuple[Any, ...],
    **kwargs: Dict[str, Any],
) -> Union[List[Any], None]:
    """Apply given function on each element of data in parallel and show progress bar..

    Args:
        func (Callable): the python function to be applied
        data_arg_name_in_func (str): argument name in `func` which requires data point from data iterable
        data (Iterable): iterable with data points
        chunksize (str, int): 'auto' or None for automatic calc, int for specific chunksize
        total (int, None): size of the iterable, required when len is not possible
        ordered (bool): if ordered is desired in results, set to false if need faster processing
        args: positional args which will be supplied to the given `func`
        kwargs: keyword args which will be supplied to the given `func`


    Returns:
        list: result with each value as a result of application of function `func` 
        on each point in the given `data` iterable


    Example:
    To parallelize given `base_func` function: 
        >>> def base_func(value, sq=True):
                if sq: return value ** 2
                return value
        >>> data = [0, 1, 2, 3, 4]
        >>> results = mp_func(base_func, 'value', data, sq=True)
        >>> print(results)
        [0, 1, 4, 9, 16]
        >>> results = mp_func(base_func, 'value', data, sq=False)
        >>> print(results)
        [0, 1, 2, 3, 4]
    """

    func_args = getfullargspec(func).args
    skip_sanity_check = False
    try:
        total = len(data)
    except Exception:
        skip_sanity_check = True
        assert total, "Need total.."

    # Sanity checks
    assert isinstance(data, Iterable), "data should be an iterable.."

    assert (
        data_arg_name_in_func in func_args
    ), f"{data_arg_name_in_func} is not an argument of {func.__name__} function that you provided.."
    assert total > 1, f"len(data) should be > 1, but is {total}"
    assert len(args) + len(kwargs) + 1 == len(
        func_args
    ), f"{len(args)} + {len(kwargs)} + 1 != {len(func_args)}\nCheck args func_args are {func_args}"

    # for better user experience
    cpus = cpu_count()
    log.info(f"CPUS: {cpus}")

    # Returns a new partial object which when called will behave
    # like func called with the positional arguments args and keyword arguments kwargs.
    _new_func = partial(func, *args, **kwargs)
    results = None

    try:
        # sanity check
        if not skip_sanity_check:
            _ = _new_func(**{data_arg_name_in_func: data[-1]})

        if not chunksize or isinstance(chunksize, str):
            if chunksize == "auto":
                chunksize = int(sqrt(total) * cpus / 3)
            else:
                logging.warning(
                    f"chunksize can't be {chunksize} use 'auto' or any int value..using auto..")
                chunksize = int(sqrt(total) * cpus / 3)
            log.info(f"chunksize: {chunksize}")

        # actual processing
        with Pool(cpus) as pool:
            if ordered:
                results = list(
                    tqdm(pool.imap(_new_func, data,
                                             chunksize=chunksize), total=total)
                )
            else:
                results = list(
                    tqdm(pool.imap_unordered(_new_func, data, chunksize=chunksize), total=total)
                )
    except TypeError:
        log.info(
            f"Please make sure that args and kwargs provided are valid for {func.__name__} function.."
        )
        log.exception(format_exc())
    except Exception:
        log.exception(format_exc())
    finally:
        log.info("Done..")

    return results


def _sample_base_func(value: int, sq: bool = True):
    if sq:
        return value ** 2
    return value


def _sample_parallel_main():
    from boondh import timer
    logging.basicConfig()
    log.setLevel(logging.DEBUG)
    log.info("Starting mp_func on 100_000_000 sample points..")
    # Sample Usage
    # function to be applied

    with timer("Ordered"):
        results = mp_func(_sample_base_func, "value", data=range(
            0, 100_000_000), chunksize=200, sq=True)

        print(results[33])

    with timer("Un-ordered"):
        results = mp_func(_sample_base_func, "value", data=range(
            0, 100_000_000), chunksize=200, ordered=False, sq=True)

        print(results[33])


if __name__ == "__main__":
    _sample_parallel_main()

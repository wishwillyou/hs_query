from concurrent.futures import ProcessPoolExecutor
from multiprocessing import cpu_count
pool = ProcessPoolExecutor(max_workers=cpu_count()-1)


def multi_process(func, params_list):
    return list(pool.map(func, params_list))

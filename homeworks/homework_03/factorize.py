
import logging
from time import time, ctime, sleep
from multiprocessing import Process, Semaphore, Pool, cpu_count, current_process
  
logging.basicConfig(level=logging.DEBUG, format='%(threadName)s %(message)s')

def factorize_sync(numbers):
    name = current_process().name
    print(f"Start process {name}: {ctime()}")
    result = [[i for i in range(1, num + 1) if num % i == 0] for num in numbers]
    print(f"End work process {name}: {ctime()}")
    return result

def factorize_semaphore(number: int, semaphore = None):
    name = current_process().name
    print(f"Start process {name}: {ctime()}")
    with semaphore:
        result = [i for i in range(1, number + 1) if number % i == 0]
        print(result)
    print(f"End work process {name}: {ctime()}")
    return result

def factorize_map(number: int):
    name = current_process().name
    print(f"Start process {name}: {ctime()}")
    result = [i for i in range(1, number + 1) if number % i == 0]
    print(result)
    print(f"End work process {name}: {ctime()}")
    return result
  

if __name__ == "__main__":    
    
    numbers = [1065100, 2065101, 3065102, 4065103, 1065104, 2065105, 3065106, 4065107, 1065100, 2065101, 3065102, 4065103, 1065104, 2065105, 3065106, 4065107]

    start = time()
    f = factorize_sync(numbers)
    end = time()
    print(f)
    logging.debug(f'Time of calculations: {round(end - start, 2)}')

    print("-"*20+'\n')
    sleep(1)

    process = []
    semaphore = Semaphore(cpu_count())
    start = time()
    for i in range(len(numbers)):
        pr = Process(target=factorize_semaphore, args=(numbers[i], semaphore,))
        pr.start()
        process.append(pr)
    [pr.join() for pr in process]
    end = time()
    logging.debug(f'Time of calculations: {round(end - start, 2)}')
    
    print("-"*20+'\n')
    sleep(1)
    
    process = []
    start = time()
    with Pool(cpu_count()) as pool:
        process = pool.map_async(factorize_map, numbers)
        pool.close()
        pool.join()
    end = time()
    #print(process)
    logging.debug(f'Time of calculations: {round(end - start, 2)}')


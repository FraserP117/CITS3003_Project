import threading

'''
An example of how to use "Locks" to deal with race conditions
among multiple Threads.
'''

count = 0

# thread_job now takes the Lock as an argument:
def thread_job(lock):
    # without a lock - "count" would be the locus
    # of a race condition:
    global count
    for i in range(1000000):
        with lock: # add the Lock
            count = count + 1

def main():
    # threading now uses threading.RLock() to prevent any
    # race conditions

    lock = threading.RLock() # this is the lock

    number_of_threads = 4
    threads = []
    for i in range(number_of_threads):
        thread = threading.Thread(
            target = thread_job,
            args = (lock,), # lock the current thread (it now "owns" the current code exec)
            daemon = True
        )
        thread.start()
        threads.append(thread)

    for thread in threads:
        thread.join()

    print("COUNT: ", count)
    print("EXPECTED COUNT: ", 4 * 1000000)

    if count != 4 * 1000000:
        print("RACE CONDITION!!!!!!!!")
    else:
        print("NO Race Condition!")

if __name__ == '__main__':
    main()

'''
Note:

This is still poorly programmed - it suffers from an isssue called "thrashing"
* all threads are attempting to modify the same variable
* only one thread can access the "count" variable at any given time, due to the lock
* the code takes signifigantly longer to exec thereby - the count value is constantly being
  moved in and out of many regesters.
* it can be difficult to mannage shared memory between threads.
'''

import threading

'''
Some sort of "job" to be done
'''
def thread_job(msg):
    print("{}:{}".format(threading.current_thread().name, msg))

def main():

    msgs = [
        "A message executing in parallel???",
        "yet another???",
        "DU YOR FAHVZ!!!!!!",
        "how much wood did the wood-chuck chuck???"
    ]

    threads = []
    for msg in msgs:
        '''
        * Target: the function that the thread will execute
        * args: the tuple of arguments that the function will parse to
          the function - must end with an "," at the end!
        * daemon: if True, the threaddies when the master process stops
          running
        '''
        thread = threading.Thread(
            target = thread_job,
            args = (msg,),
            daemon = True
        )
        thread.start()
        threads.append(thread)

    '''
    If we want to wait for all a thread to complete its task;
    calling thread.join() will acomplish this for any given thread.
    '''
    for thread in threads:
        thread.join()

    print("All Done!")

if __name__ == "__main__":
    main()

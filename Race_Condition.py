import threading

count = 0

def thread_job():
    # oh no; count changed by all threads concurrently!
    global count
    for i in range(1000000):
        count = count + 1

def main():
    number_of_threads = 4
    threads = []
    for i in range(number_of_threads):
        thread = threading.Thread(
            target = thread_job,
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

if __name__ == '__main__':
    main()

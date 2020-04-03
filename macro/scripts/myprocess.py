import multiprocessing

def task(pid):
    print ("my result")
    return 0

def main():
    multiprocessing.freeze_support()
    pool = multiprocessing.Pool()
    cpus = multiprocessing.cpu_count()
    results = []
    print ("max cpu : ", cpus)
    for i in range(0, cpus):
        result = pool.apply_async(task, args=(i,))
        results.append(result)

    pool.close()
    pool.join()

#    for result in results:
#        print(result.get())

if __name__=="__main__":
   main()

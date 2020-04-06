import multiprocessing
from multiprocessing import Pool, cpu_count
import time

class mytask():
      def __init__(self, i=None, ik=None):
          self.printname = i
          self.newname = ik
      def output(self):
          print(self.printname)
          return 0      
      def output2(self):
          print(self.newname)
          return 0      

def task(pid):
    print("pid" , pid)
    print ("my result")
    print (multiprocessing.current_process().name)
    return 0

def main():
    t1 = time.time()
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
    print("multiprocessing time : ", int((time.time() - t1)*1000000))
  
    print(" ")
    print("Pool : ")
    t2 = time.time()
    selectors = 8
    pool2 = Pool(processes=cpus)
    results2 = [pool2.apply_async(task, (s,)) for s in range(selectors)]
    while results2:
       for r in results2:
          if r.ready():
             results2.remove(r)

    print(" ")
    print("Pool2 : ")
    t3 = time.time()
    selectors3 = ["my","task","is","good","!!!"]
    pool3 = Pool(processes=cpus)
    M = mytask("aa")
    M.output()
    a = mytask(ik = "abs")
    a.output2()
    
    results3 = [pool3.apply_async(M.output, (s,)) for s in selectors3]
    while results3:
       for r in results3:
          if r.ready():
             results3.remove(r)

    print("Pool time : ", int((time.time() - t3)*1000000))
#    time.sleep(1)
  

#    for result in results:
#        print(result.get())

if __name__=="__main__":
   main()

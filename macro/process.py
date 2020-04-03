from logger import log, supports_color
import sys
from array import array
import ROOT
import os
import enums
import time
from time import localtime, asctime
from multiprocessing import Pool, cpu_count

class ProgressBar():

      def __init__(self,ntotal=None,text=None,width=None,init_t=None):
          self.ntotal = ntotal
          self.text = text
          self.init_t = init_t
          self.width = width or 40

      def update(self,n):
          bar = '[%-'+str(self.width)+'s] %.f%% %.2f s'
          frac = float(n)/float(self.ntotal)
          print_time = time.time() - self.init_t
          sys.stdout.write('\r')
          inc = int(frac * float(self.width))
          line=enums.BLUEBOLD
          if self.text is not None:
             line+='%-17s:  '%(str(self.text)[:20])
          line+=bar % ('='*inc, frac*100., print_time)
          line+=enums.UNSET
          sys.stdout.write(line)
          sys.stdout.flush()
          
      def finalize(self):
           sys.stdout.write('\n')


class Processor():
      
      def __init__(self,ncores): 
          self.ncores = ncores

      def __selector__(self):
          print("test")
                
      def __process__(self,selectors):
          log().info("Starting Job: %s"%(asctime(localtime())))

          if not self.ncores:   ncores = min(4, cpu_count())
          else: ncores = min(self.ncores, cpu_count())
          
          log().info("Lighting up %d cores!!!"%(ncores))
          ti = time.time()

          selectors = __selector__()
          pool = Pool(processes=ncores)
          results = [pool.apply_async(__process_selector__, (s,)) for s in selectors]

def __process_selector__(ie):
    print("test")
       

from logger import log, supports_color
import sys
from array import array
import ROOT
import os
import enums

class ProgressBar():

      def __init__(self,ntotal=None,text=None,width=None):
          self.ntotal = ntotal
          self.text = text
          self.width = width or 40

      def update(self,n):
          bar = '[%-'+str(self.width)+'s] %.f%%'
          frac = float(n)/float(self.ntotal)
          sys.stdout.write('\r')
          inc = int(frac * float(self.width))
          line=enums.BLUEBOLD
          if self.text is not None:
             line+='%-17s:  '%(str(self.text)[:20])
          line+=bar % ('='*inc, frac*100.)
          line+=enums.UNSET
          sys.stdout.write(line)
          sys.stdout.flush()
          
      def finalize(self):
           sys.stdout.write('\n')


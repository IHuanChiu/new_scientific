from logger import log, supports_color
import sys
from array import array
import ROOT
import os
import enums
import time
from time import localtime, asctime
from multiprocessing import Pool, cpu_count
from utils.helpers import ProgressBar
from tran import tran_process
sys.path.append('/Users/chiu.i-huan/Desktop/new_scientific/macro/utils/')
sys.path.append('/Users/chiu.i-huan/Desktop/new_scientific/macro/scripts/')
from slimming import DisableBranch
from utils.cuts import PreEventSelection, findx2yshift, findadccut
from printInfo import checkTree

class Processor():
      
      def __init__(self,ifile=None,ofile=None,ncores=None,nevents=None,tree=None,efile=None): 
          # config
          self.tree = tree
          self.ncores = ncores
          self.nevents = nevents
          self.ifile = ifile
          self.ofile = ofile
          self.efile = efile
          
          # members
          self.T = None
          self.skimmingtree = None
          self.drawables = []
          self.Nevents = None

      def register(self,drawables):
          """
          :param drawables: single or list of ROOT drawables or plots (collection of drawables)
          """
          if not isinstance(drawables, list):
              drawables = [drawables]
          self.drawables += drawables

      def mainprocess(self):
          log().info("Starting Job: %s"%(asctime(localtime())))
          selector_job_list = self.__get_selector__()
          self.__process__(selector_job_list)
          self.__outputs__()

      def __get_selector__(self):
          log().info("Preparing jobs...")
          tree = DisableBranch(self.tree)
          if self.nevents:   self.Nevents = min(self.nevents, self.tree.GetEntries())
          else: self.Nevents = self.tree.GetEntries()

          self.skimmingtree = PreEventSelection(self.ifile, tree, self.Nevents) # this is ROOT.TEventList

          self.T = tran_process(ifile=self.ifile, tree=self.tree, event_list=self.skimmingtree ,efile=self.efile)         
          self.register(self.T.tree_list)
          self.register(self.T.hist_list)
     
          selectorjob_list = [SelectorCfg(i,eventlist = self.skimmingtree, tran=self.T) for i in range(self.Nevents)]

          return selectorjob_list 
                
      def __process__(self,selectorjob_list):
          if not self.ncores:   ncores = min(2, cpu_count())
          else: ncores = min(self.ncores, cpu_count())

          log().info("Lighting up %d cores!!!"%(ncores))
          ti = time.time()
          prog = ProgressBar(ntotal=len(selectorjob_list),text="Processing ntuple",init_t=ti)

          self.T.h1_event_cutflow.Fill(0,self.tree.GetEntries())         
 
          pool = Pool(processes=ncores)
          results = [pool.apply_async(__process_selector__, (s,)) for s in selectorjob_list]

          #TODO:sgel only retune result of 1 events/ 1 jobs
#          nevproc=0
#          while results:
#             for r in results:             
#                if r.ready():
#                   sgel = r.get()
#                   results.remove(r)
#                   nevproc+=1
#             if prog: prog.update(nevproc)          
#             time.sleep(0.05)
#          prog.finalize()
#          print(sgel.tran.h2_cutflow_x.GetEntries())

          # temp 
          nevproc=0
          for s in selectorjob_list:
             __process_selector__(s)
             nevproc+=1
             if prog: prog.update(nevproc)
          prog.finalize()
          print(self.T.h2_cutflow_x.GetEntries())

      def __outputs__(self):
          log().info("Printing output...")
          fout = ROOT.TFile( self.ofile, 'recreate' )
          __print_output__(fout, self.drawables)
          checkTree(self.T.tout,self.Nevents)

def __process_selector__(sgel):
    sgel.tran.tran_adc2e(sgel.ie)
    return sgel
       
def __print_output__(ofile, Drawables):
    ofile.cd()
    for idraw in Drawables:
       idraw.Write()
    ofile.Close()

class SelectorCfg(object):
      def __init__(self,ie=None,eventlist=None,tran=None):
          self.ie = ie
          self.eventlist = eventlist
          self.tran = tran



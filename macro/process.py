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
      
      def __init__(self,ifilelist=None,ofile=None,ncores=None,nevents=None,efile=None,dtype=None): 
          # config
          self.ncores = ncores
          self.nevents = nevents
          self.ifilelist = ifilelist
          self.ofile = ofile
          self.efile = efile
          self.dtype = dtype
          
          # members
          self.ifilename = None
          self.tree = None
          self.ifile = None
          self.T = None
          self.skimmingtree = None
          self.drawables = dict()
          self.Nevents = None

      def register(self,ifile, drawables):
          """
          :param drawables: single or list of ROOT drawables or plots (collection of drawables)
          """
          if not isinstance(drawables, list):
              drawables = [drawables]
          self.drawables[ifile] = drawables

      def mainprocess(self):
          log().info("Starting Job: %s"%(asctime(localtime())))
          neventsum, selector_job_list = self.__get_selector__()
          self.__process__(neventsum, selector_job_list)
          self.__outputs__()

      def __get_selector__(self):
          log().info("Preparing jobs...")
          selectorjob_list = list()          
          alle, sele = 0,0
          #TODO use TCahin for multi-file
          for self.ifilename in self.ifilelist:
             self.ifile = ROOT.TFile(self.ifilename)
             self.tree = self.ifile.Get("eventtree")  
             self.tree = DisableBranch(self.tree)

             if self.nevents:   self.Nevents = min(self.nevents, self.tree.GetEntries())
             else: self.Nevents = self.tree.GetEntries()
             self.skimmingtree = PreEventSelection(self.ifilename, self.tree, self.Nevents) # this is ROOT.TEventList
             alle += self.Nevents
             sele += self.skimmingtree.GetN()     

          log().info("Current Tpye : %s "%(self.dtype))
          log().info("Total passed events : %s / %s (by PreEventSelection)"%(sele,alle))

          self.T = tran_process(ifile=self.ifilename, tree=self.tree, event_list=self.skimmingtree ,efile=self.efile, dtype=self.dtype)        
          self.T.h1_event_cutflow.Fill(0,alle)
          self.register(self.ifilename, self.T.drawables) 

          selectorjob_list = [SelectorCfg(run_id=i, tran=self.T) for i in range(sele)]
          return sele, selectorjob_list 
                
      def __process__(self,neventsum, selectorjob_list):
          if not self.ncores:   ncores = min(2, cpu_count())
          else: ncores = min(self.ncores, cpu_count())

          log().info("Lighting up %d cores!!!"%(ncores))
          ti = time.time()
          prog = ProgressBar(ntotal=neventsum,text="Processing ntuple",init_t=ti)

          #TODO : Pool is no avaiable now : return a result (sgel) for 1 event/job, need to merge them
#          pool = Pool(processes=ncores)
#          results = [pool.apply_async(__process_selector__, (s,)) for s in selectorjob_list] # run the jobs
#          nevproc=0
#          while results:
#             for r in results:             
#                if r.ready():
#                   sgel = r.get()
#                   nevproc+=sgel.eventlist.GetN()
#                   self.register(sgel.ifile, sgel.drawable)
#                   results.remove(r)
#             if prog: prog.update(nevproc)          
#          prog.finalize()

          # temp : single core
          nevproc=0
          for s in selectorjob_list:
             __process_selector__(s)
             nevproc+=1
             if prog: prog.update(nevproc)
          if prog: prog.finalize()

      def __outputs__(self):
          log().info('Printing output...')
          for ifile, drawobjects in self.drawables.items():
             subProc = self.ofile+ifile.split("/")[-1]
             fout = ROOT.TFile( subProc, 'recreate' )
             __print_output__(fout, drawobjects)
          checkTree(self.T.tout,self.Nevents)

def __process_selector__(sgel):
    sgel.tran.tran_adc2e(sgel.run_id)
    return sgel
       
def __print_output__(ofile, Drawables):
    ofile.cd()
    for idraw in Drawables:
       idraw.Write()
    ofile.Close()

class SelectorCfg(object):
      def __init__(self,ifile=None,tree=None,eventlist=None,efile=None, run_id=None, tran=None):
          self.ifile = ifile
          self.tree = tree          
          self.eventlist = eventlist
          self.efile = efile
          self.run_id = run_id
          self.tran = tran
          self.drawable = None



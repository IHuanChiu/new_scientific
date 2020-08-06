from logger import log, supports_color
import sys
from array import array
import glob,ROOT
import os
import enums
import time
from time import localtime, asctime

class ProgressBar():

      def __init__(self,ntotal=None,text=None,width=None,init_t=None):
          self.ntotal = ntotal
          self.text = text
          self.init_t = init_t
          self.width = width or 40

      def update(self,n):
          bar = '[%-'+str(self.width)+'s] %.f%% %.1f s'
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

def GetInputList(inputFolder):
    inputDict = list()
    if ".root" in inputFolder : 
       inputDict.append(inputFolder)
       return inputDict

    subFolders = glob.glob(inputFolder+"/*.root")
    for subFolder in subFolders:
       inputDict.append(subFolder)

#    for subFolder in subFolders:
#        subProc = subFolder.split("/")[-1]
#        inputDict[subProc] = glob.glob(subFolder+"/*.root")

    return inputDict

def GetInitUnixTime(flist):
    _ifile = ROOT.TFile(flist)# first file
    _tree = _ifile.Get("eventtree")
    _tree.Draw("unixtime >> temp_h1","Entry$ == 1","") # first event
    _h1 = ROOT.gDirectory.Get("temp_h1")
    return _h1.GetXaxis().GetBinCenter( _h1.GetMaximumBin() )

def GetTChain(inputFolder,treename):
    _list=GetInputList(inputFolder)
    chain = ROOT.TChain(treename)
    for _l in _list:
       chain.AddFile(_l)
    return chain    

def createRatioCanvas(Name = "cs", w = 1200, h = 800):
    cRatioCanvas = ROOT.TCanvas(Name,"",0,0,int(w),int(h))
    cRatioCanvas.GetFrame().SetBorderMode(0)
    cRatioCanvas.GetFrame().SetBorderSize(0)
    cRatioCanvas.SetBorderMode(0)
    cRatioCanvas.SetBorderSize(0)
    cRatioCanvas.SetFillStyle(0)
    cRatioCanvas.SetFillColor(0)
    cRatioCanvas.SetRightMargin(0.15)
    cRatioCanvas.SetWindowSize( int(w + (w-cRatioCanvas.GetWw())), int(h + (h-cRatioCanvas.GetWh())) )
    return cRatioCanvas

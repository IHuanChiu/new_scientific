import time
import numpy
import ROOT
import root_numpy 
from root_numpy import hist2array, array2hist, tree2array
import root_numpy.tmva
import uproot

def main(aa=None):
   if aa is None: bb = 10
   else: bb= aa
   print(bb)
   ff=ROOT.TFile("/Users/chiu.i-huan/Desktop/parallel_test.root","recreate")
   ff.cd()
   aaa = numpy.array([1,2,3])
   h1=ROOT.TH1D("aa","aa",3,0,10)
   array2hist(aaa,h1)
   h1.Write()
   ff.Write()
   
if __name__=="__main__":
   main(100)

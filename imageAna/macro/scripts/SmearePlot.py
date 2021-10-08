import sys,os,random,math,time,ROOT,argparse, ctypes
from ROOT import TFile, TTree, gROOT, TCut, gDirectory, TMinuit, Long, Double, TMath, AddressOf
gROOT.SetBatch(1)
from root_numpy import hist2array, array2hist, tree2array
import numpy as np

inputname="/Users/chiu.i-huan/Desktop/new_scientific/imageAna/run/figs/repro_3Dimage.CdTe_30MeV_forpaper.root"
outputname=inputname.replace(".root","_Smeared.root")
fint=ROOT.TFile(inputname,"read")
outlist=[]
for i in range(16):
   _h=fint.Get("h"+str(i))
   h=_h.Clone()
   # === Smeared empty data ===
   _array=hist2array(h)
   _array[np.where(_array == 0)]=0.0000000000001
   array2hist(_array,h)
   outlist.append(h)

fout=ROOT.TFile(outputname,"recreate")
fout.cd()
for h in outlist:
   h.Write()
fout.Write()
print(outputname)

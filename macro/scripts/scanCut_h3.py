import sys,os,random,math,time,ROOT,argparse, ctypes
from ROOT import TFile, TTree, gROOT, TCut, gDirectory, TMinuit, Long, Double, TMath, AddressOf
from root_numpy import hist2array, array2hist, tree2array
import numpy as np

cutrangeMin=0
cutrangeMax=100
cutstep=5
name=input("path of file:")
if not os.path.exists(name): 
   print("no this root file!")
   exit(0)
f=ROOT.TFile(name,"read")

name2=name.replace(".root","_scancut.root")
fout=ROOT.TFile(name2,"recreate")
#h3=f.Get("MLEM_3Dimage")
h3=f.Get("MLEM_3Dimage_h12_iteration0")
h3_array=hist2array(h3)
nbins=h3.GetNbinsX()

fout.cd()

for i in range(cutrangeMin,cutrangeMax,cutstep):
   hist_final=ROOT.TH3D("MLEM_final_{}".format(i),"MLEM_final_{}".format(i),nbins,-20,20,nbins,-20,20,nbins,-20,20)
   h3_array_temp=h3_array
   w=np.where(h3_array_temp <  i)
   h3_array_temp[w]=0
   array2hist(h3_array_temp,hist_final)
   hist_final.Write()
print("output : {}".format(name2))
fout.Write()

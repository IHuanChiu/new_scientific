import sys,os,random,math,time,ROOT,argparse, ctypes
from ROOT import TFile, TTree, gROOT, TCut, gDirectory, TMinuit, Long, Double, TMath, AddressOf
from root_numpy import hist2array, array2hist, tree2array
import numpy as np

cutrange=900

f=ROOT.TFile("/Users/chiu.i-huan/Desktop/mytesth3output_sr_outputname.root","read")
fout=ROOT.TFile("/Users/chiu.i-huan/Desktop/mytesth3output_sr_outputname_scancut.root","recreate")
h3=f.Get("MLEM_3Dimage")
h3_array=hist2array(h3)

fout.cd()

for i in range(100,cutrange,10):
   hist_final=ROOT.TH3D("MLEM_final_{}".format(i),"MLEM_final_{}".format(i),40,-20,20,40,-20,20,40,-20,20)
   h3_array_temp=h3_array
   w=np.where(h3_array_temp <  i)
   h3_array_temp[w]=0
   array2hist(h3_array_temp,hist_final)
   hist_final.Write()

fout.Write()

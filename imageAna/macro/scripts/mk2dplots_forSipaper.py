import sys,os,ROOT,time
sys.path.append('/Users/chiu.i-huan/Desktop/new_scientific/imageAna/macro/utils/')
sys.path.append('/Users/chiu.i-huan/Desktop/new_scientific/imageAna/macro/')
from ROOT import gSystem, gPad, gDirectory, gStyle
from helpers import createRatioCanvas, ProgressBar
from logger import log
from root_numpy import hist2array, array2hist, tree2array
import numpy as np
ROOT.gErrorIgnoreLevel = ROOT.kWarning
__location__ = os.path.realpath(
        os.path.join(os.getcwd(), os.path.dirname(__file__)))
ROOT.gROOT.LoadMacro( __location__+'/AtlasStyle/AtlasStyle.C')
ROOT.SetAtlasStyle()

#inputname_list=["/Users/chiu.i-huan/Desktop/new_scientific/imageAna/run/root/MLEM_output/myMLEMoutput_1111_mlemall_iteration30.root"]
inputname_list=["/Users/chiu.i-huan/Desktop/new_scientific/imageAna/run/figs/repro_3Dimage.Si_30MeV_forSipaper.root"]

def mk2dplots(h_list):
    index=0
    for _h in h_list:
       index=index+1
       cv = createRatioCanvas("cv_"+str(index), 1000, 900)
       outname = "/Users/chiu.i-huan/Desktop/hist_Si_"+_h.GetName()+".pdf"
       _h2=_h.Clone()
       _array=hist2array(_h)
       _array[np.where(_array == 0)]=0.0000000001
       array2hist(_array,_h2)
       _h2.SetStats(0)
       _h2.SetTitle("Image; X[mm]; Y[mm]")
       _h2.RebinX(4); _h2.RebinY(4)
       _h2.GetXaxis().CenterTitle()
       _h2.GetYaxis().CenterTitle()
       _h2.GetZaxis().SetRangeUser(0, 8)
       gStyle.SetPalette(53)
       _h2.Draw("colz")
       cv.SaveAs(outname)
       
for _if in inputname_list:
   fint=ROOT.TFile(_if,"read")
   h_list=[]
   h=fint.Get("h1")# 0 
   h_list.append(h)
   h=fint.Get("h2")# 22.5
   h_list.append(h)
   h=fint.Get("h4")# 67.5
   h_list.append(h)
   h=fint.Get("h7")# 135
   h_list.append(h)

   mk2dplots(h_list)
      

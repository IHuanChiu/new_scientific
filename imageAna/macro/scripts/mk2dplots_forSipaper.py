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

#inputname="/Users/chiu.i-huan/Desktop/new_scientific/imageAna/run/root/MLEM_output/myMLEMoutput_1111_mlemall_iteration30.root"
#inputname="/Users/chiu.i-huan/Desktop/new_scientific/imageAna/run/figs/repro_3Dimage.Si_30MeV_forSipaper.root" #(x:y)
inputname="/Users/chiu.i-huan/Desktop/new_scientific/imageAna/run/figs/repro_3Dimage.Si_30MeV_forSipaper_yx.root" #(y:x)
plot_list=["h0","h1","h2","h3","h4","h5","h6","h7","h8","h9","h10","h11","h12","h13","h14","h15"]

def mk2dplots(h_list):
    index=0
    RebinSize, Zrange = 4, 8
    for _h in h_list:
       index=index+1
       cv = createRatioCanvas("cv_"+str(index), 1000, 900)
       outname = "/Users/chiu.i-huan/Desktop/new_scientific/imageAna/run/figs/Scan2DPlotsForPaper/hist_Si_"+_h.GetName()+"_yx.pdf"
       _h2=_h.Clone()
       _array=hist2array(_h)
       _array[np.where(_array == 0)]=0.0000000000001
       array2hist(_array,_h2)
       _h2.SetStats(0)
       _h2.SetTitle("Image; X [mm]; Y [mm]")
       _h2.RebinX(RebinSize); _h2.RebinY(RebinSize)
       _h2.GetXaxis().CenterTitle()
       _h2.GetYaxis().CenterTitle()
       _h2.GetZaxis().SetRangeUser(0, Zrange)
       gStyle.SetPalette(53)
       _h2.Draw("colz")
       cv.SaveAs(outname)
    print("Output in : {}".format(outname))

if __name__ == "__main__":  
   fint=ROOT.TFile(inputname,"read")
   h_list=[]
   for _pname in plot_list:
      h=fint.Get(_pname) 
      h_list.append(h)
   mk2dplots(h_list)
      

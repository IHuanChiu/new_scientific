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
#ROOT.SetAtlasStyle()

nplots=40
Ymaxrange=12
_outname=input("output name is : ")
if _outname == '':
   _outname="mlem_image"

#inputname_list=["/Users/chiu.i-huan/Desktop/new_scientific/imageAna/run/root/MLEM_output/myMLEMoutput_1111_mlemall_iteration30.root"]
inputname_list=["/Users/chiu.i-huan/Desktop/new_scientific/imageAna/run/root/MLEM_output/myMLEMoutput_35MeV_iteration5.root"]

def namelist(_name):
    if _name == "x": return ["Y [mm]", "Z [mm]"]
    if _name == "y": return ["X [mm]", "Z [mm]"]
    if _name == "z": return ["X [mm]", "Y [mm]"]

def setrange(_h, _axis,_up,_down):
    _h.GetXaxis().SetRangeUser(-20, 20)
    _h.GetYaxis().SetRangeUser(-20, 20)
    _h.GetZaxis().SetRangeUser(-20, 20)
    if _axis == "x": _h.GetXaxis().SetRangeUser(_down, _up)
    if _axis == "y": _h.GetYaxis().SetRangeUser(_down, _up)
    if _axis == "z": _h.GetZaxis().SetRangeUser(_down, _up)

def doslice(hist3d,outname,axisname):
    name = "/Users/chiu.i-huan/Desktop/new_scientific/imageAna/run/figs/3Dslices/hist_"+outname+"_"+axisname+".pdf"
    cv  = createRatioCanvas("cv_"+axisname, 1000, 900)
    cv.SetLeftMargin(0.1)
    cv.Print(name + "[", "pdf")
    _scan_axis="xyz"
    scan_axis=_scan_axis.replace(axisname,"")
    titlename=namelist(axisname)
    for i in range(nplots):                   
       _h3temp = hist3d.Clone()
       _u, _d = (20 - (40./nplots)*i), (20 - (40./nplots)*(i+1))
       setrange(_h3temp, axisname, _u, _d)
       _h2temp = _h3temp.Project3D(scan_axis)
       _h2=_h2temp.Clone()
       _array=hist2array(_h2temp)
       _array[np.where(_array == 0)]=0.001
       array2hist(_array,_h2)
       _h2.SetStats(0)
       _h2.SetTitle("slice %s %.1f mm"%(axisname,(_d+_u)/2.)) 
       _h2.GetXaxis().SetTitle(titlename[0])
       _h2.GetYaxis().SetTitle(titlename[1])
       _h2.GetZaxis().SetRangeUser(0, Ymaxrange)
       gPad.SetLogz(0)
       gStyle.SetPalette(62)
       _h2.Draw("colz")
       cv.Print(name, "pdf") 
    cv.Print(name + "]", "pdf");

for _if in inputname_list:
   f_mlem=ROOT.TFile(_if,"read")
   h3=f_mlem.Get("MLEM_3Dimage")
   doslice(h3,_outname,"x")
   doslice(h3,_outname,"y")
   doslice(h3,_outname,"z")
      
log().info("Path of pdf: {}".format("/Users/chiu.i-huan/Desktop/new_scientific/imageAna/run/figs/3Dslices/"))

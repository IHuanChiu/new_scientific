import sys,os,ROOT,time
sys.path.append('/Users/chiu.i-huan/Desktop/new_scientific/imageAna/macro/utils/')
sys.path.append('/Users/chiu.i-huan/Desktop/new_scientific/imageAna/macro/')
from ROOT import gSystem, gPad, gDirectory, gStyle
from helpers import createRatioCanvas, ProgressBar
from logger import log
from root_numpy import hist2array, array2hist, tree2array
import numpy as np
from scipy import ndimage, misc
ROOT.gErrorIgnoreLevel = ROOT.kWarning
__location__ = os.path.realpath(
        os.path.join(os.getcwd(), os.path.dirname(__file__)))
ROOT.gROOT.LoadMacro( __location__+'/AtlasStyle/AtlasStyle.C')
ROOT.SetAtlasStyle()

#inputname_list=["/Users/chiu.i-huan/Desktop/new_scientific/imageAna/run/root/MLEM_output/myMLEMoutput_1111_mlemall_iteration30.root"]
#inputname_list=["/Users/chiu.i-huan/Desktop/new_scientific/imageAna/run/root/MLEM_output/myMLEMoutput_30MeV_iteration100.root"]
inputname_list=["/Users/chiu.i-huan/Desktop/new_scientific/imageAna/run/root/MLEM_output/myMLEMoutput_30MeV_cutT10_10per_Lyaxis_Yshift_1p25_mlem_forpaper_iteration100.root"]

nplots=20
Zmaxrange=25# check slice of 3D plot
print("input name is : {}".format(inputname_list))
_outname=input("output name is : ")
if _outname == '':
   _outname="mlem_image"


def namelist(_name):
    # if you use root2vedo.py :
    # (root->vedo): x->Z; y->X; z->Y; -20~20 -> 0~40
    #if _name == "x": return ["X", "Y [mm]", "Z [mm]"]
    #if _name == "y": return ["Y", "Z [mm]", "X [mm]"]
    #if _name == "z": return ["Z", "X [mm]", "Y [mm]"]
    if _name == "x": return ["Z", "X [mm]", "Y [mm]"]#for paper
    if _name == "y": return ["X", "Z [mm]", "Y [mm]"]#for paper
    if _name == "z": return ["Y", "Z [mm]", "X [mm]"]#for paper

def setrange(_h, _axis,_up,_down):
    _h.GetXaxis().SetRangeUser(-20, 20)
    _h.GetYaxis().SetRangeUser(-20, 20)
    _h.GetZaxis().SetRangeUser(-20, 20)
    if _axis == "x": _h.GetXaxis().SetRangeUser(_down, _up)
    if _axis == "y": _h.GetYaxis().SetRangeUser(_down, _up)
    if _axis == "z": _h.GetZaxis().SetRangeUser(_down, _up)

def doslice(hist3d,outname,axisname):
    _scan_axis="xyz"
    scan_axis=_scan_axis.replace(axisname,"")
    titlename=namelist(axisname)
    name = "/Users/chiu.i-huan/Desktop/new_scientific/imageAna/run/figs/3Dslices/hist_"+outname+"_"+titlename[0]+".pdf"
    cv  = createRatioCanvas("cv_"+titlename[0], 1000, 900)
    cv.SetLeftMargin(0.1)
    cv.Print(name + "[", "pdf")
    _hist_list=[]

    # === because the rotation at root2vedo.py ===
    _h3array=hist2array(hist3d)
    _angle=105
    #_h3array=ndimage.rotate(_h3array,_angle,axes=(1,2),reshape=False)  
    #_h3array=ndimage.rotate(_h3array,180,axes=(0,2),reshape=False)  
    #_h3array=ndimage.rotate(_h3array,180,axes=(1,0),reshape=False)  
    _h3array[np.where(_h3array < 0.5)]=0.001
    array2hist(_h3array,hist3d)

    for i in range(nplots):                   
       _h3temp = hist3d.Clone()
       #_h3temp.SetTitle(";X [mm];Y [mm];Z [mm]")#for root plots
       _h3temp.SetTitle(";Z [mm];X [mm];-Y [mm]")#for paper (vedo plts)
       _u, _d = (20 - (40./nplots)*(i)), (20 - (40./nplots)*(i+1))
       setrange(_h3temp, axisname, _u, _d)
       _h2temp = _h3temp.Project3D(scan_axis)
       #_h2=_h2temp.Clone()
       _h2=ROOT.TH2D("h2_{}".format(i),"h2_{}".format(i),40,0,40,40,0,40)
       _array=hist2array(_h2temp)
       _array[np.where(_array < 0.5)]=0.001
       array2hist(_array,_h2)
       _h2.SetStats(0)
       _h2.SetTitle("slice %s %.1f mm"%(titlename[0],(_d+_u)/2.)) 
       _h2.GetXaxis().SetTitle(_h2temp.GetXaxis().GetTitle())
       _h2.GetYaxis().SetTitle(_h2temp.GetYaxis().GetTitle())
       _h2.GetXaxis().CenterTitle()
       _h2.GetYaxis().CenterTitle()
       _h2.GetZaxis().SetRangeUser(0, Zmaxrange)
       gPad.SetLogz(0)
       gPad.SetLeftMargin(0.15)
       gStyle.SetPalette(62)
       _hist_list.append(_h2)
       _h2.Draw("colz")
       cv.Print(name, "pdf") 
    cv.Print(name + "]", "pdf");

    # for paper
    for i in range(len(_hist_list)):                   
       _h=ROOT.TH2D("h_{}".format(i),"h_{}".format(i),40,0,40,40,0,40)
       _hori=_hist_list[i]
       _arrayori=hist2array(_hori)
       _arrayori[np.where(_arrayori == 0)]=0.1
       array2hist(_arrayori,_h)
       _u, _d = (40 - (40./len(_hist_list))*i), (40 - (40./len(_hist_list))*(i+1))
       cv2  = createRatioCanvas("cv2_{}".format(i)+titlename[0], 1000, 900)
       name2=name.replace("3Dslices/","3Dslices/allplots/")
       name2=name2.replace(".pdf","{0}to{1}_{2}.pdf".format(_d,_u,titlename[0]))
       _h.SetTitle("{0};{1};{2}".format(titlename[0],_h2temp.GetXaxis().GetTitle(),_h2temp.GetYaxis().GetTitle()))
       _h.GetXaxis().CenterTitle()
       _h.GetYaxis().CenterTitle()
       _h.GetZaxis().SetRangeUser(0, Zmaxrange)
       _h.Draw("colz")
       _h.SetName("hist_{0}_{1}to{2}".format(titlename[0],int(_d),int(_u)))
       _h.Write()
       cv2.Print(name2)

if __name__=="__main__":
   f_outname=""
   for _if in inputname_list:
      f_mlem=ROOT.TFile(_if,"read")
      f_outname=_if.replace(".root","_fitSlice.root")
      f_out=ROOT.TFile(f_outname,"recreate")
   #   h3=f_mlem.Get("MLEM_3Dimage")
   #   h3=f_mlem.Get("MLEM_3Dimage_h15_iteration14")
      h3=f_mlem.Get("MLEM_3Dimage_iteration50")
      f_out.cd()
      doslice(h3,_outname,"x")
      doslice(h3,_outname,"y")
      doslice(h3,_outname,"z")
      
   log().info("Path of pdf: {}".format("/Users/chiu.i-huan/Desktop/new_scientific/imageAna/run/figs/3Dslices/"))
   log().info("Path of output: {}".format(f_outname))

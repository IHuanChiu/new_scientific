import sys,os,ROOT,time
sys.path.append('/Users/chiu.i-huan/Desktop/new_scientific/macro/utils/')
sys.path.append('/Users/chiu.i-huan/Desktop/new_scientific/macro/')
from ROOT import gSystem
from helpers import createRatioCanvas, ProgressBar
from logger import log
from root_numpy import hist2array, array2hist, tree2array
import numpy as np
ROOT.gErrorIgnoreLevel = ROOT.kWarning
__location__ = os.path.realpath(
        os.path.join(os.getcwd(), os.path.dirname(__file__)))
ROOT.gROOT.LoadMacro( __location__+'/AtlasStyle/AtlasStyle.C')
ROOT.SetAtlasStyle()

def dofit(hist):
    f1=ROOT.TF1("f1","gaus",-20,20)
    hist.Fit("f1","QR")
    constant, mean, sigma = f1.GetParameter(0), f1.GetParameter(1), f1.GetParameter(2)
    chi2=f1.GetChisquare()
    return sigma,chi2

name_list=["mlem","osem"]
n_iterations,n_angles=100, 16
#prog = ProgressBar(ntotal=n_iterations*len(name_list),text="Performance",init_t=time.time())
#nevproc=0
for _if in name_list:
   
   f_mlem=ROOT.TFile("/Users/chiu.i-huan/Desktop/new_scientific/run/root/MLEM_output/myMLEMoutput_1116_{}_iteration100.root".format(_if),"read")
      
   hsigx=ROOT.TH1F("per_{}_hx".format(_if),"per_{}_hx".format(_if),n_iterations,0,n_iterations)
   hsigy=ROOT.TH1F("per_{}_hy".format(_if),"per_{}_hy".format(_if),n_iterations,0,n_iterations)
   hsigz=ROOT.TH1F("per_{}_hz".format(_if),"per_{}_hz".format(_if),n_iterations,0,n_iterations)
   for it in range(n_iterations):
      hxname="MLEM_3Dimage_h3_iteration{}_px".format(it)
      hyname="MLEM_3Dimage_h3_iteration{}_py".format(it)
      hzname="MLEM_3Dimage_h3_iteration{}_pz".format(it)
      _hx=f_mlem.Get("MLEMprojection").Get(hxname)
      _hy=f_mlem.Get("MLEMprojection").Get(hyname)
      _hz=f_mlem.Get("MLEMprojection").Get(hzname)
     
      sig_x,chi2_x=dofit(_hx)
      sig_y,chi2_y=dofit(_hy)
      sig_z,chi2_z=dofit(_hz)
       
      if chi2_x < 100000:hsigx.Fill(it, sig_x)
      if chi2_y < 100000:hsigy.Fill(it, sig_y)
      if chi2_z < 100000:hsigz.Fill(it, sig_z)
   
   c3=createRatioCanvas("Performance_{}".format(_if), 1200, 1600)
   c3.cd()
   hsigx.SetMaximum(5); hsigx.SetMinimum(0);
   hsigx.SetMarkerColor(1); hsigx.SetLineColor(1);
   hsigy.SetMarkerColor(2); hsigy.SetLineColor(2);
   hsigz.SetMarkerColor(4); hsigz.SetLineColor(4);
   hsigx.GetYaxis().SetTitle("1#sigma"); hsigx.GetXaxis().SetTitle("# of iterations");
   hsigx.Draw("hist p"); hsigy.Draw("hist p same"); hsigz.Draw("hist p same")
   
   leg = ROOT.TLegend(.55,.58,.75,.80)
   leg.SetFillColor(0)
   leg.SetLineColor(0)
   leg.SetBorderSize(0)
   leg.AddEntry(hsigx,  "#sigma_{x}", "l")
   leg.AddEntry(hsigy,  "#sigma_{y}", "l")
   leg.AddEntry(hsigz,  "#sigma_{z}", "l")
   leg.Draw("same")
   
   line = ROOT.TLine(0,1,n_iterations,1)
   line.SetLineColorAlpha(ROOT.kSpring-1, 0.9)
   line.Draw("same")
   
   c3.Print("/Users/chiu.i-huan/Desktop/new_scientific/run/root/MLEM_output/performance_{}.pdf".format(_if))
#if prog: prog.finalize()

log().info("Path of gif: {}".format("/Users/chiu.i-huan/Desktop/new_scientific/run/root/MLEM_output/"))

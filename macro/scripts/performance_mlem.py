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

f_mlem=ROOT.TFile("/Users/chiu.i-huan/Desktop/new_scientific/run/root/MLEM_output/myMLEMoutput_1113_mlem_iteration100.root","read")
f_osem=ROOT.TFile("/Users/chiu.i-huan/Desktop/new_scientific/run/root/MLEM_output/myMLEMoutput_1113_osem_iteration100.root","read")
n_iterations,n_angles=100, 16

def dofit(hist):
    f1=ROOT.TF1("f1","gaus",-20,20)
    hist.Fit("f1","QR")
    constant, mean, sigma = f1.GetParameter(0), f1.GetParameter(1), f1.GetParameter(2)
    return sigma
   
prog = ProgressBar(ntotal=n_iterations,text="Performance",init_t=time.time())
nevproc=0
hsigx=ROOT.TH1F("per_hx","per_hx",n_iterations,0,n_iterations)
hsigy=ROOT.TH1F("per_hy","per_hy",n_iterations,0,n_iterations)
hsigz=ROOT.TH1F("per_hz","per_hz",n_iterations,0,n_iterations)
for it in range(n_iterations):
   hxname="MLEM_3Dimage_h3_iteration{}_px".format(it)
   hyname="MLEM_3Dimage_h3_iteration{}_py".format(it)
   hzname="MLEM_3Dimage_h3_iteration{}_pz".format(it)
   _hx=f_mlem.Get("MLEMprojection").Get(hxname)
   _hy=f_mlem.Get("MLEMprojection").Get(hyname)
   _hz=f_mlem.Get("MLEMprojection").Get(hzname)
  
   sig_x=dofit(_hx)
   sig_y=dofit(_hy)
   sig_z=dofit(_hz)

   hsigx.Fill(it, sig_x)
   hsigy.Fill(it, sig_y)
   hsigz.Fill(it, sig_z)

c3=createRatioCanvas("Performance", 1200, 1600)
c3.cd()
hsigx.SetMarkerColor(1); hsigx.SetLineColor(1);
hsigy.SetMarkerColor(2); hsigy.SetLineColor(2);
hsigz.SetMarkerColor(4); hsigz.SetLineColor(4);
hsigx.GetYaxis().SetTitle("#pm 1#sigma"); hsigx.GetXaxis().SetTitle("# of iterations");
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

c3.Print("/Users/chiu.i-huan/Desktop/new_scientific/run/root/MLEM_output/mlem_performance.pdf")
if prog: prog.finalize()

log().info("Path of gif: {}".format("/Users/chiu.i-huan/Desktop/new_scientific/run/root/MLEM_output/"))

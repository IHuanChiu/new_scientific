import sys,os,ROOT,time
sys.path.append('/Users/chiu.i-huan/Desktop/new_scientific/macro/utils/')
sys.path.append('/Users/chiu.i-huan/Desktop/new_scientific/macro/')
from ROOT import gSystem
from helpers import createRatioCanvas, ProgressBar
from logger import log
from root_numpy import hist2array, array2hist, tree2array
import numpy as np

name=input("path of file:")
a=input("number of iterations:")
c=input("cut value (0 for no cut): %")
_a=name[-8:-5]
if "n" in _a: _a=name[-7:-5]
if "n" in _a: _a=name[-6:-5]
if not os.path.exists(name):
   print("no this root file!")
   exit(0)
if "_scancut.root" in name:
   print("wrong root file!")
   exit(0)
if int(a) > int(_a): 
   print("wrong number for iteration!")
   exit(0)
if int(c) >= int(100): 
   print("wrong cut!")
   exit(0)

gSystem.Unlink("/Users/chiu.i-huan/Desktop/new_scientific/run/root/MLEM_output/anim_iter.gif")
gSystem.Unlink("/Users/chiu.i-huan/Desktop/new_scientific/run/root/MLEM_output/anim_iter_2d.gif")
gSystem.Unlink("/Users/chiu.i-huan/Desktop/new_scientific/run/root/MLEM_output/anim_iter_pro.gif")
c1=createRatioCanvas("rotation", 600, 500)
f=ROOT.TFile(name,"read")

n_iterations,n_angles=int(a),16
n_phi,n_top,phi_range=9,8,30

prog = ProgressBar(ntotal=n_iterations*n_angles*n_phi,text="3D images",init_t=time.time())
nevproc=0
for iPhi in range(n_phi):
   c1.SetTheta(10)
   c1.SetPhi(10+iPhi*phi_range)
   for it in range(n_iterations):
      for ip in range(0,n_angles):
          nevproc+=1
          if prog: prog.update(nevproc)
          hname="MLEM_3Dimage_h{0}_iteration{1}".format(ip,it)
          if not f.GetListOfKeys().Contains(hname): continue
          _h3=f.Get(hname)
          if c != 0:
             ha=hist2array(_h3)       
             h3=ROOT.TH3D(hname+"_Phi{}".format(10+iPhi*phi_range),hname+"_Phi{}".format(10+iPhi*phi_range),40,-20,20,40,-20,20,40,-20,20)
             _ha_sort=np.reshape(ha,ha.shape[0]*ha.shape[1]*ha.shape[2]) # reshape
             _ha_index=np.argpartition(_ha_sort, -n_top)[-n_top:]# get n_top of the leading values
             maxvalue=np.sum(_ha_sort[_ha_index])/n_top # get max. content
             _where0=np.where(ha < maxvalue*float(c)/100)# drop c% of max. content
             ha[_where0]=0
             array2hist(ha,h3)
             h3.Draw("BOX2Z")
          else:
             _h3.Draw("BOX2Z")
          c1.Print("/Users/chiu.i-huan/Desktop/new_scientific/run/root/MLEM_output/anim_iter.gif+{}".format(ip+it*n_angles))
if prog: prog.finalize()

prog = ProgressBar(ntotal=n_iterations*n_angles,text="2D images",init_t=time.time())
nevproc=0
c2=createRatioCanvas("2dcomparison", 1200, 500)
c2.Divide(2,1)
for it in range(n_iterations):
   for ip in range(0,n_angles):
       nevproc+=1
       if prog: prog.update(nevproc)
       hmname="h{0}".format(ip)
       h2name="MLEM_2Dimage_h{0}_iteration{1}".format(ip,it)
       if not f.GetListOfKeys().Contains(h2name): continue
       _hm=f.Get("measurement").Get(hmname)
       _h2=f.Get(h2name)
       c2.cd(1)
       _hm.Draw("colz")
       c2.cd(2)
       _h2.Draw("colz")
       c2.Print("/Users/chiu.i-huan/Desktop/new_scientific/run/root/MLEM_output/anim_iter_2d.gif+{}".format(ip+it*n_angles))
if prog: prog.finalize()

prog = ProgressBar(ntotal=n_iterations*n_angles,text="Projection",init_t=time.time())
nevproc=0
c3=createRatioCanvas("Projection", 1500, 500)
c3.Divide(3,1)
for it in range(n_iterations):
   for ip in range(0,n_angles):
       nevproc+=1
       if prog: prog.update(nevproc)
       if it == 0 and ip == 0: continue
       hname="MLEM_3Dimage_h{0}_iteration{1}".format(ip,it)
       if not f.GetListOfKeys().Contains(hname): continue
       hxname="MLEM_3Dimage_h{0}_iteration{1}_px".format(ip,it)
       hyname="MLEM_3Dimage_h{0}_iteration{1}_py".format(ip,it)
       hzname="MLEM_3Dimage_h{0}_iteration{1}_pz".format(ip,it)
       _hx=f.Get("MLEMprojection").Get(hxname)
       _hy=f.Get("MLEMprojection").Get(hyname)
       _hz=f.Get("MLEMprojection").Get(hzname)
       _hx.SetLineColor(2)
       _hy.SetLineColor(4)
       _hz.SetLineColor(ROOT.kTeal)
       c3.cd(1)
       _hx.Draw("hist")
       c3.cd(2)
       _hy.Draw("hist")
       c3.cd(3)
       _hz.Draw("hist")
       c3.Print("/Users/chiu.i-huan/Desktop/new_scientific/run/root/MLEM_output/anim_iter_pro.gif+{}".format(ip+it*n_angles))
if prog: prog.finalize()

log().info("Path of gif: {}".format("/Users/chiu.i-huan/Desktop/new_scientific/run/root/MLEM_output/"))

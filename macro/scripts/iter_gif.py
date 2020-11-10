import sys,os,ROOT,time
sys.path.append('/Users/chiu.i-huan/Desktop/new_scientific/macro/utils/')
sys.path.append('/Users/chiu.i-huan/Desktop/new_scientific/macro/')
from ROOT import gSystem
from helpers import createRatioCanvas, ProgressBar
from logger import log
from root_numpy import hist2array, array2hist, tree2array
import numpy as np

name=input("path of file:")
_a=name[-8:-5]
if "n" in _a: _a=name[-7:-5]
if "n" in _a: _a=name[-6:-5]

a=input("number of iterations:")
c=input("cut value (0 for no cut):")
if not os.path.exists(name):
   print("no this root file!")
   exit(0)
if int(a) > int(_a): 
   print("wrong number for iteration!")
   exit(0)
gSystem.Unlink("/Users/chiu.i-huan/Desktop/new_scientific/run/root/MLEM_output/anim_iter.gif")
gSystem.Unlink("/Users/chiu.i-huan/Desktop/new_scientific/run/root/MLEM_output/anim_iter_2d.gif")
c1=createRatioCanvas("rotation", 600, 500)
f=ROOT.TFile(name,"read")

#c1.Print("/Users/chiu.i-huan/Desktop/new_scientific/run/root/MLEM_output/anim_iter.gif+");
n_iterations,n_angles=int(a),16

prog = ProgressBar(ntotal=n_iterations*n_angles*2,text="Rotating images",init_t=time.time())
nevproc=0
for iPhi in range(2):
   c1.SetTheta(10)
   c1.SetPhi(10+iPhi*90)
   for it in range(n_iterations):
      for ip in range(0,n_angles):
          nevproc+=1
          if prog: prog.update(nevproc)
          hname="MLEM_3Dimage_h{0}_iteration{1}".format(ip,it)
          _h3=f.Get(hname)
          if c != 0:
             ha=hist2array(_h3)       
             h3=ROOT.TH3D(hname+"_Phi{}".format(10+iPhi*90),hname+"_Phi{}".format(10+iPhi*90),40,-20,20,40,-20,20,40,-20,20)
             if it == 0 and ip == 0: _where0=np.where(ha<(float(c)/10.))
             else:_where0=np.where(ha<float(c))
             ha[_where0]=0
             array2hist(ha,h3)
             h3.Draw("BOX2Z")
          else:
             _h3.Draw("BOX2Z")
          c1.Print("/Users/chiu.i-huan/Desktop/new_scientific/run/root/MLEM_output/anim_iter.gif+{}".format(ip+it*n_angles))
if prog: prog.finalize()

prog = ProgressBar(ntotal=n_iterations*n_angles,text="Compare images",init_t=time.time())
nevproc=0
c2=createRatioCanvas("2dcomparison", 1200, 500)
c2.Divide(2,1)
for it in range(n_iterations):
   for ip in range(0,n_angles):
       nevproc+=1
       if prog: prog.update(nevproc)
       hmname="h{0}".format(ip)
       h2name="MLEM_2Dimage_h{0}_iteration{1}".format(ip,it)
       _hm=f.Get("measurement").Get(hmname)
       _h2=f.Get(h2name)
       c2.cd(1)
       _hm.Draw("colz")
       c2.cd(2)
       _h2.Draw("colz")
       c2.Print("/Users/chiu.i-huan/Desktop/new_scientific/run/root/MLEM_output/anim_iter_2d.gif+{}".format(ip+it*n_angles))
if prog: prog.finalize()

log().info("Path of gif: {}".format("/Users/chiu.i-huan/Desktop/new_scientific/run/root/MLEM_output/anim_iter.gif"))
log().info("Path of gif: {}".format("/Users/chiu.i-huan/Desktop/new_scientific/run/root/MLEM_output/anim_iter_2d.gif"))

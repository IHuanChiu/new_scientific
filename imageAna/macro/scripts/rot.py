import sys,os,ROOT,time
sys.path.append('/Users/chiu.i-huan/Desktop/new_scientific/imageAna/macro/utils/')
sys.path.append('/Users/chiu.i-huan/Desktop/new_scientific/imageAna/macro/')
from ROOT import gSystem
from helpers import createRatioCanvas, ProgressBar
from logger import log

name=input("path of file:")
if not os.path.exists(name):
   print("no this root file!")
   exit(0)
gSystem.Unlink("/Users/chiu.i-huan/Desktop/new_scientific/imageAna/run/root/MLEM_output/anim.gif")
a=input("number of thetas (rec.:1):")
b=input("number of phis (rec.:50):")

c1=createRatioCanvas("rotation", 500, 500)

f=ROOT.TFile(name,"read")
h3=f.Get("MLEM_3Dimage")
#h3.Draw("ISO")
#h3.Draw("BOX")
h3.Draw("BOX2Z")

c1.SetTheta(18)
c1.SetPhi(0)
c1.Print("/Users/chiu.i-huan/Desktop/new_scientific/imageAna/run/root/MLEM_output/anim.gif+");
n_phis, n_thetas=int(b),int(a)

prog = ProgressBar(ntotal=n_phis*n_thetas,text="Rotating image...",init_t=time.time())
nevproc=0
for itheta in range(n_thetas):
   for iphi in range(n_phis):
       nevproc+=1
       if prog: prog.update(nevproc)
       c1.SetTheta(18-n_thetas*10)
       c1.SetPhi(iphi*360/n_phis+0.1)
       c1.Print("/Users/chiu.i-huan/Desktop/new_scientific/imageAna/run/root/MLEM_output/anim.gif+{}".format(iphi+itheta*n_phis))
if prog: prog.finalize()
log().info("Path of gif: {}".format("/Users/chiu.i-huan/Desktop/new_scientific/imageAna/run/root/MLEM_output/anim.gif"))

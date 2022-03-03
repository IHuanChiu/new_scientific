import os, ROOT
from array import array
ROOT.gErrorIgnoreLevel = ROOT.kFatal
__location__ = os.path.realpath(
        os.path.join(os.getcwd(), os.path.dirname(__file__)))
ROOT.gROOT.LoadMacro( __location__+'/AtlasStyle/AtlasStyle.C')
#ROOT.SetAtlasStyle()

dlist=[]
for _line in open("data_list_new.txt","r"):
   _line=_line.replace(".CSV",".root")
   _line=_line.replace("\n","")
   _line=_line.replace("csv/","root/")
   dlist.append(_line)

if __name__=="__main__":
   index, maxbin = 1, 0
   h_list=[]
   for i in dlist:
      print("INDEX:", index,i)
      fint=ROOT.TFile(i,"read")
      tree=fint.Get("tree")
      tree.Draw("energy >> h{}(6800,10,180)".format(index))
      h1=ROOT.gDirectory.Get("h{}".format(index))
      h1.SetDirectory(0)
      h1.SetStats(0) 
      h1.SetLineColorAlpha(index,0.5)
      h1.SetTitle(";Energy [keV]; Counts/25 eV")
      if h1.GetMaximum() > maxbin: maxbin = h1.GetMaximum()
      h_list.append(h1)
      index+=1

   c1=ROOT.TCanvas("c1","c1",1600,800)
   c2=ROOT.TCanvas("c2","c2",1600,800)
   c3=ROOT.TCanvas("c3","c3",1600,800)
   c4=ROOT.TCanvas("c4","c4",1600,800)
   index=1
   for ii in range(4):
      for h1 in h_list:
         h1.SetMaximum(maxbin*1.1)
         if ii == 0: 
            c1.cd()
            h1.GetXaxis().SetRangeUser(10,60)
            h1.DrawNormalized("hist same")
         if ii == 1: 
            c2.cd()
            h1.GetXaxis().SetRangeUser(50,100)
            h1.DrawNormalized("hist same")
         if ii == 2: 
            c3.cd()
            h1.GetXaxis().SetRangeUser(90,140)
            h1.DrawNormalized("hist same")
         if ii == 3: 
            c4.cd()
            h1.GetXaxis().SetRangeUser(130,180)
            h1.DrawNormalized("hist same")
   c1.Print("/Users/chiu.i-huan/Desktop/check_calibration_r1.pdf")
   c2.Print("/Users/chiu.i-huan/Desktop/check_calibration_r2.pdf")
   c3.Print("/Users/chiu.i-huan/Desktop/check_calibration_r3.pdf")
   c4.Print("/Users/chiu.i-huan/Desktop/check_calibration_r4.pdf")

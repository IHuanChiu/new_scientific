import ROOT
from array import array

#old ri data
#n_points=7
#x_ch2=array("d",[1.23741e+03, 1.39687e+03, 1.57868e+03, 1.60221e+03, 1.81246e+03, 3.23532e+03, 4.86330e+03]) #channel
#y_ch2=array("d",[30.9,34.9,39.5,40.1,45.4,81,121.8]) #energy
#x_ch3=array("d",[1.21205e+03, 1.36934e+03, 1.54736e+03, 1.57040e+03, 1.77612e+03, 3.16840e+03, 4.76116e+03]) #channel
#y_ch3=array("d",[30.9,34.9,39.5,40.1,45.4,81,121.8]) #energy
#new ri data
n_points=3
x_ch2=array("d",[1.85921e+03,2.10264e+03,5.64173e+03]) #channel
y_ch2=array("d",[40.1,45.4,121.8]) #energy
x_ch3=array("d",[1.57017e+03,1.77635e+03,4.76144e+03]) #channel
y_ch3=array("d",[40.1,45.4,121.8]) #energy

if __name__=="__main__":
   fout=ROOT.TFile("./ge_calfunc_1210_new.root","recreate")
   fout.cd()

   gr_2 = ROOT.TGraph(n_points,x_ch2,y_ch2)
   gr_3 = ROOT.TGraph(n_points,x_ch3,y_ch3)
   gr_2.SetName("graph_ch2")
   gr_3.SetName("graph_ch3")
   gr_2.SetMarkerStyle(3)
   gr_3.SetMarkerStyle(3)

   #f2 = ROOT.TF1("f2","[0]*pow(x,[1])",0,8192);
   #f3 = ROOT.TF1("f3","[0]*pow(x,[1])",0,8192);
   f2 = ROOT.TF1("f2","[0]+x*[1]",0,8192);
   f3 = ROOT.TF1("f3","[0]+x*[1]",0,8192);
   gr_2.Fit(f2,"R");
   gr_3.Fit(f3,"R");
   f2.SetName("cal_func_ch2")
   f3.SetName("cal_func_ch3")

   gr_2.Write()
   gr_3.Write()
   f2.Write()
   f3.Write()
   fout.Write()

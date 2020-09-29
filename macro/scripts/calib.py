#!/usr/bin/env python    
#-*- coding:utf-8 -*-   
"""
This module provides the transformation from adc to energy.
"""
__author__    = "I-Huan CHIU"
__email__     = "ichiu@chem.sci.osaka-u.ac.jp"
__created__   = "2019-11-08"
__copyright__ = "Copyright 2019 I-Huan CHIU"
__license__   = "GPL http://www.gnu.org/licenses/gpl.html"

# modules
import sys,os,random,math,ROOT,argparse,time
from ROOT import TFile, TTree, gPad, TGraphAsymmErrors, TSpline3, gStyle, gErrorIgnoreLevel, gROOT
ROOT.gROOT.SetBatch(1)
from array import array
#from logger import log
from random import gauss
import linecache

def getLatex(ch, x = 0.85, y = 0.85):
    _t = ROOT.TLatex()
    _t.SetNDC()
    _t.SetTextFont( 62 )
    _t.SetTextColor( 36 )
    _t.SetTextSize( 0.08 )
    _t.SetTextAlign( 12 )
    return _t

class Calibration():
      def __init__(self,filename=None,output=None,Etable=None,source=None):
          self.filename=filename
          self.output=output
          self.Etable=Etable
          self.source=source
          self.hist_list,self.name_list=self.gethist()
          self.element_list_pside, self.element_list_nside,self.element_list_1,self.element_list_2,self.element_list_3,self.element_list_4,self.element_list_5=self.getrange()
          self.fit_result=self.fit()
          self.graph_list,self.spline_list=self.mkTSpline()

      def gethist(self):
          f = ROOT.TFile(self.filename) 
          hist_list,name_list=[],[]
          for i in range(256):
             i=i*2
             if i < 10: hist_name = "hist_cmn" + "00" + str(i) 
             elif i < 100:  hist_name = "hist_cmn" + "0" + str(i) 
             else : hist_name = "hist_cmn" + str(i)
             _h = f.Get(hist_name).Clone()
             _h.SetDirectory(0) 
             hist_list.append(_h)
             name_list.append(hist_name)             
          return hist_list, name_list

      def getrange(self):
          # get element for fit =>
          # element_list[i] is for the ith line
          # element_list[i][1], [2], [3] is source energy, ADC fit center, ADC fit range 
          element_list_pside, element_list_nside, element_list_1, element_list_2, element_list_3, element_list_4,element_list_5=[],[],[],[],[],[],[]
          table_pside, table_nside=self.Etable.replace(".txt","_pside.txt"), self.Etable.replace(".txt","_nside.txt")
          table_1,table_2,table_3,table_4,table_5=self.Etable.replace(".txt","_0_95.txt"),self.Etable.replace(".txt","_96_127.txt"),self.Etable.replace(".txt","_128_159.txt"),self.Etable.replace(".txt","_160_223.txt"),self.Etable.replace(".txt","_224_255.txt")
          _lp=linecache.getlines(table_pside) 
          _ln=linecache.getlines(table_nside) 
          _l1=linecache.getlines(table_1) 
          _l2=linecache.getlines(table_2) 
          _l3=linecache.getlines(table_3) 
          _l4=linecache.getlines(table_4) 
          _l5=linecache.getlines(table_5) 
          for _il in range(len(_lp)):
             _e=_lp[_il].strip().split(' ')
             if "#" in _e[0]: continue
             if _e[0] == self.source: element_list_pside.append(_e)  
          for _il in range(len(_ln)):
             _e=_ln[_il].strip().split(' ')
             if "#" in _e[0]: continue
             if _e[0] == self.source: element_list_nside.append(_e)  
          for _il in range(len(_l1)):
             _e=_l1[_il].strip().split(' ')
             if "#" in _e[0]: continue
             if _e[0] == self.source: element_list_1.append(_e)  
          for _il in range(len(_l2)):
             _e=_l2[_il].strip().split(' ')
             if "#" in _e[0]: continue
             if _e[0] == self.source: element_list_2.append(_e)  
          for _il in range(len(_l3)):
             _e=_l3[_il].strip().split(' ')
             if "#" in _e[0]: continue
             if _e[0] == self.source: element_list_3.append(_e)  
          for _il in range(len(_l4)):
             _e=_l4[_il].strip().split(' ')
             if "#" in _e[0]: continue
             if _e[0] == self.source: element_list_4.append(_e)  
          for _il in range(len(_l5)):
             _e=_l5[_il].strip().split(' ')
             if "#" in _e[0]: continue
             if _e[0] == self.source: element_list_5.append(_e)  
          return element_list_pside, element_list_nside, element_list_1, element_list_2, element_list_3, element_list_4, element_list_5

      def fit(self):
          fit_result=[]
          ich=0
          for ih in self.hist_list:
#             if ich < 128: element_list = self.element_list_pside
#             else: element_list = self.element_list_nside
             if ich < 96: element_list=self.element_list_1
             elif ich < 128: element_list=self.element_list_2
             elif ich < 160: element_list=self.element_list_3
             elif ich < 224: element_list=self.element_list_4
             else: element_list=self.element_list_5
             dic, n_fit={}, 0
             for ifit in element_list:
                E_down, E_up=float(ifit[2]), float(ifit[3])
                g1=ROOT.TF1("g1","gaus",E_down,E_up)
                g1.SetLineColor(ROOT.kRed)
                if n_fit == 0: ih.Fit("g1","QR")
                else: ih.Fit("g1","QR+")
                dic.update({ifit[1]:g1.GetParameter(1)})
                n_fit+=1   
             ich+=1
             fit_result.append(dic)
          return fit_result

      def mkTSpline(self):
          graph_list,spline_list=[],[]
          for i in range(len(self.hist_list)):     
             _g = ROOT.TGraph()
             _s = ROOT.TSpline3()
             _g.SetName("graph_"+self.name_list[i])
             _g.SetPoint(0, 0, 0)
#             if i < 128: element_list = self.element_list_pside
#             else: element_list = self.element_list_nside
             if i < 96: element_list=self.element_list_1
             elif i < 128: element_list=self.element_list_2
             elif i < 160: element_list=self.element_list_3
             elif i < 224: element_list=self.element_list_4
             else: element_list=self.element_list_5
             for ifit in range(len(element_list)):
                 source_E=element_list[ifit][1]
                 fit_adc=self.fit_result[i][source_E]
                 _g.SetPoint(ifit+1, fit_adc, float(source_E))
                 if ifit == len(element_list)-1:
                    source_Epre=element_list[ifit-1][1]
                    fit_adcpre=self.fit_result[i][source_Epre]
                    if fit_adc == fit_adcpre: fit_adc +=1
                    slope = (float(source_E) - float(source_Epre))/(fit_adc - fit_adcpre)
                    f_x, f_y = fit_adc, float(source_E)
             _g.SetPoint(len(element_list) + 1, 1500, (1500-f_x)*slope + f_y) 
             _s = ROOT.TSpline3("spline_"+str(i), _g)
             spline_list.append(_s)
             graph_list.append(_g)
          return graph_list,spline_list

      def plot(self):
          __location__ = os.path.realpath(
                  os.path.join(os.getcwd(), os.path.dirname(__file__)))
          ROOT.gROOT.LoadMacro( __location__+'/AtlasStyle/AtlasStyle.C')
          ROOT.SetAtlasStyle()
          for i in range(256):
             latex = getLatex(i,400,8000)
             if i*2 < 10: temp_name = "hist_cmn" + "00" + str(i*2) 
             elif i*2 < 100:  temp_name = "hist_cmn" + "0" + str(i*2) 
             else : temp_name = "hist_cmn" + str(i*2)
             new_name=self.name_list[i].replace(temp_name,"ch : {}".format(i))
             gROOT.ProcessLine("gErrorIgnoreLevel = kWarning;")
             #c1 = ROOT.TCanvas(self.name_list[i],"",0,0,800,800)
             c0 = ROOT.TCanvas(self.name_list[i],"",0,0,2400,800)
             c0.Divide(3,1)
             c0.cd(1)
             gPad.SetLogy(1)
             self.hist_list[i].SetLineColor(1)
             self.hist_list[i].Draw()
             latex.DrawLatex(0.5,0.85,new_name)
             #c1.SaveAs("/Users/chiu.i-huan/Desktop/new_scientific/run/figs/cali_plots/"+temp_name.replace(temp_name,"hist_"+self.source+"_fit"+"_"+str(i))+".pdf")

             c0.cd(2)
             #c2 = ROOT.TCanvas("gr"+self.name_list[i],"",0,0,800,800)
             graph=self.graph_list[i]
             graph.SetMarkerColor(4)
             graph.SetMarkerStyle(21)
             graph.Draw("ALP")
             latex.DrawLatex(0.5,0.85,new_name)         
             #c2.Print("/Users/chiu.i-huan/Desktop/new_scientific/run/figs/cali_plots/"+temp_name.replace(temp_name,"hist_"+self.source+"_gr"+"_"+str(i))+".pdf")

             c0.cd(3)
             #c3 = ROOT.TCanvas("line"+self.name_list[i],"",0,0,800,800)
             graph=self.spline_list[i]
             graph.SetLineColor(1)
             graph.Draw("L")
             latex.DrawLatex(0.5,0.85,new_name)         
             #c3.Print("/Users/chiu.i-huan/Desktop/new_scientific/run/figs/cali_plots/"+temp_name.replace(temp_name,"hist_"+self.source+"_line"+"_"+str(i))+".pdf")

             c0.SaveAs("/Users/chiu.i-huan/Desktop/new_scientific/run/figs/cali_plots/"+temp_name.replace(temp_name,"hist_"+self.source+"_all"+"_"+str(i))+".pdf")

      def Printout(self):
          args.output=args.output.replace(".root","_"+self.source+".root")
          fout = ROOT.TFile( args.output, 'recreate' )
          fout.cd()
          for i in range(256):
             graph=self.graph_list[i]
             graph.SetName("graph_"+str(i))
             graph.Write()    
          for i in range(256):
             spline=self.spline_list[i]
             spline.SetName("spline_"+str(i))
             spline.Write()    
          fout.Write()          

def fit(i, f, h_name, Amenergy):
    c0 = ROOT.TCanvas("temp_"+h_name,"",0,0,800,800)
    hist = f.Get(h_name)
    g1 = ROOT.TF1("g1","gaus",90,110)
    g2 = ROOT.TF1("g2","gaus",120,150)
    g3 = ROOT.TF1("g3","gaus",190,230)
    g4 = ROOT.TF1("g4","gaus",500,600)
    if i <= 48 and i >= 43: 
       g1 = ROOT.TF1("g1","gaus",85,110)
       g2 = ROOT.TF1("g2","gaus",115,150)
    elif i <= 126 and i >= 96: 
       g1 = ROOT.TF1("g1","gaus",90,130)
       g2 = ROOT.TF1("g2","gaus",120,170)
       g3 = ROOT.TF1("g3","gaus",190,250)
    elif (i <= 153 and i >= 128) or (i <= 218 and i >= 166) or (i <= 255 and i >= 226): 
       g1 = ROOT.TF1("g1","gaus",100,150)
       g2 = ROOT.TF1("g2","gaus",150,200)
       g3 = ROOT.TF1("g3","gaus",230,300)
    elif (i <= 225 and i >= 219) or (i <= 165 and i >= 154): 
       g1 = ROOT.TF1("g1","gaus",100,250)
       g2 = ROOT.TF1("g2","gaus",100,250)
       g3 = ROOT.TF1("g3","gaus",100,250)
    g1.SetLineColor(ROOT.kRed)
    g2.SetLineColor(ROOT.kRed)
    g3.SetLineColor(ROOT.kRed)
    g4.SetLineColor(ROOT.kRed)
    hist.Fit("g1","QR")
    hist.Fit("g2","QR+")
    hist.Fit("g3","QR+")
    hist.Fit("g4","QR+")

    dic = {Amenergy[0]:g1.GetParameter(1), Amenergy[1]:g2.GetParameter(1), Amenergy[2]:g3.GetParameter(1), Amenergy[3]:g4.GetParameter(1)}
#    dic = { g1.GetParameter(1) : Amenergy[i] for i in range(1,5)} 
    print(h_name," : ", dic)
    return hist, dic 

def makeTGraphAndTSpline(i, name, table, energy):
    _g = ROOT.TGraph()
    _s = ROOT.TSpline3()
    _g.SetName("graph_"+name)
    _g.SetPoint(0, 0, 0)
    for i in range(len(energy)):
        _g.SetPoint(i+1, table[energy[i]], energy[i])
        if energy[i] == energy[i-1]: continue
        slope = (energy[i] - energy[i-1])/(table[energy[i]] - table[energy[i-1]])
        f_x = table[energy[i]]
        f_y = energy[i]
    _g.SetPoint(len(energy) + 1, 1500, (1500-f_x)*slope + f_y) 
    _s = ROOT.TSpline3("spline_"+str(i), _g)
    return _g, _s
    
def plot(name, hist, graph, latex):
    namech = name.replace("hist_cmn","ch : ")
    gROOT.ProcessLine("gErrorIgnoreLevel = kWarning;")
    c1 = ROOT.TCanvas("hist"+name,"",0,0,800,800)
    gPad.SetLogy(1)
    hist.Draw()
    latex.DrawLatex(0.5,0.85,namech)
    c1.SaveAs("../run/figs/cali_plots/"+name+"_fit.pdf")

    c2 = ROOT.TCanvas("gr"+name,"",0,0,800,800)
    graph.SetMarkerColor(4)
    graph.SetMarkerStyle(21)
    graph.Draw("ALP")
    latex.DrawLatex(0.5,0.85,namech)

    c2.Print("../run/figs/cali_plots/"+name+"_gr.pdf")
    
def main(args, IsRandom = False):
    __location__ = os.path.realpath(
            os.path.join(os.getcwd(), os.path.dirname(__file__)))
    ROOT.gROOT.LoadMacro( __location__+'/AtlasStyle/AtlasStyle.C')
    ROOT.SetAtlasStyle()

#    Amenergy = (13.94, 16.81, 17.75, 59.5)
    Amenergy = (13.94, 17.75, 26.3, 59.5)
    hist_name = [] 
    fout = ROOT.TFile( args.output, 'recreate' )

    f = ROOT.TFile(args.input)  
    fout.cd() 
    for i in range(256):
       if (i <= 225 and i >= 219) or (i <= 165 and i >= 154): Amenergy = (16.81, 16.81, 16.81, 59.5)       
       else: Amenergy = (13.94, 16.81, 26.3, 59.5)

       if i < 10: hist_name = "hist_cmn" + "00" + str(i) 
       elif i < 100:  hist_name = "hist_cmn" + "0" + str(i) 
       else : hist_name = "hist_cmn" + str(i)
       # cannot fitting
       if i == 0 : hist_name = "hist_cmn001"
       if i == 78 : hist_name = "hist_cmn079"
       if i == 127 : hist_name = "hist_cmn128"

       hist, table = fit(i, f, hist_name, Amenergy)
       gr, spline = makeTGraphAndTSpline(i, hist_name, table, Amenergy)
       latex = getLatex(i,400,8000)
       plot(hist_name , hist, gr, latex)
       spline.SetName("spline_"+str(i))
       spline.Write()    
    fout.Write()
    os.system("pdfunite ../run/figs/cali_plots/hist_cmn*.pdf ../run/figs/cali_plots/hist_all_book.pdf")
        
def run(args):
    if ".root" not in args.input:
       args.input=args.input+"_"+args.source+".root"
    Cal=Calibration(filename=args.input, output=args.output,Etable=args.table,source=args.source)
    Cal.plot()
    Cal.Printout()
#    os.chdir('/Users/chiu.i-huan/Desktop/new_scientific/run/figs/cali_plots/') 
#    os.system("pdfunite hist_cmn*fit.pdf hist_cali_2mmcdte_book.pdf")
    exit(0)
 
if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='Process some integers.')

#    /Users/chiu.i-huan/Desktop/new_scientific/data/minami_data/500n20/cali_2mmcdte_Am.root
#    /Users/chiu.i-huan/Desktop/new_scientific/data/minami_data/500n20/cali_2mmcdte_Ba.root
#    /Users/chiu.i-huan/Desktop/new_scientific/data/minami_data/500n20/cali_2mmcdte_Co.root

    parser.add_argument("-i","--input", dest="input", type=str, default="/Users/chiu.i-huan/Desktop/new_scientific/data/minami_data/500n20/cali_2mmcdte", help="Input File Name")
    parser.add_argument("--output", type=str, default="./spline_calibration_2mmtest.root", help="Output File Name")
    parser.add_argument("--table", type=str, default="./energy_table/energy_table.txt", help="energy table")
    parser.add_argument("-s","--source", dest="source", type=str, default="Am", help="Am or Co or Ba")
    parser.add_argument("--channel", default=False, action="store_true", help="number of CPU")
    parser.add_argument("--nevent", default=500000, action="store_true", help="number of event")
    args = parser.parse_args()

#    main( args , True)# for Si-detector
    run( args)# for CdTe


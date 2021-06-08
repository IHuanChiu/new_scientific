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


import sys,os,random,math,ROOT,argparse
from ROOT import TFile, TTree, gPad, TGraphAsymmErrors, TSpline, TSpline3, TSpline5, gStyle, gErrorIgnoreLevel, gROOT
ROOT.gROOT.SetBatch(1)
ROOT.gErrorIgnoreLevel = ROOT.kWarning
#kPrint, kInfo, kWarning, kError, kBreak, kSysError, kFatal;

def getLatex(ch, x = 0.85, y = 0.85):
    _t = ROOT.TLatex()
    _t.SetNDC()
    _t.SetTextFont( 62 )
    _t.SetTextColor( 36 )
    _t.SetTextSize( 0.08 )
    _t.SetTextAlign( 12 )
    return _t

def compare(_outputname, _voltage, fa, fb, fc, spline):   
    __location__ = os.path.realpath(
            os.path.join(os.getcwd(), os.path.dirname(__file__)))
    ROOT.gROOT.LoadMacro( __location__+'/AtlasStyle/AtlasStyle.C')
    ROOT.SetAtlasStyle()
    c0name="/Users/chiu.i-huan/Desktop/new_scientific/imageAna/run/figs/cali_plots/"+_outputname+"_"+_voltage+"/comparison_all.pdf" 
    c0 = ROOT.TCanvas(c0name,"",0,0,1600,800)
    c0.Divide(2,1)
    c0.Print(c0name + "[", "pdf")
    for ich in range(128):
       for side in range(2):
          c0.cd(side+1)
          i=ich+side*128
          linename = "spline_"+str(i) 
          la=fa.Get(linename)
          lb=fb.Get(linename)
          lc=fc.Get(linename)          
          spline[i].SetLineColor(1)
          la.SetLineColor(2)
          lb.SetLineColor(3)
          lc.SetLineColor(4)
          spline[i].Draw()
          la.Draw("same")
          lb.Draw("same")
          lc.Draw("same")

          leg = ROOT.TLegend(.55,.18,.75,.40)
          leg.SetFillColor(0)
          leg.SetLineColor(0)
          leg.SetBorderSize(0)
          leg.AddEntry(spline[i],  "merge", "l")
          leg.AddEntry(la,  "Am", "l")
          leg.AddEntry(lb,  "Ba", "l")
          leg.AddEntry(lc,  "Co", "l")
          leg.Draw("same")

          latex = getLatex(i,400,8000) 
          Latex_name="Ch : {}".format(i)
          latex.DrawLatex(0.25,0.85,Latex_name)
          del la,lb,lc
       c0.Print(c0name, "pdf")
    c0.Print(c0name + "]", "pdf")

def merge(args):
    spline_list=[]
    useCoHight = True
    fout=ROOT.TFile("./files_cali/spline_calibration_"+args.outname+"_"+args.voltage+"_merge.root","recreate")
    fa=ROOT.TFile("files_cali/spline_calibration_"+args.outname+"_"+args.voltage+"_Am.root","read")
    fb=ROOT.TFile("files_cali/spline_calibration_"+args.outname+"_"+args.voltage+"_Ba.root","read")
    fc=ROOT.TFile("files_cali/spline_calibration_"+args.outname+"_"+args.voltage+"_Co.root","read")
    fout.cd()
    for i in range(256):
       _g = ROOT.TGraph()
       _s = ROOT.TSpline3()
       _index=0
       _g.SetPoint(_index, 0, 0)
       graph_name="graph_"+str(i)
       _ga=fa.Get(graph_name)
       _gb=fb.Get(graph_name)
       _gc=fc.Get(graph_name)
       # === check fitting plots & adc range (adc, energy) ===       
#       _index=_index+1
#       if i == 0 and _ga.GetPointY(1) != 13.94: print("should be 13.94 : ", _ga.GetPointY(1))
#       _g.SetPoint(_index, _ga.GetPointX(1), _ga.GetPointY(1))#Am 13.94

       _index=_index+1
       if i == 0 and _gc.GetPointY(1) != 14.41: print("should be 14.41 : ", _gc.GetPointY(1))
       _g.SetPoint(_index, _gc.GetPointX(1), _gc.GetPointY(1))#Co 14.41

       _index=_index+1
       if i == 0 and _ga.GetPointY(2) != 17.75: print("should be 17.75 : ", _ga.GetPointY(2))
       _g.SetPoint(_index, _ga.GetPointX(2), _ga.GetPointY(2))#Am 17.75

       _index=_index+1
       if i == 0 and _ga.GetPointY(3) != 20.8: print("should be 20.8 : ", _ga.GetPointY(3))
       _g.SetPoint(_index, _ga.GetPointX(3), _ga.GetPointY(3))#Am 20.8

       _index=_index+1
       if i == 0 and _ga.GetPointY(4) != 26.3: print("should be 26.3 : ", _ga.GetPointY(4))
       _g.SetPoint(_index, _ga.GetPointX(4), _ga.GetPointY(4))#Am 26.3

       _index=_index+1
       if i == 0 and _gb.GetPointY(1) != 31.0: print("should be 31 : ", _gb.GetPointY(1))
       _g.SetPoint(_index, _gb.GetPointX(1), _gb.GetPointY(1))#Ba 31

       _index=_index+1
       if i == 0 and _ga.GetPointY(5) != 59.5: print("should be 59.5 : ", _ga.GetPointY(5))
       _g.SetPoint(_index, _ga.GetPointX(5), _ga.GetPointY(5))#Am 59.5

       _index=_index+1
       if i == 0 and _gb.GetPointY(3) != 81.0: print("should be 81 : ", _gb.GetPointY(3))
       _g.SetPoint(_index, _gb.GetPointX(3), _gb.GetPointY(3))#Ba 81

       if useCoHight:
          _index=_index+1
          if i == 0 and _gc.GetPointY(2) != 122.06: print("should be 122.06 : ", _gc.GetPointY(2))
          _g.SetPoint(_index, _gc.GetPointX(2), _gc.GetPointY(2))#Co 122.06

          if i < 128:#p-side
             slope = (_gc.GetPointY(2) - _gb.GetPointY(3))/(_gc.GetPointX(2) - _gb.GetPointX(3))
             f_x, f_y = _gc.GetPointX(2), _gc.GetPointY(2)
             _index=_index+1
             _g.SetPoint(_index, 1024, (1024-f_x)*slope + f_y)
          else:#n-side
             _index=_index+1
             if i == 0 and _gc.GetPointY(3) != 136.47: print("should be 136.47 : ", _gc.GetPointY(3))
             _g.SetPoint(_index, _gc.GetPointX(3), _gc.GetPointY(3))#Co 136.47
             slope = (_gc.GetPointY(3) - _gc.GetPointY(2))/(_gc.GetPointX(3) - _gc.GetPointX(2))
             f_x, f_y = _gc.GetPointX(3), _gc.GetPointY(3)
             _index=_index+1
             _g.SetPoint(_index, 1024, (1024-f_x)*slope + f_y)       
       else:
          slope = (_gb.GetPointY(3) - _ga.GetPointY(5))/(_gb.GetPointX(3) - _ga.GetPointX(5))
          f_x, f_y = _gb.GetPointX(3), _gb.GetPointY(3)
          _index=_index+1
          _g.SetPoint(_index, 1024, (1024-f_x)*slope + f_y)
       _s = ROOT.TSpline3("spline_"+str(i), _g)
#       _s.SetName("spline_"+str(i))
#       _s.Write()

#       _g.SetName(graph_name)
       _g.SetName("spline_"+str(i))
       _g.Write()

       spline_list.append(_s)
       del _g,_s    
    fout.Write()
    fout.Close()
    compare(args.outname,args.voltage,fa,fb,fc,spline_list)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument("-o","--outname", dest="outname", type=str, default="machine2", help="Name of Output File from Calibration")
    parser.add_argument("-v","--voltage", dest="voltage", type=str, default="500n20", help="500n20, 400n20, 300n20...")
    args = parser.parse_args()
    merge(args)

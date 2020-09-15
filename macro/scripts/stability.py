
#!/usr/bin/env python    
#-*- coding:utf-8 -*-   
"""
This module checks the time stability of 2mm CdTe detector
"""
__author__    = "I-Huan CHIU"
__email__     = "ichiu@chem.sci.osaka-u.ac.jp"
__created__   = "2020-09-14"
__copyright__ = "Copyright 2020 I-Huan CHIU"
__license__   = "GPL http://www.gnu.org/licenses/gpl.html"

# modules
import sys,os,random,math,time,ROOT,argparse, ctypes
from ROOT import TFile, TTree, gPad, TGraphAsymmErrors, TSpline3, gStyle, gErrorIgnoreLevel, gROOT, gDirectory
ROOT.gROOT.SetBatch(1)
import argparse
import time
from root_numpy import hist2array, array2hist, tree2array
import numpy as np
sys.path.append('/Users/chiu.i-huan/Desktop/new_scientific/macro/utils/')
sys.path.append('/Users/chiu.i-huan/Desktop/new_scientific/macro/')
ROOT.gErrorIgnoreLevel = ROOT.kWarning
from helpers import GetTChain, createRatioCanvas
from logger import log, supports_color

def getUT(chain):
    _ut=tree2array(chain,branches="unixtime")
    return np.min(_ut), np.max(_ut) 

def mkADCplots(chain, initUT, finalUT, timerange):
    nplots=int((finalUT-initUT)/timerange)+1
    hp_list,hn_list =[],[]
    for i in range(nplots):
#    for i in range(3):
       log().info("unixtime > {0} && unixtime < {1}".format(initUT+timerange*i, initUT+timerange*(i+1)))
       UTcut="unixtime > {0} && unixtime < {1}".format(initUT+timerange*i, initUT+timerange*(i+1))
       hp=ROOT.TH1D("hpside_{}".format(i),"hpside_{}".format(i),1024,0,1024)
       for iasic in range(4):
          adc_name, cmn_name = "adc"+str(iasic), "cmn"+str(iasic)
          chain.Draw(adc_name +"-"+ cmn_name+">> h1(1024,0,1024)",UTcut,"")
          h1=gDirectory.Get("h1")
          hp.Add(h1)
       hp_list.append(hp)
   
       hn=ROOT.TH1D("hnside_{}".format(i),"hnside_{}".format(i),1024,0,1024)
       for iasic in range(4,8):
          adc_name, cmn_name = "adc"+str(iasic), "cmn"+str(iasic)
          chain.Draw(adc_name +"-"+ cmn_name+">> h1(1024,0,1024)",UTcut,"")
          h1=gDirectory.Get("h1")
          hn.Add(h1)
       hn_list.append(hn)
    return hp_list, hn_list

def mkADCArray(chain, initUT, finalUT, timerange):
    treearray=tree2array(chain,branches=['adc0-cmn0','adc1-cmn1','adc2-cmn2','adc3-cmn3','adc4-cmn4','adc5-cmn5','adc6-cmn6','adc7-cmn7','unixtime'])
    nplots=int((finalUT-initUT)/timerange)+1
    hp_list,hn_list =[],[]
#    for i in range(nplots):
    for i in range(3):
       UTcutL, UTcutH =initUT+timerange*i, initUT+timerange*(i+1)
       log().info("Current Time range : {0} ~ {1}".format(UTcutL, UTcutH))
       _treecut="unixtime > {0} && unixtime < {1}".format(UTcutL,UTcutH)
#       _w = np.where((treearray["unixtime"] > UTcutL) & (treearray["unixtime"] > UTcutH))
       hp=ROOT.TH1D("hpside_{}".format(i),"hpside_{}".format(i),1024,0,1024)
       hn=ROOT.TH1D("hnside_{}".format(i),"hnside_{}".format(i),1024,0,1024)
       for iasic in range(8):
          var_name='adc{}-cmn{}'.format(iasic)
          _varcut="("+var_name+" > 30"+")"
          _treecut+=_treecut+"&&"+_varcut
          treearray=tree2array(chain,branches=[var_name],selection=_treecut)
          _treearray[var_name]=np.reshape(treearray[var_name],(treearray[var_name].shape[0]*treearray[var_name].shape[1]))
          if iasic < 4 : 
             if iasic == 0: hparray=_treearray[var_name]
             else: hparray=np.hstack((hparray,_treearray[var_name]))
          else :
             if iasic == 4: hnarray=_treearray[var_name]
             else: hnarray=np.hstack((hnarray,_treearray[var_name]))
       array2hist(hparray,hp)
       array2hist(hnarray,hn)
       hp_list.append(hp)
       hn_list.append(hn)
    return hp_list, hn_list

def getADCplots(plotfilename):
    #TODO fix this
    hp_list, hn_list = [], []
    _f=ROOT.TFile(plotfilename,"read")
    hp1=_f.Get("hpside_0")
    hp2=_f.Get("hpside_1")
    hp3=_f.Get("hpside_2")
    hn1=_f.Get("hnside_0")
    hn2=_f.Get("hnside_1")
    hn3=_f.Get("hnside_2")
    hp_list.append(hp1)
    hp_list.append(hp2)
    hp_list.append(hp3)
    hn_list.append(hn1)
    hn_list.append(hn2)
    hn_list.append(hn3)
    return hp_list, hn_list

def mkcv(_hp_list,_hn_list):
    _cv  = createRatioCanvas("cv", 5000, 2500)
    _cv.Divide(2,1)
    _cv.cd(1)
    leg = ROOT.TLegend(.55,.78,.75,.90)
    gPad.SetLogy()
    for _ip in range(len(_hp_list)):
       _hp_list[_ip].SetStats(0)
       _hp_list[_ip].SetLineColor(_ip+1)
       if _ip == 0 :
          _hp_list[_ip].SetMaximum(_hp_list[_ip].GetMaximum()*20)
          _hp_list[_ip].SetTitle("P-side")
          _hp_list[_ip].GetXaxis().SetTitle("ADC")
          _hp_list[_ip].GetYaxis().SetTitle("Counts")
          _hp_list[_ip].Draw()
       else:
          _hp_list[_ip].Draw("same")
       leg.AddEntry(_hp_list[_ip],  " Pside, Time step_{}".format(_ip), "l")
       leg.Draw("same")
    
    _cv.cd(2)
    leg = ROOT.TLegend(.55,.78,.75,.90)
    gPad.SetLogy()
    for _in in range(len(_hn_list)):
       _hn_list[_in].SetStats(0)
       _hn_list[_in].SetLineColor(_in+1)
       if _in == 0 :
          _hn_list[_in].SetMaximum(_hn_list[_in].GetMaximum()*20)
          _hn_list[_in].SetTitle("N-side")
          _hn_list[_in].GetXaxis().SetTitle("ADC")
          _hn_list[_in].GetYaxis().SetTitle("Counts")
          _hn_list[_in].Draw()
       else:
          _hn_list[_in].Draw("same")
       leg.AddEntry(_hn_list[_in],  "Nside, Time step_{}".format(_in), "l")
       leg.Draw("same")

    return _cv           

def run(args):
    foldername=args.inputFolder+"/"+args.condition+"/"+args.source
    mychain=GetTChain(foldername,"eventtree")
    initUT, finalUT=getUT(mychain)   
    timerange=args.timerange*3600
    log().info("Total plots : {0} , Time range : {1} hours".format(int((finalUT-initUT)/timerange)+1, args.timerange))
    if(int((finalUT-initUT)/timerange)+1 > 10): 
       exit(0)

    if args.plots is None:
       outputname="/Users/chiu.i-huan/Desktop/new_scientific/run/root/"+"cdte2mmdata_"+args.condition+"_"+args.source+"_"+str(args.timerange)+"h_"+args.output+".root"
       fout=ROOT.TFile(outputname,"recreate")
       fout.cd()
       hp_list,hn_list=mkADCplots(mychain,initUT,finalUT,timerange)    
       for i in range(len(hp_list)):
          hp_list[i].Write()
          hn_list[i].Write()
       fout.Write()
       log().info("Done, check output file in : {}".format(outputname))
    else:
       hp_list,hn_list=getADCplots(args.plots)

    cv=mkcv(hp_list,hn_list)
    outcv_name="/Users/chiu.i-huan/Desktop/"+"cv_"+args.condition+"_"+args.source+"_"+str(args.timerange)+"h_"+args.output+".pdf"
    cv.SaveAs(outcv_name)

if __name__=="__main__":

   parser = argparse.ArgumentParser(description='Process some integers.')
   parser.add_argument("-i","--inputFolder", type=str, default="/Users/chiu.i-huan/Desktop/new_scientific/data/minami_data", help="Input File Name")
   parser.add_argument("-p","--plots", type=str, default=None, help="Input File Name")
   parser.add_argument("-c","--condition", type=str, default="300n20", help="Condition : 300n20 400n20 500n20")
   parser.add_argument("-s","--source", type=str, default="Am", help="Input Source : Am Ba Co")
   parser.add_argument("-o","--output",type=str, default="stability", help="Name of output file")
   parser.add_argument("-tr","--timerange",type=int, default=3, help="Time range (Hours)")
   args = parser.parse_args()

   run(args)

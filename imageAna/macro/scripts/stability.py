
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
sys.path.append('/Users/chiu.i-huan/Desktop/new_scientific/imageAna/macro/utils/')
sys.path.append('/Users/chiu.i-huan/Desktop/new_scientific/imageAna/macro/')
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
       log().info("unixtime > {0} && unixtime < {1}".format(initUT+timerange*i, initUT+timerange*(i+1)))
       UTcut="unixtime > {0} && unixtime < {1}".format(initUT+timerange*i, initUT+timerange*(i+1))
       hp=ROOT.TH1D("hpside_{}".format(i),"hpside_{}".format(i),994,30,1024)
       for iasic in range(4):
          adc_name, cmn_name = "adc"+str(iasic), "cmn"+str(iasic)
          chain.Draw(adc_name +"-"+ cmn_name+">> h1(994,30,1024)",UTcut,"")
          h1=gDirectory.Get("h1")
          hp.Add(h1)
       hp_list.append(hp)
   
       hn=ROOT.TH1D("hnside_{}".format(i),"hnside_{}".format(i),994,30,1024)
       for iasic in range(4,8):
          adc_name, cmn_name = "adc"+str(iasic), "cmn"+str(iasic)
          chain.Draw(adc_name +"-"+ cmn_name+">> h2(994,30,1024)",UTcut,"")
          h2=gDirectory.Get("h2")
          hn.Add(h2)
       hn_list.append(hn)
    return hp_list, hn_list

def readtree(chain, cutvalue):
    list_array=[]
    pha0array=tree2array(chain,branches=['adc0-cmn0','unixtime'],selection='adc0-cmn0 > {}'.format(cutvalue))
    pha1array=tree2array(chain,branches=['adc1-cmn1','unixtime'],selection='adc1-cmn1 > {}'.format(cutvalue))
    pha2array=tree2array(chain,branches=['adc2-cmn2','unixtime'],selection='adc2-cmn2 > {}'.format(cutvalue))
    pha3array=tree2array(chain,branches=['adc3-cmn3','unixtime'],selection='adc3-cmn3 > {}'.format(cutvalue))
    pha4array=tree2array(chain,branches=['adc4-cmn4','unixtime'],selection='adc4-cmn4 > {}'.format(cutvalue))
    pha5array=tree2array(chain,branches=['adc5-cmn5','unixtime'],selection='adc5-cmn5 > {}'.format(cutvalue))
    pha6array=tree2array(chain,branches=['adc6-cmn6','unixtime'],selection='adc6-cmn6 > {}'.format(cutvalue))
    pha7array=tree2array(chain,branches=['adc7-cmn7','unixtime'],selection='adc7-cmn7 > {}'.format(cutvalue))
    list_array.append(pha0array)
    list_array.append(pha1array)
    list_array.append(pha2array)
    list_array.append(pha3array)
    list_array.append(pha4array)
    list_array.append(pha5array)
    list_array.append(pha6array)
    list_array.append(pha7array)
    return list_array

def mkADCArray(chain, initUT, finalUT, timerange):
    ti=time.time()
    list_treearray=readtree(chain,30)
    log().info("CPU time for tree2array: {} seconds".format(time.time()-ti))
    nplots=int((finalUT-initUT)/timerange)+1
    hp_list,hn_list =[],[]
    for i in range(nplots):
       UTcutL, UTcutH =initUT+timerange*i, initUT+timerange*(i+1)
       log().info("Current Time range : {0} ~ {1}".format(UTcutL, UTcutH))

       hp=ROOT.TH1D("hpside_{}".format(i),"hpside_{}".format(i),1024,0,1024)
       hn=ROOT.TH1D("hnside_{}".format(i),"hnside_{}".format(i),1024,0,1024)
       for iasic in range(8):
          var_name='adc{}-cmn{}'.format(iasic,iasic)
          treearray=list_treearray[iasic]
          _w = np.where((treearray["unixtime"] > UTcutL) & (treearray["unixtime"] > UTcutH))
          pha_array=np.reshape(treearray[_w][var_name],(treearray[_w][var_name].shape[0]*treearray[_w][var_name].shape[1]))
          if iasic < 4 : 
             if iasic == 0: hparray=pha_array
             else: hparray=np.hstack((hparray,pha_array))
          else :
             if iasic == 4: hnarray=pha_array
             else: hnarray=np.hstack((hnarray,pha_array))
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

def mkcv(_hp_list,_hn_list,_tr):
    _cv  = createRatioCanvas("cv", 5000, 2500)
    _cv.Divide(2,1)
    _cv.cd(1)
    #gPad.SetLogy()
    for _ip in range(len(_hp_list)):
       _hp_list[_ip].SetStats(0)
       if((_ip+1) < 5): _hp_list[_ip].SetLineColor(_ip+1)
       else: _hp_list[_ip].SetLineColor(_ip+2)
       if _ip == 0 :
#          _hp_list[_ip].SetMaximum(_hp_list[_ip].GetMaximum()*20)
#          _hp_list[_ip].SetMaximum(1000)
          _hp_list[_ip].SetTitle("P-side")
          _hp_list[_ip].GetXaxis().SetTitle("ADC")
          _hp_list[_ip].GetYaxis().SetTitle("Counts")
#          _hp_list[_ip].Draw()
          _hp_list[_ip].DrawNormalized()
       else:
#          _hp_list[_ip].Draw("same")
          _hp_list[_ip].DrawNormalized("same")
    
    _cv.cd(2)
    #gPad.SetLogy()
    leg = ROOT.TLegend(.70,.60,.88,.88)
    leg.SetFillColor(0)
    leg.SetLineColor(0)
    leg.SetBorderSize(0)
    for _in in range(len(_hn_list)):
       leg.AddEntry(_hn_list[_in],"{0:.1f}-{1:.1f}hours".format(_in*_tr,(_in+1)*_tr))
       _hn_list[_in].SetStats(0)
       if((_in+1) < 5): _hn_list[_in].SetLineColor(_in+1)
       else: _hn_list[_in].SetLineColor(_in+2)
       if _in == 0 :
#          _hn_list[_in].SetMaximum(_hn_list[_in].GetMaximum()*20)
#          _hn_list[_in].SetMaximum(5000000)
#          _hn_list[_in].SetMaximum(1000)
          _hn_list[_in].SetTitle("N-side")
          _hn_list[_in].GetXaxis().SetTitle("ADC")
          _hn_list[_in].GetYaxis().SetTitle("Counts")
          _hn_list[_in].GetListOfFunctions().Add(leg)
#          _hn_list[_in].Draw()
          _hn_list[_in].DrawNormalized()
       else:
#          _hn_list[_in].Draw("same")
          _hn_list[_in].DrawNormalized("same")
    leg.Draw("same")

    return _cv           

def run(args):
    foldername=args.inputFolder+"/"+args.condition+"/"+args.source
    mychain=GetTChain(foldername,"eventtree")
    initUT, finalUT=getUT(mychain)   
    timerange=args.timerange*3600
    log().info("Total plots : {0} , Time range : {1} hours".format(int((finalUT-initUT)/timerange)+1, args.timerange))
    if(int((finalUT-initUT)/timerange)+1 > 10): 
       log().info("Many plots ! {}".format(int((finalUT-initUT)/timerange)+1))

    if args.plots is None:
       outputname="/Users/chiu.i-huan/Desktop/new_scientific/imageAna/run/root/"+"cdte2mmdata_"+args.condition+"_"+args.source+"_"+str(args.timerange)+"h_"+args.output+".root"
       fout=ROOT.TFile(outputname,"recreate")
       fout.cd()
       hp_list,hn_list=mkADCplots(mychain,initUT,finalUT,timerange)    
#       hp_list,hn_list=mkADCArray(mychain,initUT,finalUT,timerange)    
       for i in range(len(hp_list)):
          hp_list[i].Write()
          hn_list[i].Write()
       fout.Write()
       log().info("Done, check output file in : {}".format(outputname))
    else:
       hp_list,hn_list=getADCplots(args.plots)

    cv=mkcv(hp_list,hn_list,args.timerange)
    outcv_name="/Users/chiu.i-huan/Desktop/"+"cv_"+args.condition+"_"+args.source+"_"+str(args.timerange)+"h_"+args.output+".pdf"
    cv.SaveAs(outcv_name)

if __name__=="__main__":

   parser = argparse.ArgumentParser(description='Process some integers.')
   parser.add_argument("-i","--inputFolder", type=str, default="/Users/chiu.i-huan/Desktop/new_scientific/imageAna/data/minami_data", help="Input File Name")
   parser.add_argument("-p","--plots", type=str, default=None, help="Input File Name")
   parser.add_argument("-c","--condition", type=str, default="300n20", help="Condition : 300n20 400n20 500n20")
   parser.add_argument("-s","--source", type=str, default="Am", help="Input Source : Am Ba Co")
   parser.add_argument("-o","--output",type=str, default="stability", help="Name of output file")
   parser.add_argument("-tr","--timerange",type=float, default=3, help="Time range (Hours)")
   args = parser.parse_args()

   run(args)

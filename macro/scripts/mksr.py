#!/usr/bin/env python
#-*- coding:utf-8 -*-
"""
This module makes the system response
"""
__author__    = "I-Huan CHIU"
__email__     = "ichiu@chem.sci.osaka-u.ac.jp"
__created__   = "2020-07-07"
__copyright__ = "Copyright 2019 I-Huan CHIU"
__license__   = "GPL http://www.gnu.org/licenses/gpl.html"

# modules
import sys,os,random,math,time,ROOT,argparse
from ROOT import TFile, TTree, gROOT, TCut, gDirectory
gROOT.SetBatch(1)
sys.path.append('/Users/chiu.i-huan/Desktop/new_scientific/macro/utils/')
sys.path.append('/Users/chiu.i-huan/Desktop/new_scientific/macro/')
ROOT.gErrorIgnoreLevel = ROOT.kWarning
from logger import log, supports_color
import enums
from root_numpy import hist2array, array2hist, tree2array
import numpy as np

def GetImageSpace(filename,npixels,mypoint):
    # Object spcae to image spcae
    weight, sumw = 0,0
    imagearray_list, weight_list=[],[]
    f=ROOT.TFile(filename,"read")
    for i in range(n_images):
      _name = "image_pos"+str(i)
      imagearray_list.append(hist2array(f.Get(_name)))
    for i in range(len(imagearray_list)):
       # TODO make mypoint and pixel_axis
       # mypoint, and pixel_axis[i] are array [x,y,z]
       weight=np.sum((mypoint-pixel_axis[i])**2)#Inverse square distance
       sumw+=weight
       weight_list.append(weight)# use this weight_list to find image for mypoint
    for i in range(len(imagearray_list)):
       myimageA+=imagearray_list[i]*weight_list[i]
    return myimageA

def mkSystemResponse(filename,n_images):
    am241_intensity = 363.1*1000 #Bq
    _time=600 #second
    image_list=[]
    f=ROOT.TFile(filename,"read")
    for i in range(n_images):    
       _name = "image_pos"+str(i)
       image_list.append(f.Get(_name))
    _sr=np.zeros((len(image_list),image_list[0].GetNbinsX(),image_list[0].GetNbinsY()),dtype=float)
    print(image_list[0].GetXaxis().GetBinCenter(1))
    for i in range(len(image_list)):
       _sr[i]=hist2array(image_list[i])
    _sr = _sr/(am241_intensity*_time)
    print(_sr[0])
    return _sr

def GuessInitObjectSpace(_object):
    # make inital object 
    return _obforSR

#def getImageSpace(_object):
#    _image = _object*A # ???
#    return _image

def IterativeMLEM(_sysRespond, _object, _image):
    return 0

def testrun(args):
    _sr=mkSystemResponse(args.inputFolder, args.nimages)

    #no need
    fout=ROOT.TFile("/Users/chiu.i-huan/Desktop/mytesth3output.root", 'recreate' )
    h3=ROOT.TH3D("h3","h3",_sr.shape[0], 0, 125,_sr.shape[1], -16, 16,_sr.shape[2],-16,16)
    array2hist(_sr,h3)
    fout.cd()
    h3.Write()

    exit(0)

if __name__=="__main__":

   parser = argparse.ArgumentParser(description='Process some integers.')
   parser.add_argument("-i","--inputFolder", type=str, default="/Users/chiu.i-huan/Desktop/new_scientific/run/root/20200406a_5to27_cali_calidata_split.root", help="Input File Name")
   parser.add_argument("-n","--nimages",dest="nimages",type=int, default=125, help="Number of images")
   args = parser.parse_args()

   testrun(args)

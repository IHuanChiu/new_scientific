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

def GetImageSpace(filename,npixels,npoints,nbins,mypoint):
    # Object spcae to image spcae (by weighting image)
    pixel_axis=[]
    index,stepsize=0,10
    for ix in range(npoints):
       for iy in range(npoints):
          for iz in range(npoints):
             pixel_axis.append([(ix-2)*stepsize, (iy-2)*stepsize, (iz-2)*stepsize])

    weight, sumw = 0,0
    imagearray_list, weight_list=[],[]
    myimageA = np.zeros((nbins,nbins),dtype=float)
    f=ROOT.TFile(filename,"read")
    for i in range(pow(npoints,3)):
      # get cal. images
      _name = "image_pos"+str(i)
      imagearray_list.append(hist2array(f.Get(_name)))
    for i in range(pow(npoints,3)):
       # get weight from each imges
       if (np.sum(((mypoint-pixel_axis[i])**2)) == 0): mypoint=mypoint+0.00000000001 #skip divide by zero
       weight=1/np.sum(((mypoint-pixel_axis[i])**2))#Inverse square distance
       sumw+=weight
       weight_list.append(weight)# use this weight_list to find image for mypoint
    for i in range(pow(npoints,3)):
       # find corresponding image from the giving object space
       myimageA+=imagearray_list[i]*(weight_list[i]/sumw)
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
    for i in range(len(image_list)):
       _sr[i]=hist2array(image_list[i])
    _sr = _sr/(am241_intensity*_time)
    return _sr

def GuessInitObjectSpace(_object,npixels):
    _obAxis=[]
    for _index in range(pow(npixels,3)):
       _obAxis=[10,10,10]#make axis from object space
    return _obAxis

def IterativeMLEM(_sysRespond, _object, _image):
    return 0

def testrun(args):
    _sr=mkSystemResponse(args.inputFolder, args.nimages)
    testpoint=np.array([5,5,5])
    testimage = GetImageSpace(args.inputFolder,128,5,128,testpoint)

    #no need
    fout=ROOT.TFile("/Users/chiu.i-huan/Desktop/mytesth3output.root", 'recreate' )
    h3=ROOT.TH3D("h3","h3",_sr.shape[0], 0, 125,_sr.shape[1], -16, 16,_sr.shape[2],-16,16)
    array2hist(_sr,h3)
    fout.cd()
    h3.Write()

    h2=ROOT.TH2D("h2","h2",testimage.shape[0], -16, 16,testimage.shape[1], -16, 16)
    array2hist(testimage,h2)
    h2.Write()

    exit(0)

if __name__=="__main__":

   parser = argparse.ArgumentParser(description='Process some integers.')
   parser.add_argument("-i","--inputFolder", type=str, default="/Users/chiu.i-huan/Desktop/new_scientific/run/root/20200406a_5to27_cali_calidata_split.root", help="Input File Name")
   parser.add_argument("-n","--nimages",dest="nimages",type=int, default=125, help="Number of images")
   args = parser.parse_args()

   testrun(args)

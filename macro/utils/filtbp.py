#!/usr/bin/env python    
#-*- coding:utf-8 -*-   
"""
This module provides the filter back projection
"""
__author__    = "I-Huan CHIU"
__email__     = "ichiu@chem.sci.osaka-u.ac.jp"
__created__   = "2020-07-07"
__copyright__ = "Copyright 2019 I-Huan CHIU"
__license__   = "GPL http://www.gnu.org/licenses/gpl.html"

# modules
import sys,os,random,math,time,ROOT
from ROOT import TFile, TTree, gROOT, TCut, gDirectory
ROOT.gROOT.SetBatch(1)
import argparse
ROOT.gErrorIgnoreLevel = ROOT.kWarning
from logger import log, supports_color
import enums
from enums import getangle

from root_numpy import hist2array, array2hist, tree2array
import numpy as np
from scipy.fftpack import fft, fftshift, ifft, dct, idct

def arangeMod(start, stop=None, step=1, nx=1, ny=1):
    """#Modified version of numpy.arange which corrects error associated with non-integer step size"""
    if stop == None:
        a = np.arange(start)
    else:
        a = np.arange(start, stop, step).reshape(nx,ny)
        if a[-1][-1] > stop-step:
            a = np.delete(a, -1)
    return a

class SimpleBackProjection():
      def __init__(self, h2list=None):
          self.ihlist = h2list
          self.h3d = self.process()

      def process(self):
          _h3d = ROOT.TH3D("solid","solid",128,-16,16,128,-16,16,128,-16,16)
          _h3d.SetXTitle("x")
          _h3d.SetYTitle("y")
          _h3d.SetZTitle("z")
          ti = time.time()
          numoff=0
          for h2 in self.ihlist:
             numoff+=1
             h2name = h2.GetTitle()
      #       rfile   =  ROOT.TFile(ifile)
      #       h2   =  rfile.Get("h2")
      #       h2name = ifile.split("/")[-1]
      #       log().info("Current file : %s , Angle is %.1f\u00b0"%(h2name, math.degrees(getangle(h2name))))
             log().info("Current Angle is %.1f\u00b0"%(math.degrees(getangle(h2name))))
             for ibinx in range(1,_h3d.GetXaxis().GetNbins()+1):
                for ibiny in range(1,_h3d.GetYaxis().GetNbins()+1):
                   for ibinz in range(1,_h3d.GetZaxis().GetNbins()+1):
                      x,y,z,content = self.getContent(ibinx, ibiny, ibinz, h2, h2name, _h3d)
                      _h3d.Fill(x,y,z,content)
             log().info("Running time : %.1f s , (%s/%s) files "%(time.time() - ti, numoff, len(self.ihlist))) 
          return _h3d  

      def getContent(self,ibinx, ibiny, ibinz, h2, h2name, _h3):
          _angle=getangle(h2name)
          _content = h2.GetBinContent(ibinx,ibiny)
          _x,_y,_z = self.GetRotation(_h3.GetXaxis().GetBinCenter(ibinx), _h3.GetYaxis().GetBinCenter(ibiny), _h3.GetYaxis().GetBinCenter(ibinz),_angle)
          return _x,_y,_z, _content

      def GetRotation(self,_x,_y,_z,_angle):
          c, s = np.cos(_angle), np.sin(_angle)
          #R = np.matrix([[c, -s, 0], [s, c,0], [0,0,1]]) # around z-axis
          #R = np.matrix([[c,0,s], [0,1,0], [-s,0,c]]) # around y-axis
          R = np.matrix([[1,0,0], [0,c,-s], [0,s,c]]) # around x-axis
          v = np.matrix( [ _x, _y, _z ])
          new_v = R*v.reshape(3,1)
          return new_v[0,0], new_v[1,0], new_v[2,0]

class Filter():
      def __init__(self, h2list=None):
          self.h2list = h2list
          self.filth2 = []
          self.myarray, self.myangle = self.defProj()
          self.filtarray = self.defFilter()
          self.filtH3 = self.getBackProject()

      def defProj(self):
          h2arraylist = np.zeros((len(self.h2list),self.h2list[0].GetNbinsX(),self.h2list[0].GetNbinsY()), dtype=int)
          _alist = []
          for ih2 in range(len(self.h2list)):
            h2arraylist[ih2,:] = hist2array(self.h2list[ih2])
            _alist.append(getangle(self.h2list[ih2].GetTitle()))
          return h2arraylist, np.array(_alist)
      
      def defFilter(self): 
          numAngles, projLenX, projLenY = self.myarray.shape
#          w = arangeMod(-np.pi, np.pi, step, projLenX, projLenY)
          step = 2*np.pi/(projLenX*projLenY)
          w = np.arange(-np.pi, np.pi, step).reshape(projLenX,projLenY)

          # === ramp filter ===
          a = 1
          rn1 = abs(2/a*np.sin(a*w/2))
          rn2 = np.sin(a*w/2)/(a*w/2)
          r = rn1*(rn2)**2
          filt = fftshift(r)

          filtSino = np.zeros((numAngles,projLenX,projLenY), dtype=int)
          for i in range(numAngles):
             projfft = fft(self.myarray[i,:])
             filtProj = projfft*filt# accumulate, convolution
             filtSino[i,:] = np.real(ifft(filtProj)) #get real part (Filtered projection data)
#             filtSino[i,:] = self.myarray[i,:] # same with SBP
             _filth2 = ROOT.TH2D("h{}_filt".format(i),"h{}_filt".format(i),128,-16,16,128,-16,16)
             array2hist(filtSino[i,:], _filth2)
             _filth2.Rebin2D(4,4)
             self.filth2.append(_filth2)
          return filtSino
      
      def getBackProject(self):
          H2Range=16 #mm
          LenOfHist = self.filtarray.shape[1]
          numAngles = self.filtarray.shape[0]
          reconMatrix = np.zeros((LenOfHist,LenOfHist,LenOfHist), dtype=int)

          # === coordinate rotation ===
          x = np.arange(LenOfHist)-LenOfHist/2 # set -16 to 16 and centered at 0 
          y, z = x.copy(), x.copy()
          X, Z, Y = np.meshgrid(x, y, z) # make rotation xyz-axis
   
          for i in range(numAngles):
             _angle = self.myangle[i]
             _filth2 = self.filtarray[i,:]# 128*128 matrix

             """  
             Explanation: 
             rotation around x-axis, Xrot = X, Yrot = Y*cos - Z*sin, Zrot = Y*sin + Z*cos (try np.einsum ?)
             after rotantion, use Xrot and Yrot to get entry from _filth2 (so Xrot and Yrot can not exceed the size of the original)
             get the 3D index from rotantion coordinates (m0, m1, m2), and then make plot in projMatrix (back projection)
             no index (exceed the size of _filth2) will be zero
             reconMatrix is used to integral all BP plots
             """
             Yrot = Y*np.sin(_angle)-Z*np.cos(_angle)# Yrot is a 128*128*128 3D matrix
             YrotCor = np.round(Yrot+LenOfHist/2) # shift back to original image coordinates, round values to make indices
             YrotCor = YrotCor.astype('int')
             XCor = np.round(X+LenOfHist/2)
             XCor = XCor.astype('int')
             m0, m1, m2 = np.where((YrotCor >= 0) & (YrotCor <= (LenOfHist-1)))# find index, condition: after rotation, YrotCor doesn't exceed the size of the original

             projMatrix = np.zeros((LenOfHist, LenOfHist, LenOfHist), dtype=int) # new proj for each angle
             projMatrix[m0, m1, m2] = _filth2[XCor[m0, m1, m2],YrotCor[m0, m1, m2]]# backproject, projMatrix is 2097152 1D matrix
             reconMatrix += projMatrix # integral
             reconMatrix.reshape(LenOfHist,LenOfHist,LenOfHist) # back to 128*128*128 3D matrix

          recon = ROOT.TH3D("solid","solid",reconMatrix.shape[0],-H2Range,H2Range,reconMatrix.shape[1],-H2Range,H2Range,reconMatrix.shape[2],-H2Range,H2Range)
          array2hist(reconMatrix,recon)
          recon.SetXTitle("x")
          recon.SetYTitle("y")
          recon.SetZTitle("z")
          return recon


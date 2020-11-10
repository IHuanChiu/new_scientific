#!/usr/bin/env python
#-*- coding:utf-8 -*-
"""
This module makes the system response
"""
__author__    = "I-Huan CHIU"
__email__     = "ichiu@chem.sci.osaka-u.ac.jp"
__created__   = "2020-07-07"
__copyright__ = "Copyright 2020 I-Huan CHIU"
__license__   = "GPL http://www.gnu.org/licenses/gpl.html"

# modules
import sys,os,random,math,time,ROOT,argparse, ctypes
from ROOT import TFile, TTree, gROOT, TCut, gDirectory, TMinuit, Long, Double, TMath, AddressOf
gROOT.SetBatch(1)
sys.path.append('/Users/chiu.i-huan/Desktop/new_scientific/macro/utils/')
sys.path.append('/Users/chiu.i-huan/Desktop/new_scientific/macro/')
ROOT.gErrorIgnoreLevel = ROOT.kWarning
from logger import log, supports_color
from helpers import GetTChain, createRatioCanvas, ProgressBar
import enums
from root_numpy import hist2array, array2hist, tree2array
import numpy as np
from array import array
from scipy import ndimage, misc

gROOT.ProcessLine(
"struct MLEMStruct {\
   Double_t  mlemx;\
   Double_t  mlemy;\
};"
);

from ROOT import MLEMStruct
mlstruct = MLEMStruct()
paramater_list,point_axis=[],[]
hole_axis=[0.001,0.001,-113]

# ======================= find the paramaters by fitting ===================
class PrepareParameters():
      def __init__(self,filename=None,npoints=None,stepsize=None,npixels=None,nbins=None):
          self.filename=filename
          self.npoints=npoints
          self.stepsize=stepsize
          self.npixels=npixels
          self.nbins=nbins
          self.imagearray = self.getimages()
          self.hist_fit = self.fitting_para()

      def getimages(self):
          global point_axis
          imagearray,point_axis=[],[]
          f=ROOT.TFile(self.filename,"read")
          index=0
          for iz in range(self.npoints):
             for iy in range(self.npoints):
                for ix in range(self.npoints):
                   point_axis.append([(ix-2)*self.stepsize, (iy-2)*self.stepsize, (iz-2)*self.stepsize])
                   _name = "image_pos"+str(index)
                   imagearray.append(hist2array(f.Get(_name)))
                   index+=1
          return imagearray

      def getfunc(self, name, _xdown, _xup, _ydown, _yup):
          myfunction = "bigaus"
          #paramaters for bigaus: Constant, MeanX, SigmaX, MeanY, SigmaY, Rho
          return ROOT.TF2(name,myfunction,_xdown,_xup,_ydown,_yup)

      def fitting_para(self):
          log().info("Progressing the paramaters by fitting ...")
          global paramater_list
          paramater_list,hist_fitlist=[], []
          xcenter, ycenter = [15.5,7.5,0,-7.5,-15], [15.5,7.5,0,-7.5,-15]
          fit_range=10
          index, constant, xup, xdown, yup, ydown, rho=0,0,0,0,0,0,0
          print(" _____________________________________________________________________________________________________ ")
          print(" __________________________________________ START ____________________________________________________ ")
          for iz in range(self.npoints):
             for iy in range(self.npoints):
                for ix in range(self.npoints):               
                   _h2name="_image_"+str(index)
                   h2=ROOT.TH2F(_h2name,_h2name,128,-16,16,128,-16,16)        
                   array2hist(self.imagearray[index],h2)
                   xup=xcenter[ix]+fit_range
                   xdown=xcenter[ix]-fit_range
                   yup=ycenter[iy]+fit_range
                   ydown=ycenter[iy]-fit_range
                   gb=self.getfunc("gb"+str(index),xdown,xup,ydown,yup)
                   gb.SetParameters(10,xcenter[ix],0,ycenter[iy],0,0.1)
                   # bad fitting channels
                   if index == 1: constant,mean_x,sigma_x,mean_y,sigma_y,rho=1.74254e+02,8.10055e+00,1.72548e+00,1.50197e+01,1.49098e+00,-9.93072e-02
                   elif index == 10: constant,mean_x,sigma_x,mean_y,sigma_y,rho=2.75625e+02,1.61334e+01,2.03669e+00,-1.09053e-01,1.87555e+00,1.30457e-01
                   elif index == 26: constant,mean_x,sigma_x,mean_y,sigma_y,rho=1.95446e+02,7.34044e+00,1.82564e+00,1.40217e+01,1.73770e+00,2.42294e-02
                   elif index == 81: constant,mean_x,sigma_x,mean_y,sigma_y,rho=1.49021e+02,6.13308e+00,1.74712e+00,5.69160e+00,1.85554e+00,-1.01725e-01
                   elif index == 100: constant,mean_x,sigma_x,mean_y,sigma_y,rho=1.18486e+02,1.12588e+01,1.95410e+00,1.05471e+01,1.80264e+00,-8.80853e-02
                   elif index == 110: constant,mean_x,sigma_x,mean_y,sigma_y,rho=1.41792e+02,1.09893e+01,1.89663e+00,-2.30509e-01,1.95740e+00,9.20033e-02
                   elif index == 122: constant,mean_x,sigma_x,mean_y,sigma_y,rho=1.25659e+02,1.06397e-01,1.69141e+00,-1.10063e+01,1.94154e+00,5.99720e-02
                   else:
                      Chi2=999999999
                      for fittime in range(5):
                         h2.Fit("gb"+str(index),"QR")
                         if Chi2 > gb.GetChisquare():
                            Chi2=gb.GetChisquare()
                            constant, mean_x, sigma_x, mean_y, sigma_y, rho = gb.GetParameter(0), gb.GetParameter(1), gb.GetParameter(2), gb.GetParameter(3), gb.GetParameter(4), gb.GetParameter(5)
                   paramater_list.append([constant, mean_x, sigma_x, mean_y, sigma_y, rho])                  
                   hist_fitlist.append(h2)
                   if ix != -1 and iy != -1:
                      print("index: {0}, fitting (constant, mux, muy, sigmax, sigmay, \u03C1) = ({1:.3f},{2:.3f},{3:.3f},{4:.3f},{5:.3f},{6:.3f})".format(index,constant,mean_x,mean_y,sigma_x,sigma_y,rho))
                   # Cheching bad fitting channels
                   if paramater_list[index][0] > 1000: 
                      log().warn("bad fitting point : {0}, {1}".format(index, paramater_list[index]))

                   index+=1
                   del gb,h2
          print(" ___________________________________________ END _____________________________________________________ ")
          print(" _____________________________________________________________________________________________________ ")
          return hist_fitlist

# ======================= fit with TMinuit for the varaibles of function ===================
def deffunc(_x,_y,_z,par):         
    func=par[0]+par[1]*_x+par[2]*_y+par[3]*_z
    return func
def constantfunc(_x,_y,_z,par):         
    func=par[0]*math.exp((-1)*(par[1]/((191+_z)**2+_x**2+_y**2))+par[2])+par[3]
    if _z == -10: 
       if abs(_x) == 20: func=func*0.9
       if abs(_y) == 20: func=func*0.9
    if _z == -20: 
       if abs(_x) == 20: func=func*0.5
       if abs(_y) == 20: func=func*0.5
    return func
def muxfunc(_x,_y,_z,par):         
    denominator=(((hole_axis[1]-_y)/(hole_axis[0]-_x)*par[3]-par[4])*((hole_axis[2]-_z)/(hole_axis[0]-_x)*par[6]-par[8])-((hole_axis[2]-_z)/(hole_axis[0]-_x)*par[3]-par[5])*((hole_axis[1]-_y)/(hole_axis[0]-_x)*par[6]-par[7]))
    if denominator == 0 : denominator = 0.00001
    numerator=((par[1]-_y-((hole_axis[1]-_y)*(par[0]-_x)/(hole_axis[0]-_x)))*((hole_axis[2]-_z)/(hole_axis[0]-_x)*par[6]-par[8])-(par[2]-_z-(hole_axis[2]-_z)*(par[0]-_x)/(hole_axis[0]-_x))*((hole_axis[1]-_y)/(hole_axis[0]-_x)*par[6]-par[7]))
    mux=numerator/denominator
    return mux
def muyfunc(_x,_y,_z,par):         
    denominator=(((hole_axis[2]-_z)/(hole_axis[0]-_x)*par[3]-par[5])*((hole_axis[1]-_y)/(hole_axis[0]-_x)*par[6]-par[7])-((hole_axis[1]-_y)/(hole_axis[0]-_x)*par[3]-par[4])*((hole_axis[2]-_z)/(hole_axis[0]-_x)*par[6]-par[8]))
    if denominator == 0 : denominator = 0.00001
    numerator=((par[1]-_y-((hole_axis[1]-_y)*(par[0]-_x)/(hole_axis[0]-_x)))*((hole_axis[2]-_z)/(hole_axis[0]-_x)*par[3]-par[5])-(par[2]-_z-(hole_axis[2]-_z)*(par[0]-_x)/(hole_axis[0]-_x))*((hole_axis[1]-_y)/(hole_axis[0]-_x)*par[3]-par[4]))
    muy=numerator/denominator
    return muy

def fcn_constant(npar, gin, f, par, iflag):
    chisq, npoints = 0., 5
    for _index in range(pow(npoints,3)):
       #chisq += pow((paramater_list[_index][0] - deffunc(point_axis[_index][0],point_axis[_index][1],point_axis[_index][2],par)),2)
       chisq += pow((paramater_list[_index][0] - constantfunc(point_axis[_index][0],point_axis[_index][1],point_axis[_index][2],par)),2)
    f[0] = chisq
def fcn_x(npar, gin, f, par, iflag):
    chisq, npoints = 0., 5
    for _index in range(pow(npoints,3)):
       chisq += pow((paramater_list[_index][1] - muxfunc(point_axis[_index][0],point_axis[_index][1],point_axis[_index][2],par)),2)
    f[0] = chisq
def fcn_x2(npar, gin, f, par, iflag):
    chisq, npoints = 0., 5
    for _index in range(pow(npoints,3)):
       chisq += pow((paramater_list[_index][1] - deffunc(point_axis[_index][0],point_axis[_index][1],point_axis[_index][2],par)),2)
    f[0] = chisq
def fcn_xsig(npar, gin, f, par, iflag):
    chisq, npoints = 0., 5
    for _index in range(pow(npoints,3)):
       chisq += pow((paramater_list[_index][2] - deffunc(point_axis[_index][0],point_axis[_index][1],point_axis[_index][2],par)),2)
    f[0] = chisq
def fcn_y(npar, gin, f, par, iflag):
    chisq, npoints = 0., 5
    for _index in range(pow(npoints,3)):
       chisq += pow((paramater_list[_index][3] - muyfunc(point_axis[_index][0],point_axis[_index][1],point_axis[_index][2],par)),2)
    f[0] = chisq
def fcn_y2(npar, gin, f, par, iflag):
    chisq, npoints = 0., 5
    for _index in range(pow(npoints,3)):
       chisq += pow((paramater_list[_index][3] - deffunc(point_axis[_index][0],point_axis[_index][1],point_axis[_index][2],par)),2)
    f[0] = chisq
def fcn_ysig(npar, gin, f, par, iflag):
    chisq, npoints = 0., 5
    for _index in range(pow(npoints,3)):
       chisq += pow((paramater_list[_index][4] - deffunc(point_axis[_index][0],point_axis[_index][1],point_axis[_index][2],par)),2)
    f[0] = chisq
def fcn_rho(npar, gin, f, par, iflag):
    chisq, npoints = 0., 5
    for _index in range(pow(npoints,3)):
       chisq += pow((paramater_list[_index][5] - deffunc(point_axis[_index][0],point_axis[_index][1],point_axis[_index][2],par)),2)
    f[0] = chisq


class SystemResponse():
      def __init__(self,fittype=None):
          if fittype:
             if "plane" in fittype or "Plane" in fittype:
                self.fittype = "plane"
             elif "vector" in fittype or "Vector" in fittype:
                self.fittype = "vector"
             else: self.fittype = "vector"
          else: self.fittype = "vector"

          self.par_con_x_xsig_y_ysig_rho = self.GetSRpar()

      def Minuit_plane(self, fcn):
          gMinuit = TMinuit(4)
          gMinuit.SetPrintLevel(-1) # -1  quiet, 0  normal, 1  verbose
          gMinuit.SetFCN( fcn )
          arglist = array( 'd', 10*[0.] )
          ierflg = ctypes.c_int(1982)
         
          arglist[0] = 1
          gMinuit.mnexcm( "SET ERR", arglist, 1, ierflg )
         
          # Set starting values and step sizes for parameters
          vstart = array( 'd', ( paramater_list[0][0],  1,  0.1,  0.01  ) )
          step   = array( 'd', ( 0.1, 0.1, 0.01, 0.001 ) )
          gMinuit.mnparm( 0, "par0", vstart[0], step[0], 0, 0, ierflg )
          gMinuit.mnparm( 1, "parx", vstart[1], step[1], 0, 0, ierflg )
          gMinuit.mnparm( 2, "pary", vstart[2], step[2], 0, 0, ierflg )
          gMinuit.mnparm( 3, "parz", vstart[3], step[3], 0, 0, ierflg )
         
          # Now ready for minimization step
          arglist[0] = 1500 # number of function calls
          arglist[1] = 0.01 # tolerance
          gMinuit.mnexcm( "MIGRAD", arglist, 2, ierflg )
         
          # Print results
          par0,par1,par2,par3 = map(ctypes.c_double, (0,0,0,0))
          par0_err,par1_err,par2_err,par3_err = map(ctypes.c_double, (0,0,0,0))
          amin, edm, errdef = map(ctypes.c_double, (0.18, 0.19, 0.20))
          nvpar, nparx, icstat = map(ctypes.c_int, (1983, 1984, 1985))
          gMinuit.mnstat( amin, edm, errdef, nvpar, nparx, icstat )
          gMinuit.GetParameter(0,par0,par0_err)
          gMinuit.GetParameter(1,par1,par1_err)
          gMinuit.GetParameter(2,par2,par2_err)
          gMinuit.GetParameter(3,par3,par3_err)
          return [par0,par1,par2,par3]

      def Minuit_vector(self, fcn):
          gMinuit = TMinuit(9)
          gMinuit.SetPrintLevel(-1) # -1  quiet, 0  normal, 1  verbose
          gMinuit.SetFCN( fcn )
          arglist = array( 'd', 10*[0.] )
          ierflg = ctypes.c_int(1982)
          arglist[0] = 1
          gMinuit.mnexcm( "SET ERR", arglist, 1, ierflg )
          vstart = array( 'd', ( -5, -5, -191, 0.1, 0.1, 0.001, 0.1, 0.1, 0.001 ) )
          step   = array( 'd', ( 0.01, 0.01, 0.01, 0.1, 0.1, 0.001, 0.1, 0.1, 0.001 ) )
          gMinuit.mnparm( 0, "d0", vstart[0], step[0], 0, 0, ierflg )
          gMinuit.mnparm( 1, "d1", vstart[1], step[1], 0, 0, ierflg )
          gMinuit.mnparm( 2, "d2", vstart[2], step[2], 0, 0, ierflg )
          gMinuit.mnparm( 3, "l0", vstart[3], step[3], 0, 0, ierflg )
          gMinuit.mnparm( 4, "l1", vstart[4], step[4], 0, 0, ierflg )
          gMinuit.mnparm( 5, "l2", vstart[5], step[5], 0, 0, ierflg )
          gMinuit.mnparm( 6, "k0", vstart[6], step[6], 0, 0, ierflg )
          gMinuit.mnparm( 7, "k1", vstart[7], step[7], 0, 0, ierflg )
          gMinuit.mnparm( 8, "k2", vstart[8], step[8], 0, 0, ierflg )
          arglist[0] = 15000000
          arglist[1] = 0.01
          gMinuit.mnexcm( "MIGRAD", arglist, 2, ierflg )
          par0,par1,par2,par3,par4,par5,par6,par7,par8 = map(ctypes.c_double, (0,0,0,0,0,0,0,0,0))
          par0_err,par1_err,par2_err,par3_err,par4_err,par5_err,par6_err,par7_err,par8_err = map(ctypes.c_double, (0,0,0,0,0,0,0,0,0))
          amin, edm, errdef = map(ctypes.c_double, (0.18, 0.19, 0.20))
          nvpar, nparx, icstat = map(ctypes.c_int, (1983, 1984, 1985))
          gMinuit.mnstat( amin, edm, errdef, nvpar, nparx, icstat )
          gMinuit.GetParameter(0,par0,par0_err)
          gMinuit.GetParameter(1,par1,par1_err)
          gMinuit.GetParameter(2,par2,par2_err)
          gMinuit.GetParameter(3,par3,par3_err)
          gMinuit.GetParameter(4,par4,par4_err)
          gMinuit.GetParameter(5,par5,par5_err)
          gMinuit.GetParameter(6,par6,par6_err)
          gMinuit.GetParameter(7,par7,par7_err)
          gMinuit.GetParameter(8,par8,par8_err)
          return [par0,par1,par2,par3,par4,par5,par6,par7,par8]

      def dofit(self, parname):
          para_list=[]
          # === define fcn ===
          if parname == "constant": fcn = fcn_constant
          if parname == "x": 
             if self.fittype == "vector": fcn = fcn_x
             if self.fittype == "plane": fcn = fcn_x2
          if parname == "xsig": fcn = fcn_xsig
          if parname == "y":
             if self.fittype == "vector": fcn = fcn_y
             if self.fittype == "plane": fcn = fcn_y2
          if parname == "ysig": fcn = fcn_ysig
          if parname == "rho": fcn = fcn_rho

          #=== fitting wiht Minuit ===
          if self.fittype == "plane":
             para_list=self.Minuit_plane(fcn) # plane method
          elif self.fittype == "vector":
             if parname != "x" and parname != "y":
                para_list=self.Minuit_plane(fcn) # plane method
             else: 
                para_list=self.Minuit_vector(fcn) # vector method

          return para_list

      def GetSRpar(self):
          _par_con_x_xsig_y_ysig_rho={}
          _par_con_x_xsig_y_ysig_rho.update({"constant":self.dofit("constant")})
          _par_con_x_xsig_y_ysig_rho.update({"x":self.dofit("x")})
          _par_con_x_xsig_y_ysig_rho.update({"xsig":self.dofit("xsig")})
          _par_con_x_xsig_y_ysig_rho.update({"y":self.dofit("y")})
          _par_con_x_xsig_y_ysig_rho.update({"ysig":self.dofit("ysig")})
          _par_con_x_xsig_y_ysig_rho.update({"rho":self.dofit("rho")})
          return _par_con_x_xsig_y_ysig_rho

# ======================= Maximum Likelihood Expectation Maximization ===================
class MLEM():
      def __init__(self,PPclass=None,SRclass=None,npoints=None,nbins=None,npixels=None,matrix=None,imageinput=None):
          # === class members ===
          self.PP=PPclass
          self.SR=SRclass
          # === setup varaibles ===
          self.nbins=nbins
          self.npoints=npoints
          self.npixels=npixels
          self.object_range=20 #mm
          # === class members ===
          self.mlemhist_list,self.mlemhist_proje_list,self.mlemratio_list,self.h_data_list=[],[],[],[]
          self.source_intensity = 363.1*1000 #Bq, Am-241
          # === get paramaters ===
          self.hist_fit=self.PP.hist_fit
          self.para_dic=self.SR.par_con_x_xsig_y_ysig_rho
          self.ori_image_list=self.PP.imagearray
          self.ob2im_dic=self.mksrfdic()
          if not isinstance(matrix, np.ndarray): self.matrix=self.mkmatrix()
          else: self.matrix=matrix
          # === plots and tree ===
          self.image_hx_hy_list_ori, self.image_hx_hy_list_sr, self.image_hx_hy_list_matrix, self.hist_delta_mu=self.mkimage()
          self.mlemtree=self.mktree()
          self.object_init=self.mkInitObject()
          self.h_measurement_list,self.h_angle_list,self.h_name_list=self.getmeasurement(inputname=imageinput)

      def movemeasurement(self,_harray):
          _image=np.zeros((self.nbins,self.nbins),dtype=float)
          image=np.zeros((self.nbins,self.nbins),dtype=float)
          xmov,ymov=16,4
          for i in range(self.nbins-xmov):
             _image[i]=_harray[i+xmov]
          for j in range(self.nbins-ymov):
             image[:,j]=_image[:,j+ymov]
          #TODO cut data
          #for c in range(10):
          #   _image[c]=0
          #   _image[127-c]=0
          #   _image[:,c]=0
          #   _image[:,127-c]=0
          return image
          
      def getmeasurement(self,inputname):
          """ === return array type ==="""
          log().info("Getting measurment data...")
          _mlist,_anglelist,_namelist=[],[],[]

          fint=ROOT.TFile(inputname,"read")
          n_angles=16 # always 16 for J-PARC data, related to angle
          for i in range(n_angles):
             #if i%10 != 0: continue
             #if i == 0 : continue
             _h=fint.Get("h"+str(i))
             _h.SetDirectory(0)
             #_harray=hist2array(_h)
             _harray=self.movemeasurement(hist2array(_h))
             _mlist.append(_harray)          
             _anglelist.append((-1)*i*(360/n_angles))# use Angle for ratation, not Radian
             _namelist.append(_h.GetName())
             hmov=ROOT.TH2D(_h.GetName(),_h.GetName(),128,-16,16,128,-16,16)
             hmov.SetDirectory(0)
             array2hist(_harray,hmov)
             #self.h_data_list.append(_h)
             self.h_data_list.append(hmov)
          return _mlist,_anglelist,_namelist

      def getconstant(self,_x,_y,_z,par):         
          _c=par[0].value*math.exp((-1)*(par[1].value/((191+_z)**2+_x**2+_y**2))+par[2].value)+par[3].value
          return _c

      def getmu(self,_x,_y,_z,par,name):         
          if name == "x":
             denominator=(((hole_axis[1]-_y)/(hole_axis[0]-_x)*par[3].value-par[4].value)*((hole_axis[2]-_z)/(hole_axis[0]-_x)*par[6].value-par[8].value)-((hole_axis[2]-_z)/(hole_axis[0]-_x)*par[3].value-par[5].value)*((hole_axis[1]-_y)/(hole_axis[0]-_x)*par[6].value-par[7].value))
             numerator=((par[1].value-_y-((hole_axis[1]-_y)*(par[0].value-_x)/(hole_axis[0]-_x)))*((hole_axis[2]-_z)/(hole_axis[0]-_x)*par[6].value-par[8].value)-(par[2].value-_z-(hole_axis[2]-_z)*(par[0].value-_x)/(hole_axis[0]-_x))*((hole_axis[1]-_y)/(hole_axis[0]-_x)*par[6].value-par[7].value))
          if name == "y":
             denominator=(((hole_axis[2]-_z)/(hole_axis[0]-_x)*par[3].value-par[5].value)*((hole_axis[1]-_y)/(hole_axis[0]-_x)*par[6].value-par[7].value)-((hole_axis[1]-_y)/(hole_axis[0]-_x)*par[3].value-par[4].value)*((hole_axis[2]-_z)/(hole_axis[0]-_x)*par[6].value-par[8].value))
             numerator=((par[1].value-_y-((hole_axis[1]-_y)*(par[0].value-_x)/(hole_axis[0]-_x)))*((hole_axis[2]-_z)/(hole_axis[0]-_x)*par[3].value-par[5].value)-(par[2].value-_z-(hole_axis[2]-_z)*(par[0].value-_x)/(hole_axis[0]-_x))*((hole_axis[1]-_y)/(hole_axis[0]-_x)*par[3].value-par[4].value))
          return numerator/denominator

      def srf(self,_x,_y,_z,_type=None):
          """
          system response function: 
          input : object(pixel_of_x,pixel_of_y,pixel_of_z)
          output : image(x,y,xsig,ysig,intensity)
          """
          if _type == "bintype": 
             _x= -1*self.object_range+(self.object_range/self.npixels)+_x*((2.*self.object_range)/self.npixels)
             _y= -1*self.object_range+(self.object_range/self.npixels)+_y*((2.*self.object_range)/self.npixels)
             _z= -1*self.object_range+(self.object_range/self.npixels)+_z*((2.*self.object_range)/self.npixels)
          par_x, par_y, par_xsig, par_ysig, par_constant, par_rho = self.para_dic["x"], self.para_dic["y"], self.para_dic["xsig"], self.para_dic["ysig"], self.para_dic["constant"], self.para_dic["rho"]
          #image_constant = par_constant[0].value+par_constant[1].value*_x+par_constant[2].value*_y+par_constant[3].value*_z         
          image_constant=self.getconstant(_x,_y,_z,par_constant) 
          if len(par_x) == 4 : image_x = par_x[0].value+par_x[1].value*_x+par_x[2].value*_y+par_x[3].value*_z
          else: image_x=self.getmu(_x,_y,_z,par_x,"x")
          image_xsig = par_xsig[0].value+par_xsig[1].value*_x+par_xsig[2].value*_y+par_xsig[3].value*_z
          if len(par_y) == 4 : image_y = par_y[0].value+par_y[1].value*_x+par_y[2].value*_y+par_y[3].value*_z
          else: image_y=self.getmu(_x,_y,_z,par_y,"y")
          image_ysig = par_ysig[0].value+par_ysig[1].value*_x+par_ysig[2].value*_y+par_ysig[3].value*_z
          image_rho = par_rho[0].value+par_rho[1].value*_x+par_rho[2].value*_y+par_rho[3].value*_z
          return [image_constant,image_x,image_xsig,image_y,image_ysig,image_rho]

      def mksrfdic(self):
          srfdic={}
          _index=0
          for z in range(self.npixels):
             for y in range(self.npixels):
                for x in range(self.npixels):
                   srfdic.update({_index:self.srf(x,y,z,"bintype")})
                   _index+=1
          return srfdic

      def mkmatrix(self):
          """ === structure of matrix : [x,y,z,mux,muy] === """
          prog = ProgressBar(ntotal=pow(self.npixels,3),text="Processing Matrix...",init_t=time.time())
          matrix=np.zeros((self.npixels,self.npixels,self.npixels,self.nbins,self.nbins),dtype=float)          
          index,nevproc=0,0
          for iz in range(self.npixels):
             for iy in range(self.npixels):
                for ix in range(self.npixels):
                   if prog: prog.update(nevproc)
                   image_var = self.ob2im_dic[index]
                   h_gaus = ROOT.TF2("h_gaus","bigaus",-16,16,-16,16)
                   h_gaus.SetParameters(image_var[0],image_var[1],image_var[2],image_var[3],image_var[4],image_var[5])

                   for imageix in range(self.nbins):
                      for imageiy in range(self.nbins):
                         _imagex=-16+0.125+imageix*(32./self.nbins)
                         _imagey=-16+0.125+imageiy*(32./self.nbins)
                         matrix[ix][iy][iz][imageix][imageiy]=(h_gaus.Eval(_imagex,_imagey)/self.source_intensity)
                   nevproc+=1
                   index+=1
          if prog: prog.finalize()
          with open('matrix_temp.npy', 'wb') as f:
             np.save(f, matrix)
          return matrix

      def mktree(self):
          log().info("Making tree...")
          mypoint=[7,7,7]
          image_var = self.srf(mypoint[0],mypoint[1],mypoint[2])
          _tree=TTree('tree','tree')          
          _tree.SetDirectory(0)
          _tree.Branch( 'mlemx', AddressOf( mlstruct, 'mlemx' ),  'mlemx/D' )
          _tree.Branch( 'mlemy', AddressOf( mlstruct, 'mlemy' ),  'mlemy/D' )
          h_gaus = ROOT.TF2("h_gaus","bigaus",-16,16,-16,16)
          h_gaus.SetParameters(image_var[0],image_var[1],image_var[2],image_var[3],image_var[4],image_var[5])
          for ix in range(128):
             for iy in range(128):
               _x=-16+(32.*ix/128)
               _y=-16+(32.*iy/128)
               mlstruct.mlemx=_x
               mlstruct.mlemy=_y
               for i in range(int(h_gaus.Eval(_x,_y))):
                  _tree.Fill()
          return _tree

      def mkimage(self):
          """ === make original vs. system response comparison plots === """
          prog = ProgressBar(ntotal=pow(self.npoints,3),text="Fitting images...",init_t=time.time())
          image_hx_hy_list_sr, image_hx_hy_list_ori, image_hx_hy_list_matrix=[],[],[]
          nevproc,_ip=0,0
          h_delta_mux=ROOT.TH1D("delta_mux","delta_mux",125,-16,16)
          h_delta_muy=ROOT.TH1D("delta_muy","delta_muy",125,-16,16)
          h_delta_sigmax=ROOT.TH1D("delta_sigmax","delta_sigmax",200,-1,1)
          h_delta_sigmay=ROOT.TH1D("delta_sigmay","delta_sigmay",200,-1,1)
          h_delta_constant=ROOT.TH1D("delta_constant","delta_constant",200,-100,100)
          h_delta_rho=ROOT.TH1D("delta_rho","delta_rho",200,-1,1)
          for _iz in range(self.npoints):
             _cvx  = createRatioCanvas("cvx_{}".format(_iz), 2500, 2500)
             _cvy  = createRatioCanvas("cvy_{}".format(_iz), 2500, 2500)
             _cvx.Divide(self.npoints,self.npoints)
             _cvy.Divide(self.npoints,self.npoints)
             _cvfit  = createRatioCanvas("cvfit_{}".format(_iz), 2500, 2500)
             _cvfit.Divide(self.npoints,self.npoints)
             _cvori  = createRatioCanvas("cvori_{}".format(_iz), 2500, 2500)
             _cvori.Divide(self.npoints,self.npoints)
             for _iy in range(self.npoints):
                for _ix in range(self.npoints):              
                   nevproc+=1
                   if prog: prog.update(nevproc)
                   # === original plots ===
                   _h2name="image_ori_"+str(_ip)             
                   _h2=ROOT.TH2F(_h2name,_h2name,self.nbins,-16,16,self.nbins,-16,16) 
                   array2hist(self.ori_image_list[_ip],_h2)
                   image_hx_hy_list_ori.append(_h2); image_hx_hy_list_ori.append(_h2.ProjectionX()); image_hx_hy_list_ori.append(_h2.ProjectionY())

                   # === system response plots (fitting after bigaus and TMinuit) ===
                   image_var = self.srf(point_axis[_ip][0], point_axis[_ip][1], point_axis[_ip][2])
                   _h2name="image_sr_"+str(_ip)
                   h2=ROOT.TH2D(_h2name,_h2name,self.nbins,-16,16,self.nbins,-16,16)
                   h2_bigaus=ROOT.TH2D(_h2name+"_bigaus",_h2name+"_bigaus",self.nbins,-16,16,self.nbins,-16,16)
                   h2_array=np.zeros((self.nbins,self.nbins),dtype=float)# MLEM
                   h2_array_bigaus=np.zeros((self.nbins,self.nbins),dtype=float)# bigaus fitting
                   h_gaus = ROOT.TF2("h_gaus","bigaus",-16,16,-16,16)
                   h_gaus.SetParameters(image_var[0],image_var[1],image_var[2],image_var[3],image_var[4],image_var[5])
                   h_gaus_fit = ROOT.TF2("h_gaus","bigaus",-16,16,-16,16)
                   h_gaus_fit.SetParameters(paramater_list[_ip][0],paramater_list[_ip][1],paramater_list[_ip][2],paramater_list[_ip][3],paramater_list[_ip][4],paramater_list[_ip][5])
                   for ix in range(128):
                      for iy in range(128):
                         _x=h2.GetXaxis().GetBinCenter(ix+1)
                         _y=h2.GetYaxis().GetBinCenter(iy+1)
                         if h_gaus.Eval(_x,_y) > 1: h2_array[ix][iy]=h_gaus.Eval(_x,_y)
                         if h_gaus_fit.Eval(_x,_y) > 1: h2_array_bigaus[ix][iy]=h_gaus_fit.Eval(_x,_y)
                   array2hist(h2_array,h2)
                   array2hist(h2_array_bigaus,h2_bigaus)
                   hx, hy = h2.ProjectionX(), h2.ProjectionY()# MLEM
                   hx_fit, hy_fit=h2_bigaus.ProjectionX(), h2_bigaus.ProjectionY()# fitting bigaus
                   hx_ori, hy_ori=_h2.ProjectionX(), h2.ProjectionY()# ori
                   image_hx_hy_list_sr.append(h2); image_hx_hy_list_sr.append(h2.ProjectionX()); image_hx_hy_list_sr.append(h2.ProjectionY());
                   image_hx_hy_list_sr.append(h2_bigaus); image_hx_hy_list_sr.append(hx_fit); image_hx_hy_list_sr.append(hy_fit)

                   # check difference between the fitting values after bigaus and TMinuit
                   h_delta_constant.Fill(image_var[0]-paramater_list[_ip][0]) 
                   h_delta_mux.Fill(image_var[1]-paramater_list[_ip][1]) 
                   h_delta_sigmax.Fill(image_var[2]-paramater_list[_ip][2]) 
                   h_delta_muy.Fill(image_var[3]-paramater_list[_ip][3]) 
                   h_delta_sigmay.Fill(image_var[4]-paramater_list[_ip][4]) 
                   h_delta_rho.Fill(image_var[5]-paramater_list[_ip][5]) 

                   # comparison canvas fitting result
                   hx.SetStats(0); hy.SetStats(0)#MLEM->red
                   hx_fit.SetStats(0); hy_fit.SetStats(0)#bigaus->blue
                   hx_ori.SetStats(0); hy_ori.SetStats(0)#ori->black
                   hx.SetLineColor(2); hy.SetLineColor(2)
                   hx_fit.SetLineColor(4); hy_fit.SetLineColor(4)
                   hx_ori.SetLineColor(1); hy_ori.SetLineColor(1)
                   hx.SetMaximum(300); hy.SetMaximum(300); hx_ori.SetMaximum(300); hy_ori.SetMaximum(300); hx_fit.SetMaximum(300); hy_fit.SetMaximum(300)

                   _cvfit.cd((_ix+1)+_iy*self.npoints)
                   h2.SetStats(0); h2.Draw("colz");
                   _cvori.cd((_ix+1)+_iy*self.npoints)
                   _h2.SetStats(0);_h2.Draw("colz");
                   _cvx.cd((_ix+1)+_iy*self.npoints) 
                   hx_ori.Draw(); hx.Draw("hist same"); hx_fit.Draw("hist same");
                   _cvy.cd((_iy+1)+_ix*self.npoints) 
                   hy_ori.Draw(); hy.Draw("hist same"); hy_fit.Draw("hist same")
                   del _h2, h2, hx, hy, h_gaus

                   # === MLEM plots with matrix ===
                   #if _ix==0 and _iy==0: 
                   #   _image_point=np.zeros((self.nbins,self.nbins),dtype=float)
                   #   _h2name="image_matrix_"+str(_ip)
                   #   h2_matrix=ROOT.TH2D(_h2name,_h2name,self.nbins,-16,16,self.nbins,-16,16)
                   #   object_point=np.zeros((self.npixels,self.npixels,self.npixels),dtype=float)
                   #   _izp, _iyp, _ixp = 0,0,0
                   #   if _iz!= 0 : _izp = _iz*10-1
                   #   if _iy!= 0 : _iyp = _iy*10-1
                   #   if _ix!= 0 : _ixp = _ix*10-1
                   #   object_point[_izp,_iyp,_ixp]=1.*self.source_intensity
                   #   for imx in range(self.nbins):
                   #      for imy in range(self.nbins):
                   #         _image_point[imx][imy]=np.sum(object_point*self.matrix[:,:,:,imx,imy])
                   #   _where_0 = np.where(_image_point < 1)
                   #   _image_point[_where_0]=0
                   #   array2hist(_image_point, h2_matrix)
                   #   h2_matrix.SetStats(0)
                   #   image_hx_hy_list_matrix.append(h2_matrix)
                   #   image_hx_hy_list_matrix.append(h2_matrix.ProjectionX())
                   #   image_hx_hy_list_matrix.append(h2_matrix.ProjectionY())
                   # === Next point ===
                   _ip+=1
   
             _pdfname = "/Users/chiu.i-huan/Desktop/new_scientific/run/figs/MLEM_comparison_x_z{}.pdf".format(_iz)
             _cvx.SaveAs(_pdfname)
             _pdfname = _pdfname.replace("_x_","_y_")
             _cvy.SaveAs(_pdfname)
             _pdfname = _pdfname.replace("_y_","_ori_")
             _cvori.SaveAs(_pdfname)
             _pdfname = _pdfname.replace("_ori_","_fit_")
             _cvfit.SaveAs(_pdfname)

          # === check entries ===
          _xp,_yp,_zp=2,2,2
          hori_entries_x=ROOT.TH1D("entries_alongx_ori","entries_alongx_ori",self.npoints,0,self.npoints)
          hori_entries_y=ROOT.TH1D("entries_alongy_ori","entries_alongy_ori",self.npoints,0,self.npoints)
          hori_entries_z=ROOT.TH1D("entries_alongz_ori","entries_alongz_ori",self.npoints,0,self.npoints)
          for _i in range(self.npoints):
             hori_entries_x.Fill(_i,np.sum(self.ori_image_list[25*_zp+5*_yp+1*_i])) 
             hori_entries_y.Fill(_i,np.sum(self.ori_image_list[25*_zp+5*_i+1*_xp])) 
             hori_entries_z.Fill(_i,np.sum(self.ori_image_list[25*_i+5*_yp+1*_xp])) 
          _xp,_yp,_zp=20,20,20
          h1_entries_x=ROOT.TH1D("entries_alongx","entries_alongx",self.npixels,0,self.npixels)
          h1_entries_y=ROOT.TH1D("entries_alongy","entries_alongy",self.npixels,0,self.npixels)
          h1_entries_z=ROOT.TH1D("entries_alongz","entries_alongz",self.npixels,0,self.npixels)
          h1_constant_x=ROOT.TH1D("constant_alongx","constant_alongx",self.npixels,0,self.npixels)
          h1_constant_y=ROOT.TH1D("constant_alongy","constant_alongy",self.npixels,0,self.npixels)
          h1_constant_z=ROOT.TH1D("constant_alongz","constant_alongz",self.npixels,0,self.npixels)
          h2_temp=ROOT.TH2D("temp_h2","temp_h2",self.nbins,-16,16,self.nbins,-16,16)
          for _i in range(self.npixels):
             _image_point_z,_image_point_y,_image_point_x=np.zeros((self.nbins,self.nbins),dtype=float), np.zeros((self.nbins,self.nbins),dtype=float), np.zeros((self.nbins,self.nbins),dtype=float)
             # srf (should be same with matrix)
             image_var_z, image_var_x, image_var_y = self.srf(_xp,_yp,_i,"bintype"), self.srf(_i,_yp,_zp,"bintype"), self.srf(_xp,_i,_zp,"bintype")
             h_gaus_z, h_gaus_y, h_gaus_x = ROOT.TF2("h_gaus_z","bigaus",-16,16,-16,16), ROOT.TF2("h_gaus_y","bigaus",-16,16,-16,16), ROOT.TF2("h_gaus_x","bigaus",-16,16,-16,16)
             h_gaus_x.SetParameters(image_var_x[0],image_var_x[1],image_var_x[2],image_var_x[3],image_var_x[4],image_var_x[5])
             h_gaus_y.SetParameters(image_var_y[0],image_var_y[1],image_var_y[2],image_var_y[3],image_var_y[4],image_var_y[5])
             h_gaus_z.SetParameters(image_var_z[0],image_var_z[1],image_var_z[2],image_var_z[3],image_var_z[4],image_var_z[5])
             for imx in range(128):
                for imy in range(128):
                   _x=h2_temp.GetXaxis().GetBinCenter(imx+1)
                   _y=h2_temp.GetYaxis().GetBinCenter(imy+1)
                   if h_gaus_x.Eval(_x,_y) > 0.1: _image_point_x[imx][imy]=h_gaus_x.Eval(_x,_y)
                   if h_gaus_y.Eval(_x,_y) > 0.1: _image_point_y[imx][imy]=h_gaus_y.Eval(_x,_y)
                   if h_gaus_z.Eval(_x,_y) > 0.1: _image_point_z[imx][imy]=h_gaus_z.Eval(_x,_y)
             _weightx=np.sum(_image_point_x)  
             _weighty=np.sum(_image_point_y)
             _weightz=np.sum(_image_point_z)  
             h1_entries_x.Fill(_i,_weightx)
             h1_entries_y.Fill(_i,_weighty)
             h1_entries_z.Fill(_i,_weightz)
             h1_constant_x.Fill(_i,image_var_x[0])
             h1_constant_y.Fill(_i,image_var_y[0])
             h1_constant_z.Fill(_i,image_var_z[0])
          image_hx_hy_list_matrix.append(hori_entries_x)             
          image_hx_hy_list_matrix.append(hori_entries_y)             
          image_hx_hy_list_matrix.append(hori_entries_z)             
          image_hx_hy_list_matrix.append(h1_entries_x)             
          image_hx_hy_list_matrix.append(h1_entries_y)             
          image_hx_hy_list_matrix.append(h1_entries_z)             
          image_hx_hy_list_matrix.append(h1_constant_x)             
          image_hx_hy_list_matrix.append(h1_constant_y)             
          image_hx_hy_list_matrix.append(h1_constant_z)             
          if prog: prog.finalize()
          return image_hx_hy_list_ori, image_hx_hy_list_sr, image_hx_hy_list_matrix, [h_delta_constant,h_delta_mux,h_delta_sigmax,h_delta_muy,h_delta_sigmay,h_delta_rho]

      def mkInitImageLoop(self):
          # return initial image from object
          prog = ProgressBar(ntotal=pow(self.npixels,3),text="Processing init. image",init_t=time.time())
          _image_init=ROOT.TH2D("image_init_loop","image_init_loop",self.nbins,-16,16,self.nbins,-16,16)
          _image_init_array=np.zeros((self.nbins,self.nbins),dtype=float)         
          nevproc=0
          for index in range(pow(self.npixels,3)):
             nevproc+=1
             if prog: prog.update(nevproc)
             imagespace_vars=self.ob2im_dic[index]
             fgaus = ROOT.TF2("fgaus","bigaus",-16,16,-16,16)
             fgaus.SetParameters(imagespace_vars[0],imagespace_vars[1],imagespace_vars[2],imagespace_vars[3],imagespace_vars[4],imagespace_vars[5])
             for ix in range(128):
                for iy in range(128):
                   _x=_image_init.GetXaxis().GetBinCenter(ix+1)
                   _y=_image_init.GetYaxis().GetBinCenter(iy+1)
                   _image_init_array[ix][iy]+=fgaus.Eval(_x,_y)
             del fgaus
          if prog: prog.finalize()
          array2hist(_image_init_array,_image_init)
          return _image_init

      def mkInitObject(self):
          log().info("Processing guess object...")
          _object_init=np.ones((self.npixels,self.npixels,self.npixels),dtype=float)
          _object_init=_object_init*self.source_intensity
          #_image_init=ROOT.TH2D("image_init","image_init",self.nbins,-16,16,self.nbins,-16,16)
          #_image_array=np.zeros((self.nbins,self.nbins),dtype=float)
          #for imx in range(self.nbins):
          #   for imy in range(self.nbins):
          #      _image_array[imx][imy]=np.sum(_object_init*self.matrix[:,:,:,imx,imy])
          #_where_0 = np.where(_image_array < 1)
          #_image_array[_where_0] = 1 # skip divide 0 problem
          #array2hist(_image_array,_image_init)
          return _object_init          

      def getindex(self,_angle): # need to be fixed before appliaction
          # === coordinate rotation ===
          x = np.arange(self.npixels)-self.npixels/2 # set -npixels to npixels and centered at 0 => rotate along 0
          y, z = x.copy(), x.copy()
          X, Z, Y = np.meshgrid(x, y, z) # make xyz-axis npixels*npixels*npixels matrix
          
          Yrot = Y*np.cos(_angle)-Z*np.sin(_angle)
          Zrot = Y*np.sin(_angle) + Z*np.cos(_angle)
          XCor = np.round(X+self.npixels/2)
          YrotCor = np.round(Yrot+self.npixels/2) # shift back to original image coordinates for checking over size, round values to make indices
          ZrotCor = np.round(Zrot+self.npixels/2) # shift back to original image coordinates for checking over size, round values to make indices
          XCor, YrotCor, ZrotCor = XCor.astype('int'), YrotCor.astype('int'), ZrotCor.astype('int')
          x0, x1, x2 = np.where((XCor >= 0) & (XCor <= (self.npixels-1)))
          y0, y1, y2 = np.where((YrotCor >= 0) & (YrotCor <= (self.npixels-1)))
          z0, z1, z2 = np.where((ZrotCor >= 0) & (ZrotCor <= (self.npixels-1)))
          ix,iy,iz=XCor[x0, x1, x2],YrotCor[y0, y1, y2],ZrotCor[z0, z1, z2]
          return [y0, y1, y2] # x0?y0?z0?

      def updateImage(self,_object):
          # === rotate matrix to make the images at the different angles ===
          _image_update=np.zeros((self.nbins,self.nbins),dtype=float)
          for imx in range(self.nbins):
             for imy in range(self.nbins):
                _image_update[imx][imy]=np.sum(self.matrix[:,:,:,imx,imy]*_object)
          # TODO
          # cut for region
          for c in range(24):
             _image_update[c]=0# left
             _image_update[127-c]=0 # right
             _image_update[:,c]=0# bottom
             _image_update[:,127-c]=0 # upper
          # cut for value
          n_top=5
          _image_sort=np.reshape(_image_update,_image_update.shape[0]*_image_update.shape[1])
          _image_index=np.argpartition(_image_sort, -n_top)[-n_top:]
          maxvalue=np.sum(_image_sort[_image_index])/n_top # get max.
          #maxvalue=np.max(_image_update)# get max.
          where_bins=np.where(_image_update < maxvalue*0.1)
          _image_update[where_bins]=0
          return _image_update

      def findratio(self,measurement_image_array,reproduction_image_array):
          # === input/output type: numpy.array ===
          image_ratio=np.zeros((self.nbins,self.nbins),dtype=float)
          _where_thre = np.where(reproduction_image_array > 0.0001)# skip divide 0 problem (sys.float_info.min or 0.01 for threshold)
          image_ratio[_where_thre]=measurement_image_array[_where_thre]/reproduction_image_array[_where_thre] # get ratio
          return image_ratio

      def updateObject(self,object_pre,image_ratio):
          # === update object with ratio, and then rotate the updated object for each angles ===
          object_ratio=np.zeros((self.npixels,self.npixels,self.npixels),dtype=float)
          for ix in range(self.npixels):
             for iy in range(self.npixels):
                for iz in range(self.npixels):
                   object_ratio[ix][iy][iz]=np.sum(image_ratio*self.matrix[ix][iy][iz])/np.sum(self.matrix[ix][iy][iz])
          _object_update=object_pre*object_ratio
          return object_ratio, _object_update

      def rotObject(self,_object,_angle):
          # === rotate object for next iteration ===
          #_object_mov=np.zeros((self.npixels,self.npixels,self.npixels),dtype=float)
          #for i in range(self.npixels-_mov):
          #   _object_mov[i+_mov]=_object[i]
          #object_update_rot=ndimage.rotate(_object_mov,_angle,axes=(0,2),reshape=False)
          #object_movupdate=np.zeros((self.npixels,self.npixels,self.npixels),dtype=float)
          #for i in range(self.npixels-_mov):
          #   object_movupdate[i]=object_update_rot[i+_mov]
          #return object_movupdate
          return ndimage.rotate(_object,_angle,axes=(0,2),reshape=False)
          
      def iterate(self,n_iteration):                   
          prog = ProgressBar(ntotal=n_iteration*len(self.h_measurement_list),text="Processing iteration",init_t=time.time())
          nevproc, n_savehist=0, 20
          hist_final_object=ROOT.TH3D("MLEM_3Dimage","MLEM_3Dimage",self.npixels,-20,20,self.npixels,-20,20,self.npixels,-20,20)
          hist_final_object.GetXaxis().SetTitle("X"); hist_final_object.GetYaxis().SetTitle("Y"); hist_final_object.GetZaxis().SetTitle("Z");

          h_angle=(-1)*360/len(self.h_measurement_list)
          for i in range(n_iteration):
             if i == 0: _object = self.object_init# unit guess object
             for _ih in range(len(self.h_measurement_list)):
                nevproc+=1
                if prog: prog.update(nevproc)
                h_measurement_array=self.h_measurement_list[_ih]
                #h_angle=self.h_angle_list[_ih]
                h_name=self.h_name_list[_ih]
                #h_index=self.getindex(h_angle)
                # === main parts ===
                _image=self.updateImage(_object)# make 2D image corresponding to angle from object
                _image_ratio=self.findratio(h_measurement_array, _image)# find ratio with data
                _object_ratio,_object=self.updateObject(_object, _image_ratio)# update object
  
                if i < n_savehist or i >= (n_iteration-3) or n_iteration <= 15:# only check n_savehist plots and last two iterations
                   hist_object_ratio=ROOT.TH3D("Ratio_object_{0}_iteration{1}".format(h_name,i),"object_ratio_{0}_iteration{1}".format(h_name,i),self.npixels,-20,20,self.npixels,-20,20,self.npixels,-20,20)
                   hist_image_ratio=ROOT.TH2D("Ratio_image_{0}_iteration{1}".format(h_name,i),"image_ratio_{0}_iteration{1}".format(h_name,i),self.nbins,-16,16,self.nbins,-16,16)
                   hist_process_object=ROOT.TH3D("MLEM_3Dimage_{0}_iteration{1}".format(h_name,i),"MLEM_3Dimage_{0}_iteration{1}".format(h_name,i),self.npixels,-20,20,self.npixels,-20,20,self.npixels,-20,20)
                   hist_process_image=ROOT.TH2D("MLEM_2Dimage_{0}_iteration{1}".format(h_name,i),"MLEM_2Dimage_{0}_iteration{1}".format(h_name,i),self.nbins,-16,16,self.nbins,-16,16)
                   hist_object_ratio.SetStats(0); hist_image_ratio.SetStats(0); hist_process_object.SetStats(0); hist_process_image.SetStats(0);
                   array2hist(_object,hist_process_object)
                   array2hist(_object_ratio,hist_object_ratio)
                   array2hist(_image,hist_process_image)
                   array2hist(_image_ratio,hist_image_ratio)
                   self.mlemratio_list.append(hist_image_ratio)
                   self.mlemratio_list.append(hist_object_ratio)
                   self.mlemhist_list.append(hist_process_image)
                   self.mlemhist_list.append(hist_process_object)
                   self.mlemhist_proje_list.append(hist_process_image.ProjectionX())
                   self.mlemhist_proje_list.append(hist_process_image.ProjectionY())
                   self.mlemhist_proje_list.append(hist_process_object.ProjectionX())
                   self.mlemhist_proje_list.append(hist_process_object.ProjectionY())
                   self.mlemhist_proje_list.append(hist_process_object.ProjectionZ())
                _object=self.rotObject(_object,h_angle)# rotate object for next iteration

          _object=self.rotObject(_object,(-1)*h_angle)# return for the last object
          if prog: prog.finalize()
          log().info("Processing array to histogram...")
          final_object=_object
          #final_object=np.zeros((self.npixels,self.npixels,self.npixels),dtype=float)
          #w_0=np.where(_object >=  1) # test cut for 3D plot
          #final_object[w_0]=_object[w_0]
          array2hist(final_object,hist_final_object)
          return hist_final_object

      def printoutput(self,RootType_list, _outname, savetype, subname=None):
          if savetype == "re" or savetype == "RE" or savetype == "Re": _savetype = "recreate"
          if savetype == "up" or savetype == "UP" or savetype == "Up": _savetype = "update"
          fout=ROOT.TFile(_outname, _savetype)
          fout.cd()    
          if subname != None:
             if fout.FindObjectAny(subname): subdir = fout.GetDirectory(subname)
             else: subdir = fout.mkdir(subname)
             subdir.cd()
          if isinstance(RootType_list, list):
             for _iR in RootType_list:
                _iR.Write()
          else:
             RootType_list.Write()
          fout.Close()

def checkmatrix(matrix, n_plots, npixels):
    log().info("Checking Matrix =>")
    check_list,n_angles=[],16
    if n_plots > n_angles: n_plots = n_angles
    fobj=ROOT.TFile("/Users/chiu.i-huan/Desktop/new_scientific/macro/auxfile/ISO3D.root","read")
    hobj=fobj.Get("h3iso")
    hobj=ROOT.TH3D("h3_test","h3_test",npixels,-20,20,npixels,-20,20,npixels,-20,20)
    for i in range(npixels):
       hobj.Fill(2,-5, i-20, 1000) 
       if i >= (npixels*0.75): 
          hobj.Fill(4,-4, i-npixels/2, 1000) 
          hobj.Fill(3,-4, i-npixels/2, 1000) 
          hobj.Fill(4,-6, i-npixels/2, 1000) 
          hobj.Fill(3,-6, i-npixels/2, 1000) 
          hobj.Fill(1,-6, i-npixels/2, 1000) 
    _h_array=hist2array(hobj)
    for i in range(n_angles):
       if i >= n_plots : continue
       log().info("{0}/{1}...".format(i+1,n_plots))
       _angle=(-1)*i*(360/n_angles)
       _image_update=np.zeros((128,128),dtype=float)
       _object_update=np.zeros((npixels,npixels,npixels),dtype=float)
       h2_image=ROOT.TH2D("h2_angle{}".format(i),"h2_angle{}".format(i),128,-16,16,128,-16,16)
       h3_image=ROOT.TH3D("h3_angle{}".format(i),"h3_angle{}".format(i),npixels,-20,20,npixels,-20,20,npixels,-20,20)
       h3_imagere=ROOT.TH3D("h3_angle{}_re".format(i),"h3_angle{}_re".format(i),npixels,-20,20,npixels,-20,20,npixels,-20,20)
       h2_image.SetDirectory(0); h3_image.SetDirectory(0); h3_imagere.SetDirectory(0)
       _object_mov=np.zeros((npixels,npixels,npixels),dtype=float)
       for i in range(34):
          _object_mov[i+6]=_h_array[i]
       h_array=ndimage.rotate(_object_mov,_angle,axes=(0,2),reshape=False)
       for imx in range(128):
          for imy in range(128):
             _image_update[imx][imy]=np.sum(matrix[:,:,:,imx,imy]*h_array)
       for ix in range(npixels):
          for iy in range(npixels):
             for iz in range(npixels):
                _object_update[ix][iy][iz]=np.sum(_image_update*matrix[ix][iy][iz])
#       _object_update=ndimage.rotate(_object_update,(-2)*_angle,axes=(1,2),reshape=False)
       array2hist(_image_update,h2_image); array2hist(h_array,h3_image); array2hist(_object_update,h3_imagere);
       check_list.append(h3_image); check_list.append(h2_image); check_list.append(h3_imagere)
    return check_list

# ======================= test part (old) ===================
def GetImageSpace(filename,npixels,npoints,nbins,mypoint):
    # Object spcae to image spcae (by weighting image)
    my_axis=[]
    index,stepsize=0,10
    for ix in range(npoints):
       for iy in range(npoints):
          for iz in range(npoints):
             my_axis.append([(ix-2)*stepsize, (iy-2)*stepsize, (iz-2)*stepsize])

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
       if (np.sum(((mypoint-my_axis[i])**2)) == 0): mypoint=mypoint+0.00000000001 #skip divide by zero
       weight=1/np.sum(((mypoint-my_axis[i])**2))#Inverse square distance
       sumw+=weight
       weight_list.append(weight)# use this weight_list to find image for mypoint
    for i in range(pow(npoints,3)):
       # find corresponding image from the giving object space
       myimageA+=imagearray_list[i]*(weight_list[i]/sumw)
    return myimageA

def mkWeightFunc(filename,_np):
    n_images=pow(_np,3)
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

# ======================= run ===================
def main_run(args):

    _n_iteration=args.loopiteration
    outfilename = "/Users/chiu.i-huan/Desktop/new_scientific/run/root/MLEM_output/myMLEMoutput_"+args.output+"_iteration"+str(_n_iteration)
    outfilename = outfilename+".root"
    image_nbins=128 # number of strips of CdTe detector

    # Load matrix (read number of pixel from matrix)
    _matrix=None
    if args.matrix: 
       log().info("Loading Matrix...")
       with open(args.matrix, 'rb') as f:
          _matrix=np.load(f)
       _npixels = _matrix.shape[0]
    else:
       _npixels=args.npixels
    if args.matrix:
       check_list=checkmatrix(_matrix,5,_npixels)#check matrix with guess object
    else: check_list=[]

    # Load module
    PP=PrepareParameters(filename=args.inputFolder,npoints=args.npoints,stepsize=args.stepsize,npixels=_npixels,nbins=image_nbins) # get cali. image list
    SR=SystemResponse(fittype=args.matrix)# get system response by TMinuit fitting
    ML=MLEM(PPclass=PP,SRclass=SR,npoints=args.npoints,nbins=image_nbins,npixels=_npixels,matrix=_matrix,imageinput=args.imageinput) # do iterate and get final plots

    # MLEM iteration
    MLEM_3DHist=ML.iterate(n_iteration=_n_iteration)

    # Store tree and plots
    log().info("Print outputs...")
    ML.printoutput(ML.mlemtree,outfilename,"re")

    ML.printoutput(ML.image_hx_hy_list_ori,outfilename,"up","fitting")
    ML.printoutput(ML.image_hx_hy_list_sr,outfilename,"up","fitting")
    ML.printoutput(ML.image_hx_hy_list_matrix,outfilename,"up","fitting")
    ML.printoutput(ML.hist_delta_mu,outfilename,"up","fitting")
    ML.printoutput(ML.h_data_list,outfilename,"up","measurement")
    ML.printoutput(check_list,outfilename,"up","checkmatrix")
    ML.printoutput(ML.mlemhist_proje_list,outfilename,"up","MLEMprojection")

    ML.printoutput(ML.mlemratio_list,outfilename,"up")
#    ML.printoutput(ML.image_init,outfilename,"up")
    ML.printoutput(ML.mlemhist_list,outfilename,"up")
    ML.printoutput(MLEM_3DHist,outfilename,"up")

    log().info("Output : %s"%(outfilename))
    exit(0)

    #old backup
    #_sr=mkWeightFunc(args.inputFolder, args.npoints)
    #testimage = GetImageSpace(args.inputFolder,image_nbins,5,image_nbins,np.array([0,0,0]))

if __name__=="__main__":

   parser = argparse.ArgumentParser(description='Process some integers.')
   parser.add_argument("-i","--inputFolder", type=str, default="/Users/chiu.i-huan/Desktop/new_scientific/run/root/20200406a_5to27_cali_caldatat_0828_split.root", help="Input File Name for system response")
   parser.add_argument("--imageinput", type=str, default="/Users/chiu.i-huan/Desktop/new_scientific/run/figs/repro_3Dimage.CdTe_LP_0909.root", help="Input File Name for 3D image")
   parser.add_argument("-o", "--output", type=str, default="sr_outputname", help="Additional Output File Name")
   parser.add_argument("-m", "--matrix", type=str, default=None, help="System response database")
   parser.add_argument("-n","--npoints",dest="npoints",type=int, default=5, help="Number of points in each axis")
   parser.add_argument("-s","--stepsize",dest="stepsize",type=int, default=10, help="step size of points")
   parser.add_argument("-p","--npixels",dest="npixels",type=int, default=40, help="Number of pixels for object space")
   parser.add_argument("-l","--loopiteration",dest="loopiteration",type=int, default=3, help="Number of iterations")
   args = parser.parse_args()

   main_run(args)

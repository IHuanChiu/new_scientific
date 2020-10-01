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

gROOT.ProcessLine(
"struct MLEMStruct {\
   Double_t  mlemx;\
   Double_t  mlemy;\
};"
);

from ROOT import MLEMStruct
mlstruct = MLEMStruct()
paramater_list,point_axis=[],[]

# ======================= find the paramaters by fitting ===================
class PrepareParameters():
      def __init__(self,filename=None,npoints=None,stepsize=None,npixels=None,nbins=None):
          self.filename=filename
          self.npoints=npoints
          self.stepsize=stepsize
          self.npixels=npixels
          self.nbins=nbins
          self.imagearray = self.getimages()
          self.par_list, self.hist_fit = self.fitting_para()

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
          #paramater: Constant, MeanX, SigmaX, MeanY, SigmaY, Rho
          return ROOT.TF2(name,myfunction,_xdown,_xup,_ydown,_yup)

      def fitting_para(self):
          global paramater_list
          paramater_list,hist_fitlist=[], []
          xcenter = [15.5,7.5,0,-7.5,-15]
          ycenter = [15.5,7.5,0,-7.5,-15]
          fit_range=10
          index, constant, xup, xdown, yup, ydown, rho=0,0,0,0,0,0,0
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
                   # TODO bad fitting channels
                   if index == 1: paramater_list.append([1.74254e+02,8.10055e+00,1.72548e+00,1.50197e+01,1.49098e+00,-9.93072e-02]) 
                   elif index == 26: paramater_list.append([1.95446e+02,7.34044e+00,1.82564e+00,1.40217e+01,1.73770e+00,2.42294e-02])
                   elif index == 81: paramater_list.append([1.49021e+02,6.13308e+00,1.74712e+00,5.69160e+00,1.85554e+00,-1.01725e-01])
                   elif index == 100: paramater_list.append([1.18486e+02,1.12588e+01,1.95410e+00,1.05471e+01,1.80264e+00,-8.80853e-02])
                   elif index == 110: paramater_list.append([1.41792e+02,1.09893e+01,1.89663e+00,-2.30509e-01,1.95740e+00,9.20033e-02])
                   elif index == 122: paramater_list.append([1.25659e+02,1.06397e-01,1.69141e+00,-1.10063e+01,1.94154e+00,5.99720e-02])
                   else:
                      Chi2=999999999
                      for fittime in range(5):
                         h2.Fit("gb"+str(index),"QR")
                         if Chi2 > gb.GetChisquare():
                            Chi2=gb.GetChisquare()
                            constant, mean_x, sigma_x, mean_y, sigma_y, rho = gb.GetParameter(0), gb.GetParameter(1), gb.GetParameter(2), gb.GetParameter(3), gb.GetParameter(4), gb.GetParameter(5)
                      paramater_list.append([constant, mean_x, sigma_x, mean_y, sigma_y, rho])                  
                   hist_fitlist.append(h2)
                   # Cheching bad fitting channels
                   if paramater_list[index][0] > 1000: 
                      log().warn("bad fitting point : {0}, {1}".format(index, paramater_list[index]))

                   index+=1
                   del gb,h2
          return paramater_list, hist_fitlist

# ======================= fit with TMinuit for the varaibles of function ===================
def deffunc(_x,_y,_z,par):         
    func=par[0]+par[1]*_x+par[2]*_y+par[3]*_z
    return func
def fcn_constant(npar, gin, f, par, iflag):
    chisq, npoints = 0., 5
    for _index in range(pow(npoints,3)):
       chisq += pow((paramater_list[_index][0] - deffunc(point_axis[_index][0],point_axis[_index][1],point_axis[_index][2],par)),2)
    f[0] = chisq
def fcn_x(npar, gin, f, par, iflag):
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
      def __init__(self):
          self.par_con_x_xsig_y_ysig_rho = self.GetSRpar()

      def dofit(self, parname):
          if parname == "constant": fcn = fcn_constant
          if parname == "x": fcn = fcn_x
          if parname == "xsig": fcn = fcn_xsig
          if parname == "y": fcn = fcn_y
          if parname == "ysig": fcn = fcn_ysig
          if parname == "rho": fcn = fcn_rho
          gMinuit = TMinuit(4)
          gMinuit.SetPrintLevel(-1) # -1  quiet, 0  normal, 1  verbose
          gMinuit.SetFCN( fcn )
          arglist = array( 'd', 10*[0.] )
          ierflg = ctypes.c_int(1982)
      
          arglist[0] = 1
          gMinuit.mnexcm( "SET ERR", arglist, 1, ierflg )
      
          # Set starting values and step sizes for parameters
          vstart = array( 'd', ( 3,  1,  0.1,  0.01  ) )
          step   = array( 'd', ( 0.1, 0.1, 0.01, 0.001 ) )
          gMinuit.mnparm( 0, "par0", vstart[0], step[0], 0, 0, ierflg )
          gMinuit.mnparm( 1, "parx", vstart[1], step[1], 0, 0, ierflg )
          gMinuit.mnparm( 2, "pary", vstart[2], step[2], 0, 0, ierflg )
          gMinuit.mnparm( 3, "parz", vstart[3], step[3], 0, 0, ierflg )
      
          # Now ready for minimization step
          arglist[0] = 500
          arglist[1] = 1.
          gMinuit.mnexcm( "MIGRAD", arglist, 2, ierflg )
      
          # Print results
          par0,par1,par2,par3 = map(ctypes.c_double, (0,0,0,0))
          par0_err,par1_err,par2_err,par3_err = map(ctypes.c_double, (0,0,0,0))
          amin, edm, errdef = map(ctypes.c_double, (0.18, 0.19, 0.20))
          nvpar, nparx, icstat = map(ctypes.c_int, (1983, 1984, 1985))
          gMinuit.mnstat( amin, edm, errdef, nvpar, nparx, icstat )
          gMinuit.GetParameter(0,par0,par0_err)
          gMinuit.GetParameter(1,par1,par0_err)
          gMinuit.GetParameter(2,par2,par0_err)
          gMinuit.GetParameter(3,par3,par0_err)
          return [par0,par1,par2,par3]

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
      def __init__(self,PPclass=None,SRclass=None,npoints=None,nbins=None,npixels=None,matrix=None):
          # class members
          self.PP=PPclass
          self.SR=SRclass
          # setup varaibles
          self.nbins=nbins
          self.npoints=npoints
          self.npixels=npixels
          self.object_range=20 #mm
          # parametor members
          self.hist_fit=self.PP.hist_fit
          self.para_dic=self.SR.par_con_x_xsig_y_ysig_rho
          self.ori_image_list=self.PP.imagearray
          self.ob2im_dic=self.mksrfdic()
          if not isinstance(matrix, np.ndarray): self.matrix=self.mkmatrix()
          else: self.matrix=matrix
          # plots
          self.image_hx_hy_list_ori, self.image_hx_hy_list_sr=self.mkimage()
          self.mlemtree=self.mktree()
#          self.image_init_loop=self.mkInitImageLoop()
          self.object_init,self.image_init=self.mkInitImage()
          self.h_measurement_list=self.getmeasurement()
          self.mlemhist_list=[]

      def getmeasurement(self):
          # return array type
          _mlist=[]
          #fint=ROOT.TFile("/Users/chiu.i-huan/Desktop/new_scientific/run/figs/repro_3Dimage.CdTe_LP_0909.root","read")
          #n_angles=1
          #for i in range(n_angles):
          #   _name = "h"+str(i)
          #   _mlist.append(hist2array(fint.Get(_name)))          
          fint=ROOT.TFile("/Users/chiu.i-huan/Desktop/new_scientific/run/root/20200406a_5to27_cali_caldatat_0828_split.root","read")
          _mlist.append(hist2array(fint.Get("image_pos43")))
          return _mlist

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
          image_constant = par_constant[0].value+par_constant[1].value*_x+par_constant[2].value*_y+par_constant[3].value*_z
          image_x = par_x[0].value+par_x[1].value*_x+par_x[2].value*_y+par_x[3].value*_z
          image_xsig = par_xsig[0].value+par_xsig[1].value*_x+par_xsig[2].value*_y+par_xsig[3].value*_z
          image_y = par_y[0].value+par_y[1].value*_x+par_y[2].value*_y+par_y[3].value*_z
          image_ysig = par_ysig[0].value+par_ysig[1].value*_x+par_ysig[2].value*_y+par_ysig[3].value*_z
          image_rho = par_rho[0].value+par_rho[1].value*_x+par_rho[2].value*_y+par_rho[3].value*_z
          return [image_constant,image_x,image_xsig,image_y,image_ysig,image_rho]

      def mksrfdic(self):
          srfdic={}
          _index=0
          for x in range(self.npixels):
             for y in range(self.npixels):
                for z in range(self.npixels):
                   srfdic.update({_index:self.srf(x,y,z,"bintype")})
                   _index+=1
          return srfdic

      def mkmatrix(self):
          prog = ProgressBar(ntotal=pow(self.npixels,3),text="Processing Matrix",init_t=time.time())
          source_intensity = 363.1*1000 #Bq
          matrix=np.ones((self.npixels,self.npixels,self.npixels,self.nbins,self.nbins),dtype=float)          
          index=0
          nevproc=0
          for iz in range(self.npixels):
             for iy in range(self.npixels):
                for ix in range(self.npixels):
                   nevproc+=1
                   if prog: prog.update(nevproc)
                   image_var = self.ob2im_dic[index]
                   h_gaus = ROOT.TF2("h_gaus","bigaus",-16,16,-16,16)
                   h_gaus.SetParameters(image_var[0],image_var[1],image_var[2],image_var[3],image_var[4],image_var[5])

                   matrix[ix][iy][iz]=0.
                   for imageix in range(self.nbins):
                      for imageiy in range(self.nbins):
                         _imagex=-16+0.125+imageix*(32./self.nbins)
                         _imagey=-16+0.125+imageiy*(32./self.nbins)
                         matrix[ix][iy][iz][imageix][imageiy]=(h_gaus.Eval(_imagex,_imagey)/source_intensity)
                   index+=1
          if prog: prog.finalize()
          with open('matrix_temp.npy', 'wb') as f:
             np.save(f, matrix)
          return matrix

      def mktree(self):
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
          # make original vs. system response comparison plots
          image_hx_hy_list_sr, image_hx_hy_list_ori=[],[]
          _ip=0
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
                   # original plots
                   _h2name="image_ori_"+str(_ip)             
                   _h2=ROOT.TH2F(_h2name,_h2name,self.nbins,-16,16,self.nbins,-16,16) 
                   array2hist(self.ori_image_list[_ip],_h2)
                   image_hx_hy_list_ori.append(_h2)
                   image_hx_hy_list_ori.append(_h2.ProjectionX())
                   image_hx_hy_list_ori.append(_h2.ProjectionY())

                   # system response plots
                   image_var = self.srf(point_axis[_ip][0], point_axis[_ip][1], point_axis[_ip][2])
                   _h2name="image_sr_"+str(_ip)
                   h2=ROOT.TH2D(_h2name,_h2name,self.nbins,-16,16,self.nbins,-16,16)
                   h2_array=np.zeros((self.nbins,self.nbins),dtype=float)
                   h_gaus = ROOT.TF2("h_gaus","bigaus",-16,16,-16,16)
                   h_gaus.SetParameters(image_var[0],image_var[1],image_var[2],image_var[3],image_var[4],image_var[5])
                   for ix in range(128):
                      for iy in range(128):
                         _x=h2.GetXaxis().GetBinCenter(ix+1)
                         _y=h2.GetYaxis().GetBinCenter(iy+1)
                         if h_gaus.Eval(_x,_y) > 1: h2_array[ix][iy]=h_gaus.Eval(_x,_y)
                   array2hist(h2_array,h2)
                   hx = h2.ProjectionX()
                   hy = h2.ProjectionY()
                   image_hx_hy_list_sr.append(h2)
                   image_hx_hy_list_sr.append(h2.ProjectionX())
                   image_hx_hy_list_sr.append(h2.ProjectionY())            

                   # comparison canvas fitting result
                   _cvfit.cd((_ix+1)+_iy*self.npoints)
                   h2.SetStats(0)
                   h2.Draw("colz")
                   _cvori.cd((_ix+1)+_iy*self.npoints)
                   _h2.SetStats(0)
                   _h2.Draw("colz")
                   # original fitting plots
                   #self.hist_fit[_ip].SetMaximum(350)
                   #self.hist_fit[_ip].SetStats(0)
                   #self.hist_fit[_ip].Draw()
                   # comparison canvas MLEM result
                   hx_ori=_h2.ProjectionX()
                   hy_ori=_h2.ProjectionY()
                   hx_ori.SetStats(0)
                   hy_ori.SetStats(0)
                   hx_ori.SetLineColor(1)
                   hy_ori.SetLineColor(1)
                   hx.SetStats(0)
                   hy.SetStats(0)
                   hx.SetLineColor(2)
                   hy.SetLineColor(2)
                   hx_ori.SetMaximum(350)
                   hy_ori.SetMaximum(350)
                   hx.SetMaximum(350)
                   hy.SetMaximum(350)
                   _cvx.cd((_ix+1)+_iy*self.npoints) 
                   hx_ori.Draw()
                   hx.Draw("hist same")
                   _cvy.cd((_iy+1)+_ix*self.npoints) 
                   hy_ori.Draw()
                   hy.Draw("hist same")
                   del _h2, h2, hx, hy, h_gaus
                   _ip+=1 

             _pdfname = "/Users/chiu.i-huan/Desktop/new_scientific/run/figs/MLEM_comparison_x_z{}.pdf".format(_iz)
             _cvx.SaveAs(_pdfname)
             _pdfname = _pdfname.replace("_x_","_y_")
             _cvy.SaveAs(_pdfname)
             _pdfname = _pdfname.replace("_y_","_ori_")
             _cvori.SaveAs(_pdfname)
             _pdfname = _pdfname.replace("_ori_","_fit_")
             _cvfit.SaveAs(_pdfname)
          return image_hx_hy_list_ori, image_hx_hy_list_sr

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

      def mkInitImage(self):
          source_intensity = 363.1*1000 #Bq
          _object_init=np.ones((self.npixels,self.npixels,self.npixels),dtype=float)
          _object_init=_object_init*source_intensity

          _image_init=ROOT.TH2D("image_init","image_init",self.nbins,-16,16,self.nbins,-16,16)
          _image_array=np.zeros((self.nbins,self.nbins),dtype=float)
          for imx in range(self.nbins):
             for imy in range(self.nbins):
                _image_array[imx][imy]=np.sum(_object_init*self.matrix[:,:,:,imx,imy])
          array2hist(_image_array,_image_init)
          return _object_init, _image_init          

      def updateImage(self,_object):
          _image_update=np.zeros((self.nbins,self.nbins),dtype=float)
          for imx in range(self.nbins):
             for imy in range(self.nbins):
                _image_update[imx][imy]=np.sum(_object*self.matrix[:,:,:,imx,imy])
          return _image_update

      def findratio(self,measurement_image_array,reproduction_image_array):
          # input/output type: numpy.array
          _where_0 = np.where(reproduction_image_array == 0)
          reproduction_image_array[_where_0]=0.00001
          image_ratio=measurement_image_array/reproduction_image_array
          return image_ratio

      def updateObject(self,object_pre,image_ratio):
          # update object based on object ratio
          object_ratio=np.zeros((self.npixels,self.npixels,self.npixels),dtype=float)
          for ix in range(self.npixels):
             for iy in range(self.npixels):
                for iz in range(self.npixels):
#                   object_ratio[ix][iy][iz]=np.sum(image_ratio*self.matrix[ix][iy][iz])
                   #TODO over matrix?
                   object_ratio[ix][iy][iz]=np.sum(image_ratio*self.matrix[ix][iy][iz])/np.sum(self.matrix[ix][iy][iz])
          object_update=object_pre*object_ratio
          return object_ratio, object_update

      def iterate(self,n_iteration):                   
          prog = ProgressBar(ntotal=n_iteration*len(self.h_measurement_list),text="Processing iterate",init_t=time.time())
          hist_final_object=ROOT.TH3D("MLEM_3Dimage","MLEM_3Dimage",self.npixels,-20,20,self.npixels,-20,20,self.npixels,-20,20)
          hist_final_object.GetXaxis().SetTitle("Z")
          hist_final_object.GetYaxis().SetTitle("Y")
          hist_final_object.GetZaxis().SetTitle("X")
          final_object=np.zeros((self.npixels,self.npixels,self.npixels),dtype=float)
          nevproc, ih, n_savehist=0, 0, 5
          for h_measurement_array in self.h_measurement_list:
             for i in range(n_iteration):
                nevproc+=1
                if prog: prog.update(nevproc)
                if i == 0: 
                   _image=hist2array(self.image_init)
                   _object=self.object_init
                _image_ratio=self.findratio(h_measurement_array, _image) 
                _object_ratio,_object=self.updateObject(_object, _image_ratio)
                _image = self.updateImage(_object)

                if ih < n_savehist:# only check n_savehist plots
                   hist_object_ratio=ROOT.TH3D("object_ratio_h{0}_iteration{1}".format(ih,i),"object_ratio_h{0}_iteration{1}".format(ih,i),self.npixels,-20,20,self.npixels,-20,20,self.npixels,-20,20)
                   hist_image_ratio=ROOT.TH2D("image_ratio_h{0}_iteration{1}".format(ih,i),"image_ratio_h{0}_iteration{1}".format(ih,i),self.nbins,-16,16,self.nbins,-16,16)
                   hist_process_image=ROOT.TH2D("image_h{0}_iteration{1}".format(ih,i),"image_ratio_h{0}_iteration{1}".format(ih,i),self.nbins,-16,16,self.nbins,-16,16)
                   array2hist(_object_ratio,hist_object_ratio)
                   array2hist(_image_ratio,hist_image_ratio)
                   array2hist(_image,hist_process_image)
                   self.mlemhist_list.append(hist_image_ratio)
                   self.mlemhist_list.append(hist_object_ratio)
                   self.mlemhist_list.append(hist_process_image)
             final_object+=_object# projeaction of all images
             ih+=1
          if prog: prog.finalize()
          # TODO test cut & make 3D plot
          w_0=np.where(final_object <  1)
          final_object[w_0]=0
          array2hist(final_object,hist_final_object)
          return hist_final_object

      def printoutput(self,RootType_list, _outname, savetype):
          if savetype == "re" or savetype == "RE" or savetype == "Re": _savetype = "recreate"
          if savetype == "up" or savetype == "UP" or savetype == "Up": _savetype = "update"
          fout=ROOT.TFile(_outname, _savetype)
          fout.cd()    
          if isinstance(RootType_list, list):
             for _iR in RootType_list:
                _iR.Write()
          else:
             RootType_list.Write()
          fout.Close()

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
def testrun(args):
    log().info("Loading Matrix...")

    outfilename = "/Users/chiu.i-huan/Desktop/mytesth3output_"+args.output
    outfilename = outfilename+".root"
    image_nbins=128 # number of strips of CdTe detector
    _matrix=None
    if args.matrix: 
       with open(args.matrix, 'rb') as f:
          _matrix=np.load(f)
       args.npixels = _matrix.shape[0]
    _sr=mkWeightFunc(args.inputFolder, args.npoints)
    testimage = GetImageSpace(args.inputFolder,image_nbins,5,image_nbins,np.array([0,0,0]))

    log().info("Progressing the paramaters for fitting ...")
    PP=PrepareParameters(filename=args.inputFolder,npoints=args.npoints,stepsize=args.stepsize,npixels=args.npixels,nbins=image_nbins) # get cali. image list
    SR=SystemResponse()# get system response by TMinuit fitting
    ML=MLEM(PPclass=PP,SRclass=SR,npoints=args.npoints,nbins=image_nbins,npixels=args.npixels,matrix=_matrix) # do iterate and get final plots

    # MLEM iteration
    MLEM_3DHist=ML.iterate(n_iteration=5)

    #check plots
    log().info("Print outputs...")
    ML.printoutput(ML.mlemtree,outfilename,"re")
    ML.printoutput(ML.image_hx_hy_list_ori,outfilename,"up")
    ML.printoutput(ML.image_hx_hy_list_sr,outfilename,"up")
    ML.printoutput(ML.image_init,outfilename,"up")
    ML.printoutput(ML.mlemhist_list,outfilename,"up")
    ML.printoutput(MLEM_3DHist,outfilename,"up")

    log().info("Output : %s"%(outfilename))
    exit(0)

if __name__=="__main__":

   parser = argparse.ArgumentParser(description='Process some integers.')
   parser.add_argument("-i","--inputFolder", type=str, default="/Users/chiu.i-huan/Desktop/new_scientific/run/root/20200406a_5to27_cali_caldatat_0828_split.root", help="Input File Name")
   parser.add_argument("-o", "--output", type=str, default="sr_outputname", help="Output File Name")
   parser.add_argument("-m", "--matrix", type=str, default=None, help="Output File Name")
   parser.add_argument("-n","--npoints",dest="npoints",type=int, default=5, help="Number of images")
   parser.add_argument("-s","--stepsize",dest="stepsize",type=int, default=10, help="Number of images")
   parser.add_argument("-p","--npixels",dest="npixels",type=int, default=10, help="Number of images")
   args = parser.parse_args()

   testrun(args)

import sys,os,ROOT,time
sys.path.append('/Users/chiu.i-huan/Desktop/new_scientific/imageAna/macro/utils/')
sys.path.append('/Users/chiu.i-huan/Desktop/new_scientific/imageAna/macro/')
from ROOT import gSystem, gPad, gDirectory, gStyle
from helpers import createRatioCanvas, ProgressBar
from logger import log
from root_numpy import hist2array, array2hist, tree2array
import numpy as np
import vtk
from vtk.util import numpy_support
ROOT.gErrorIgnoreLevel = ROOT.kWarning
__location__ = os.path.realpath(
        os.path.join(os.getcwd(), os.path.dirname(__file__)))

inputfile="/Users/chiu.i-huan/Desktop/new_scientific/imageAna/run/root/MLEM_output/myMLEMoutput_30MeV_iteration100.root"
plotname="MLEM_3Dimage_h15_iteration14"

if __name__=="__main__":
   f_mlem=ROOT.TFile(inputfile,"read")
   h3=f_mlem.Get(plotname)
   matrix=hist2array(h3)
   with open('mlem_3Dplot.npy', 'wb') as f:
      np.save(f, matrix)
   VTK_data = numpy_support.numpy_to_vtk(num_array=matrix.ravel(), deep=True, array_type=vtk.VTK_FLOAT)
   # save vtk data
   sphere = vtk.vtkSphereSource()
   sphere.SetRadius(4)
   sphere.SetCenter(0,0,1)
   sphere.Update()
#   writer = vtk.vtkPolyDataWriter()
   writer = vtk.vtkUnstructuredGridWriter()
   writer.SetFileName("mlem_3Dplot.vtk")
   writer.SetInputData(VTK_data)
   #writer.SetInputData(sphere.GetOutput())
   writer.Update()
   writer.Write()

      
log().info("output npy file: {}".format("mlem_3Dplot.npy"))
log().info("output vtk file: {}".format("mlem_3Dplot.vtk"))

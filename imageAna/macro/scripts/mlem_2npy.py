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
import itkwidgets
ROOT.gErrorIgnoreLevel = ROOT.kWarning
__location__ = os.path.realpath(
        os.path.join(os.getcwd(), os.path.dirname(__file__)))

inputfile="/Users/chiu.i-huan/Desktop/new_scientific/imageAna/run/root/MLEM_output/myMLEMoutput_30MeV_iteration100.root"
#plotname="MLEM_3Dimage_h15_iteration14"
plotname="MLEM_2Dimage_h15_iteration14"

if __name__=="__main__":
   f_mlem=ROOT.TFile(inputfile,"read")
   h3=f_mlem.Get(plotname)
   matrix=hist2array(h3)
   with open('3Dplot_mlem.npy', 'wb') as f:
      np.save(f, matrix)
   VTK_data = numpy_support.numpy_to_vtk(num_array=matrix.ravel(), deep=True, array_type=vtk.VTK_FLOAT)
#   VTK_data = numpy_support.numpy_to_vtk(num_array=matrix.ravel())

   # to polydata
   polydata = vtk.vtkPolyData()
   polydata.GetPointData().AddArray(VTK_data)
   # to table
   tab = vtk.vtkTable()
   tab.GetRowData().AddArray(VTK_data)
   # example : sphere
   sphere = vtk.vtkSphereSource()
   sphere.SetRadius(4)
   sphere.SetCenter(0,0,1)
   sphere.Update()
#   print(sphere.GetOutput())

#   Filename = 'file.vtk'
#   reader = vtk.vtkUnstructuredGridReader()
#   reader.SetFileName(Filename)
#   reader.ReadAllScalarsOn()
#   reader.ReadAllVectorsOn()
#   pa = vtk.vtkPassArrays()
#   pa.SetInputConnection(reader.GetOutputPort())
#   pa.AddArray( 0, 'Array1Name' ) # 0 for PointData, 1 for CellData, 2 for FieldData
#   writer = vtk.vtkDataSetWriter()
#   writer.SetFileName('3Dplot_mlem.vtk')
#   writer.SetInputConnection(pa.GetOutputPort())
#   writer.Update()
#   writer.Write()
#

   writer = vtk.vtkPolyDataWriter()
   writer.SetFileName("3Dplot_mlem.vtk")
   writer.SetInputData(polydata)
   writer.Update()
   writer.Write()

      
log().info("output npy file: {}".format("3Dplot_mlem.npy"))
log().info("output vtk file: {}".format("3Dplot_mlem.vtk"))

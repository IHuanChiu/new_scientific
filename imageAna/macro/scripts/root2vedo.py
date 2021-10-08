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
from vedo import *
from vedo.applications import IsosurfaceBrowser
from vedo.applications import SlicerPlotter
ROOT.gErrorIgnoreLevel = ROOT.kWarning
__location__ = os.path.realpath(
        os.path.join(os.getcwd(), os.path.dirname(__file__)))

#inputfile="/Users/chiu.i-huan/Desktop/new_scientific/imageAna/run/root/MLEM_output/myMLEMoutput_30MeV_iteration100.root"
#plotname="MLEM_3Dimage_h15_iteration14"

inputfile="/Users/chiu.i-huan/Desktop/new_scientific/imageAna/run/root/MLEM_output/myMLEMoutput_30MeV_osem_forpaper_iteration5.root"
plotname="MLEM_3Dimage"

#inputfile="/Users/chiu.i-huan/Desktop/edb2root/test_rannor.root"
#plotname="h3"

if __name__=="__main__":
   f_mlem=ROOT.TFile(inputfile,"read")
   h3=f_mlem.Get(plotname)
   matrix=hist2array(h3)
   with open('3Dplot_mlem.npy', 'wb') as f:
      np.save(f, matrix)

   # === only for 2D image ===
#   VTK_data = numpy_support.numpy_to_vtk(num_array=matrix.ravel(), deep=True, array_type=vtk.VTK_FLOAT)
   # to polydata
#   polydata = vtk.vtkPolyData()
#   polydata.GetPointData().AddArray(VTK_data)
#   # to table
#   tab = vtk.vtkTable()
#   tab.GetRowData().AddArray(VTK_data)
#   # example : sphere
#   sphere = vtk.vtkSphereSource()
#   sphere.SetRadius(4)
#   sphere.SetCenter(0,0,1)
#   sphere.Update()
##   print(sphere.GetOutput())
#   writer = vtk.vtkPolyDataWriter()
#   writer.SetFileName("3Dplot_mlem.vtk")
#   writer.SetInputData(polydata)
#   writer.Update()
#   writer.Write()

   # === for 3D image ===
   dataImporter = vtk.vtkImageImport()#make vtkImageImport
   arrBytes = matrix.tobytes()# numpy 2 bytes
   dataImporter.CopyImportVoidPointer(arrBytes, len(arrBytes))
   dataImporter.SetDataScalarTypeToUnsignedChar()
   dataImporter.SetNumberOfScalarComponents(1)
   dataImporter.SetWholeExtent(0, 74, 0, 74, 0, 74)
   dataImporter.SetDataExtentToWholeExtent()
   dataImporter.SetDataSpacing(1.0, 1.0, 2.0)
   dataImporter.SetDataOrigin(0, 350, 0)
   dataImporter.Update()
#   vtkImage = dataImporter.GetOutput()
#   itkwidgets.view(vtkImage)
#   if os.path.isfile("./3Dplot_mlem.vtk"):
#      os.system("rm ./3Dplot_mlem.vtk")
#   writer = vtk.vtkNIFTIImageWriter()
#   writer.SetFileName("3Dplot_mlem.vtk")
#   writer.SetInputData(vtkImage)
#   writer.Update()
#   writer.Write()

   # === VEDO ===
   vol = Volume(matrix, c=['white','b','g','r'])
   vol.addScalarBar3D()
   plt = IsosurfaceBrowser(vol, c='gold') # Plotter instance
   thresholds = [0.1, 0.25, 0.4, 0.6, 0.75, 0.9]
   isos = Volume(matrix).isosurface(thresholds)
#   volvtk = Volume(dataImporter)
#   pltvtk = SlicerPlotter( vol,bg='white', bg2='lightblue',cmaps=("gist_ncar_r","jet","Spectral_r","hot_r","bone_r"),useSlider3D=False,)
  
   #show(vol, __doc__, axes=1).close()
   #plt.show(axes=7, bg2='lb').close()
   #show(isos, __doc__, axes=1, interactive=False).addCutterTool(isos)
   #pltvtk.show().close()

   vol = Volume(matrix).alpha([0.0, 0.0, 0.2, 0.6/2, 0.8/2, 1.0/2]).c('lightblue')
   slices = []
   for i in range(5):
       sl = vol.slicePlane(origin=[i*5+10,10,10], normal=(1,0,0))
       slices.append(sl)
   amap = [0, 1, 1, 1, 1]  # hide low value points giving them alpha 0
   mslices = merge(slices) # merge all slices into a single Mesh
#   mslices.cmap('hot_r', alpha=amap).lighting('off').addScalarBar3D(title='Slice', c='w')
   mslices.cmap('hot_r', alpha=amap).lighting('off').addScalarBar(title='Slice', c='w')
   show(vol, mslices, __doc__, axes=1)
#   plt=show(vol, mslices, __doc__, axes=1,viewup='z',mode=9,interactive=False)#no interactive
#   dolfin.screenshot(filename="/Users/chiu.i-huan/Desktop/vedo3Dplot.png")

      
#log().info("output npy file: {}".format("3Dplot_mlem.npy"))
#log().info("output vtk file: {}".format("3Dplot_mlem.vtk"))

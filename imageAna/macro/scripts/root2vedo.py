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
from scipy import ndimage, misc
ROOT.gErrorIgnoreLevel = ROOT.kWarning
__location__ = os.path.realpath(
        os.path.join(os.getcwd(), os.path.dirname(__file__)))

#x:y plots
#inputfile="/Users/chiu.i-huan/Desktop/new_scientific/imageAna/run/root/MLEM_output/myMLEMoutput_30MeV_iteration100.root"
#plotname="MLEM_3Dimage_h15_iteration14"

#inputfile="/Users/chiu.i-huan/Desktop/new_scientific/imageAna/run/root/MLEM_output/myMLEMoutput_30MeV_ImageCut_w_rot12_forpaper_iteration15.root"
#inputfile="/Users/chiu.i-huan/Desktop/new_scientific/imageAna/run/root/MLEM_output/myMLEMoutput_30MeV_ImageCut_w_rot12_noX_osem_forpaper_iteration10.root"
#inputfile="/Users/chiu.i-huan/Desktop/new_scientific/imageAna/run/root/MLEM_output/myMLEMoutput_30MeV_forpaper_iteration5.root"
#inputfile="/Users/chiu.i-huan/Desktop/new_scientific/imageAna/run/root/MLEM_output/myMLEMoutput_30MeV_1014_forpaper_iteration15.root"#new rotation
#inputfile="/Users/chiu.i-huan/Desktop/new_scientific/imageAna/run/root/MLEM_output/myMLEMoutput_30MeV_1014_rotation_cutR_forpaper_iteration15.root"#new rotation
#inputfile="/Users/chiu.i-huan/Desktop/new_scientific/imageAna/run/root/MLEM_output/myMLEMoutput_30MeV_ImageCut_w_rot12_noX_forpaper_iteration15.root"
#inputfile="/Users/chiu.i-huan/Desktop/new_scientific/imageAna/run/root/MLEM_output/myMLEMoutput_30MeV_rotation_cutR_forpaper_iteration5.root"
#inputfile="/Users/chiu.i-huan/Desktop/new_scientific/imageAna/run/root/MLEM_output/myMLEMoutput_30MeV_cutR_forpaper_iteration15.root"
#inputfile="/Users/chiu.i-huan/Desktop/new_scientific/imageAna/run/root/MLEM_output/myMLEMoutput_30MeV_cutR3_osem_forpaper_iteration15.root"
#inputfile="/Users/chiu.i-huan/Desktop/new_scientific/imageAna/run/root/MLEM_output/myMLEMoutput_30MeV_cutR3_dropIM_osem_forpaper_iteration5.root"
#inputfile="/Users/chiu.i-huan/Desktop/new_scientific/imageAna/run/root/MLEM_output/myMLEMoutput_30MeV_dropIM_osem_forpaper_iteration5.root"
#inputfile="/Users/chiu.i-huan/Desktop/new_scientific/imageAna/run/root/MLEM_output/myMLEMoutput_30MeV_mlem_forpaper_iteration15.root"

#TODO here
#inputfile="/Users/chiu.i-huan/Desktop/new_scientific/imageAna/run/root/MLEM_output/myMLEMoutput_30MeV_mlem_forpaper_iteration150.root"
#inputfile="/Users/chiu.i-huan/Desktop/new_scientific/imageAna/run/root/MLEM_output/myMLEMoutput_30MeV_osem_forpaper_iteration150.root"
#plotname="MLEM_3Dimage_iteration2"
inputfile="/Users/chiu.i-huan/Desktop/new_scientific/imageAna/run/root/MLEM_output/myMLEMoutput_30MeV_noRcut_mlem_forpaper_iteration50.root"
#inputfile="/Users/chiu.i-huan/Desktop/new_scientific/imageAna/run/root/MLEM_output/myMLEMoutput_30MeV_noRcut_osem_forpaper_iteration50.root"

# === with bug ===
#inputfile="/Users/chiu.i-huan/Desktop/new_scientific/imageAna/run/root/MLEM_output/myMLEMoutput_30MeV_ImageCut_w_forpaper_iteration50.root"
#mlem
#inputfile="/Users/chiu.i-huan/Desktop/new_scientific/imageAna/run/root/MLEM_output/myMLEMoutput_30MeV_no14keV_iteration15.root"
#inputfile="/Users/chiu.i-huan/Desktop/new_scientific/imageAna/run/root/MLEM_output/myMLEMoutput_30MeV_ImageCut_forpaper_iteration5.root"#noweight
#inputfile="/Users/chiu.i-huan/Desktop/new_scientific/imageAna/run/root/MLEM_output/myMLEMoutput_30MeV_ImageCut_forpaper_iteration15.root"#noweight
#inputfile="/Users/chiu.i-huan/Desktop/new_scientific/imageAna/run/root/MLEM_output/myMLEMoutput_30MeV_forpaper_iteration50.root"#noweight
#inputfile="/Users/chiu.i-huan/Desktop/new_scientific/imageAna/run/root/MLEM_output/myMLEMoutput_30MeV_noweight_forpaper_iteration5.root"
#inputfile="/Users/chiu.i-huan/Desktop/new_scientific/imageAna/run/root/MLEM_output/myMLEMoutput_30MeV_forpaper_iteration5.root"
#inputfile="/Users/chiu.i-huan/Desktop/new_scientific/imageAna/run/root/MLEM_output/myMLEMoutput_30MeV_forpaper_iteration15.root"
plotname="MLEM_3Dimage_iteration40"

#osem
#inputfile="/Users/chiu.i-huan/Desktop/new_scientific/imageAna/run/root/MLEM_output/myMLEMoutput_30MeV_osem_no14keV_iteration15.root"
#inputfile="/Users/chiu.i-huan/Desktop/new_scientific/imageAna/run/root/MLEM_output/myMLEMoutput_30MeV_osem_forpaper_iteration5.root"
#inputfile="/Users/chiu.i-huan/Desktop/new_scientific/imageAna/run/root/MLEM_output/myMLEMoutput_30MeV_noweight_osem_forpaper_iteration5.root"
#inputfile="/Users/chiu.i-huan/Desktop/new_scientific/imageAna/run/root/MLEM_output/myMLEMoutput_30MeV_ImageCut_osem_forpaper_iteration5.root"#noweight
#inputfile="/Users/chiu.i-huan/Desktop/new_scientific/imageAna/run/root/MLEM_output/myMLEMoutput_30MeV_osem_forpaper_iteration15.root"
#plotname="MLEM_3Dimage_set3_iteration10"

#plotname="MLEM_3Dimage"

if __name__=="__main__":
   f_mlem=ROOT.TFile(inputfile,"read")
   h3=f_mlem.Get(plotname)
   matrix=hist2array(h3)
   with open('3Dplot_mlem.npy', 'wb') as f:
      np.save(f, matrix)

#   with open("/Users/chiu.i-huan/Desktop/new_scientific/imageAna/macro/scripts/Sample_4sphere.npy", 'rb') as f:
#      sample_matrix=np.load(f)

   # === Rotation ===
   _angle=65
   matrix=ndimage.rotate(matrix,_angle,axes=(1,2),reshape=False)   

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
   init_X=20
   init_Y=20
   init_Z=11
   diff_Big=4
   shift_small=0.2
   poi_big1  =(init_X+7.07,init_Y+7.07,init_Z+12.7-diff_Big)
   poi_big2  =(init_X-7.07,init_Y-7.07,init_Z)
   poi_small1=(init_X+7.07,init_Y-7.07,init_Z+6.35-diff_Big+6.35-6.35/2)
   poi_small2=(init_X-7.07,init_Y+7.07,init_Z+12.7+6.35-diff_Big-6.35/2)
   s1 = Sphere(c="white",pos=poi_big1, r=12.7/2,alpha=0.5, res=12).wireframe()
   s2 = Sphere(c="white",pos=poi_big2, r=12.7/2,alpha=0.5, res=12).wireframe()
   s3 = Sphere(c="white",pos=poi_small1, r=12.7/4,alpha=0.5, res=12).wireframe()
   s4 = Sphere(c="white",pos=poi_small2, r=12.7/4,alpha=0.5, res=12).wireframe()

#   vol_sample=Volume(sample_matrix).isosurface(thresholds_sample)
#   vol_sample.addScalarBar3D()
   #plt_sample = IsosurfaceBrowser(vol_sample, c='k')
#   show(vol_sample, __doc__, axes=1).close()

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

   vol = Volume(matrix).alpha([0.0, 0.0, 0.3, 0.6, 0.8, 1.0]).c('lightblue')
   slices = []
   for i in range(5):
       sl = vol.slicePlane(origin=[i*5+10,10,10], normal=(1,0,0))
       slices.append(sl)
   amap = [0, 1, 1, 1, 1]  # hide low value points giving them alpha 0
   mslices = merge(slices) # merge all slices into a single Mesh
   mslices.cmap('hot_r', alpha=amap).lighting('off').addScalarBar(title='Slice', c='w')
   # == check ==
#   show(s1,s2,s3,s4,vol,mslices,  __doc__, axes=1)

   # == paper plot ==
   #plt=show(s1,s2,s3,s4, vol, mslices, __doc__, axes=1,viewup='y',mode=9,interactive=False)#no interactive
   #dolfin.screenshot(filename="/Users/chiu.i-huan/Desktop/vedo3Dplot.png")

   # == video ==
   #cam = dict(pos=(4.14, -4.25, 2.35),
   #        focalPoint=(0.167, -0.287, 0.400),
   #        viewup=(-0.230, 0.235, 0.944),
   #        distance=5.94)
   #plt=show(s1,s2,s3,s4,vol,mslices,  __doc__, axes=1, camera=cam, interactive=False)
   #for i in range(200):
   #   plt.camera.Azimuth(-0.2)
   #   vol.rotateZ(3.6)
   #   s1.rotateZ(3.6)
   #   s2.rotateZ(3.6)
   #   s3.rotateZ(3.6)
   #   s4.rotateZ(3.6)
   #   mslices.rotateZ(3.6)
   #interactive().close()

   # == video 2 ==
   #settings.screeshotScale = 2
   plt = Plotter(axes=1, offscreen=True)
   #plt = Plotter(axes=1, interactive=False)
   video = Video("video_rot.mp4", duration=6,backend='opencv')
   for i in range(200):
      plt.camera.Azimuth(-2)
      plt.show(s1,s2,s3,s4,vol,mslices)
      video.addFrame()
   video.close()
#   plt.close()
      
#log().info("output npy file: {}".format("3Dplot_mlem.npy"))
#log().info("output vtk file: {}".format("3Dplot_mlem.vtk"))

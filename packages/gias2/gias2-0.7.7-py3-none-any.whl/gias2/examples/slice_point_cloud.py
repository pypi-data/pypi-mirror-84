import numpy as np
from gias2.common import geoprimitives
from gias2.image_analysis.image_tools import Scan
from gias2.mesh import vtktools

mesh = vtktools.loadpoly('data/autoCarpal1_outer.stl')

# make a plane to cut the mesh
mesh_com = mesh.v.mean(0)
plane_o = mesh_com
plane_normal = np.array([0, 0, 1])
plane_x = np.array([1, 0, 0])
plane_y = np.array([0, 1, 0])
slice_plane = geoprimitives.Plane(
    mesh_com, plane_normal, x=plane_x, y=plane_y
)

near_dist = 2.0
sliced_pts = slice_plane.near_points(mesh.v, near_dist)

# turn mesh into a 3D image array
#
# NOTE the mesh should be near the origin in the +x, +y, quadrant for it
# to be in the generated image.
#
# create a dummy image array that ranges from origin to the most distant
# corner of the mesh + 10 mm
dummy_image = np.array(mesh.v.max(0).astype(int) + 10)
dummy_scan = Scan('dummy_scan')
dummy_scan.setImageArray(dummy_image, i2cmat=np.eye(4), c2imat=np.eye(4))
mesh_image_arr = vtktools.simplemesh2BinaryMask(
    mesh, dummy_scan, False, False,
    outputOrigin=[0.0, 0.0, 0.0],
    outputSpacing=[1.0, 1.0, 1.0]
)
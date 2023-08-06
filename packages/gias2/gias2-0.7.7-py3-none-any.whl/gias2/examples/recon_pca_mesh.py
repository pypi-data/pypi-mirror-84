from gias2.learning.PCA import loadPrincipalComponents
from gias2.mesh.vtktools import loadpoly, savepoly

pc_filename = 'example.npz'  # the principal components npz file
mean_mesh_filename = 'mean_bone.stl'  # the mean mesh STL or PLY file
recon_mesh_filename = 'recon_bone.stl'  # output STL or PLY
recon_weights = [0, 0, 0]  # weights to reconstruct with, get from PLSR
recon_modes = [0, 1, 2]  # PC modes to reconstruct with, should be same length as above

# load principal components
pc = loadPrincipalComponents(pc_filename)

# reconstruct vertex coordinates
recon_1d = pc.reconstruct(recon_weights, recon_modes)
recon_3d = recon_1d.reshape([-1, 3])

# put reconstructed vertices into a mesh object
recon_mesh = loadpoly(mean_mesh_filename)
recon_mesh.v = recon_3d

# write out reconstructed mesh
savepoly(recon_mesh, recon_mesh_filename)

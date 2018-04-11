import numpy as np

pointcloud = np.loadtxt('Chiffon/adquisicionInfra_Mant.out')
color  = np.loadtxt('Chiffon/adquisicionColorInfra_Mant.out')
color = (np.delete(color, 3, 1)*255).astype(int)
mesh3d = np.concatenate((pointcloud, color), axis=1).astype(int)
np.savetxt("Mesh.asc", mesh3d, fmt='%1.4e')
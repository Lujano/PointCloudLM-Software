import numpy as np

pointcloud = np.loadtxt('Chiffon/adquisicionUltra_Mant.out')
color  = np.loadtxt('Chiffon/adquisicionColorUltra_Mant.out')
color = (np.delete(color, 3, 1)*255).astype(int)
mesh3d = np.concatenate((pointcloud, color), axis=1).astype(int)
np.savetxt("Mesh_UltraXYZRGB.txt", mesh3d, fmt='%1.4e')
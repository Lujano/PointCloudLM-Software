import numpy as np



# Datos de motores calibrados
phi_180 = 228
phi_0 = 36
phi_resol = (phi_180 - phi_0 + 1) / 180.0
phi_step = 1.0 # un paso
ni_phi = int(round((phi_180-phi_0+1)/phi_step)) # numero de angulos phi


theta_90 = 245
theta_0 = 131
theta_min = 100  # minimo angulo sin que el motor choque con la base
theta_resol = (theta_90 - theta_0 + 1) / 90.0
theta_step = 1.0 # un paso
ni_theta = int(round((theta_90-theta_0+1)/theta_step)) # numero de angulos theta

# Ajuste de indices para la creacion de la matriz de datos
n_medidas = 1
data = np.zeros((ni_phi, ni_theta, n_medidas))  # matriz de datos
phi = 37
theta = 132
phi_index = int(round((phi-phi_0)/phi_step))
theta_index = int(round((theta -theta_0)/theta_step))

###
###

# Convertir data a nube de puntos
data_reshape = np.zeros([0, 3])
for phi in range(data.shape[0]):
    for theta in range(data.shape[1]):
        r = data[phi, theta, 0]
        theta_prima = theta * np.pi / 180.0
        phi_prima = phi * np.pi / 180.0
        x = r * np.sin(theta_prima) * np.cos(phi_prima)
        y = r * np.sin(theta_prima) * np.sin(phi_prima)
        z = r * np.cos(theta_prima)
        data = np.append(data_reshape, [[x, y, z]], 0)












import numpy as np

# fc=(10.0**6)/10.0
# L = 22.0*10**-6
# C = 10.0*10**-6
# rc = 0.5
# R = 0.4545
# w = 2*np.pi*fc

#Leo
# fc=(50*10**3)/10
# L = 361.25*(10**-6)
# C = 100*(10**-6)
# rc = 0.5
# R =0.555
# w = 2*np.pi*fc

#Kheyter
# fc=(100*10**3)/10
# L = 10*(10**-6)
# C = 200*(10**-6)
# rc = 0.5
# R =0.555
# w = 2*np.pi*fc

#Ray
fc=(35*10**3)/10
L = 65*(10**-6)
C = 200*(10**-6)
rc = 0.5
R = 5
w = 2*np.pi*fc
fase1 = np.arctan2(w*C*rc, 1)
fase2 = np.arctan2((w*( (1.0/(R*C))+rc/L) ), 1/(L*C)-(w**2)*(1+rc/R))

Num =np.sqrt(1+(w*rc*C)**2)
Den =np.sqrt((1.0-(w**2)*L*C*(1.0+rc/R))**2 + (w*(L/R+rc*C))**2)

Den2 =1.0/(L*C)*np.sqrt((1.0/(L*C)-(w**2)*(1.0+rc/R))**2 + (w*(1.0/(R*C)+rc/L))**2)

G = Num/Den
fase = fase1-fase2
fase_grados = fase*180/np.pi

K = np.tan((45-fase_grados)*np.pi/(180*2))

GdB=20*np.log10(G)
print("La fase es {}".format(fase_grados))
print("La ganancia del sist no compensado en dB es: "+str(GdB))

print("k es {}".format(K))
print(G)
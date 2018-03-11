import numpy as np

# fc=(10**6)/10
# L = 22*10**-6
# C = 10**-6
# rc = 0.5
# R = 0.4545
# w = 2*np.pi*fc

fc=(10**5)/10
L = 100*(10**-6)
C = 100*(10**-6)
rc = 0.5
R =5
w = 2*np.pi*fc


fase1 = np.arctan2(w*C*rc, 1)
fase2 = np.arctan2(w*( 1/(R*C+rc/L) ), 1/(L*C)-(w**2)*(1+rc/R))

Num =np.sqrt(1+(w*rc*C)**2)
Den =np.sqrt((1.0-(w**2)*L*C*(1+rc/R))**2 + (w*(L/R+rc*C))**2)

G = Num/Den*2
fase = fase1-fase2
fase_grados = fase*180/np.pi


k = np.tan(((45-fase_grados)*np.pi/180)/2)

print("La ganancia es: "+str(G))
print

print(fase_grados)
print("k es {}".format(k))
GdB=20*np.log10(G)
print("La ganancia del sist no compensado en dB es: "+str(GdB))
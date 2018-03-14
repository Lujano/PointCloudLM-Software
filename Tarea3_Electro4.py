# Luis Lujano, 13-10775
# Tarea 3, Electro 4
import numpy as np
import matplotlib.pyplot as plt
import scipy.optimize


#Datos de entrada
A = 5
B = 7
L = (100+10*B)*10**-3
R = 500+100*A
f = 60
w = 2*np.pi*f
phi = np.arctan(w*L/R)
z_mod =np.sqrt((w*L)**2+R**2)

"""Pregunta 1, Potencia maxima"""
print("Modulo de la impedancia = {}".format(z_mod))
Vrms  = 220
Smax = Vrms**2/z_mod
Pmax = Smax*np.cos(phi)
print("Smax = {}, Pmax ={}, phi = {}".format(Smax, Pmax, phi*180/np.pi))

"""Pregunta 2, Potencia Promedio para alpha = 85"""
alpha = np.radians(85) # Angulo de retardo
#Calculo del angulo de extincion
def f_ext(x):
    return np.sin(x-phi)-np.sin(alpha-phi)*np.exp((-1/np.tan(phi))*(x-alpha))
angles_posibles = np.arange(85, 185, 0.01)

x = scipy.optimize.ridder( f_ext, np.radians(86.0) , np.radians(190.0)) # Calculo del x de la ecuacion no lineal
print("Angulo de extincion = {}" .format(np.degrees(x)))
# Grafica de la corriente
plt.plot(angles_posibles, f_ext(np.radians(angles_posibles)))
plt.title("Corriente vs x")
# Potencia Promedio para alpha = 85
P = Vrms**2/(2*np.pi*z_mod)*(
                np.sin(2 * alpha - phi) - np.sin(2 * x - phi) + np.cos(phi) * (2 * x - 2 * alpha)
                + 4 * np.sin(phi) * np.sin(alpha - phi) * (
                        np.sin(phi + x) * np.exp((-1 / np.tan(phi)) * (x - alpha)) - np.sin(phi + alpha)))
print("Potencia Promedio = {}, alpha={}".format(P, np.degrees(alpha)))


"""Pregunta 3, 4 y 5"""
# Analisis de Fourier de la corriente en la carga
def coeff_f(n):

    if n == 0:
        return 0
    elif n == 1:
        ai1 = np.sqrt(2) * Vrms / (2 * np.pi * z_mod) * (
                np.cos(2 * alpha - phi) - np.cos(2 * x - phi) - np.sin(phi) * (2 * x - 2 * alpha)
                + 4 * np.sin(phi) * np.sin(alpha - phi) * (
                        np.cos(phi + x) * np.exp((-1 / np.tan(phi)) * (x - alpha)) - np.cos(phi + alpha)))
        bi1 = np.sqrt(2) * Vrms / (2 * np.pi * z_mod) * (
                np.sin(2 * alpha - phi) - np.sin(2 * x - phi) - np.cos(phi) * (2 * x - 2 * alpha)
                + 4 * np.sin(phi) * np.sin(alpha - phi) * (
                        np.sin(phi + x) * np.exp((-1 / np.tan(phi)) * (x - alpha)) - np.sin(phi + alpha)))
        ci1 = np.sqrt(ai1 ** 2 + bi1 ** 2)
        phi_i1 = np.arctan2(ai1, bi1)

        return ci1, ai1, bi1, phi_i1
    else:
        ain = np.sqrt(2) * Vrms / (2 * np.pi * z_mod) * (
                2.0 / (n + 1.0) * (np.cos((n + 1) * alpha - phi) - np.cos((n + 1) * x - phi))
                - 2.0 / (n - 1) * (np.cos((n - 1) * alpha - phi) - np.cos((n - 1) * x - phi))
                + 4 * np.sin(alpha - phi) / (n ** 2 + 1 / (np.tan(phi)) ** 2) * (
                        (1 / np.tan(phi) * np.cos(n * x) - n * np.sin(n * x)) * np.exp((-1 / np.tan(phi)) * (x - alpha))
                        -(1 / np.tan(phi) * np.cos(n * alpha) - n * np.sin(n * alpha))
                )
        )

        bin = np.sqrt(2) * Vrms / (2 * np.pi * z_mod) * (
                2 / (n + 1) * (np.sin((n + 1) * alpha - phi) - np.sin((n + 1) * x - phi))
                - 2 / (n - 1) * (np.sin((n - 1) * alpha - phi) - np.sin((n - 1) * x - phi))
                + 4 * np.sin(alpha - phi) / (n ** 2 + 1 / np.tan(phi) ** 2) * (
                        (1 / np.tan(phi) * np.sin(n * x) - n * np.cos(n * x)) * np.exp((-1 / np.tan(phi)) * (x - alpha))
                        - (1 / np.tan(phi) * np.sin(n * alpha) - n * np.cos(n * alpha))))
        cin = np.sqrt(ain ** 2 + bin ** 2)
        phi_in = np.arctan2(ain, bin)
        return cin, ain, bin, phi_in


# Coeficientes de Fouerier corriente rms
I_total = 0
for i in range(0, 30, 1):
    if i%2 !=0:
        c, a, b, angle_c = coeff_f(i)
        print("Corriente coeficiente {} = {}, a = {}, b = {}, angulo = {}".format( i, c, a, b, np.degrees(angle_c)) )
        print("En rms = {}".format(c/np.sqrt(2)))
        I_total = c**2/2+I_total

print("Valor rms total de la corriente = {}".format(np.sqrt(I_total)) )


plt.show()
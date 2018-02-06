import numpy as np
import matplotlib.pyplot as plt
import time




def main():

    i = 0.00
    y = 0.00
    Amplitud_matrix = np.array([])
    Time_matrix = np.array([])
    T_Inicio = time.time()
    T_Final = time.time()
    Dif = T_Final-T_Inicio
    while(Dif < 2.0):

        i += 1
        y = 2*i
        Amplitud_matrix = np.append(Amplitud_matrix, [y])
        Time_matrix = np.append(Time_matrix, [i])
        T_Final = time.time()
        Dif = T_Final - T_Inicio

    plt.plot(Time_matrix, Amplitud_matrix)
    plt.show()

if __name__ == "__main__": main()
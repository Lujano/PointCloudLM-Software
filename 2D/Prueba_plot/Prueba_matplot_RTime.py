import numpy as np
import matplotlib.pyplot as plt
import time




def main():
    plt.ion()
    counter = 0
    i = 0.00
    y = 0.00
    Amplitud_matrix = np.array([])
    Time_matrix = np.array([])
    T_Inicio = time.time()
    T_Final = time.time()
    Dif = T_Final-T_Inicio
    while(True):
        i += 1
        y = 2*i
        Amplitud_matrix = np.append(Amplitud_matrix, [y])
        Time_matrix = np.append(Time_matrix, [i])
        T_Final = time.time()
        Dif = T_Final - T_Inicio
        if Dif > 0.25:
            plt.plot(Time_matrix, Amplitud_matrix)
            plt.pause(0.001)
            plt.cl
            Amplitud_matrix = np.array([])
            Time_matrix = np.array([])
            T_Inicio = time.time()


if __name__ == "__main__": main()
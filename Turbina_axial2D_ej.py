import numpy as np
import matplotlib.pyplot as plt
import math
import sys

import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from tkinter import ttk
from tkinter import Canvas

pi = math.pi

s1_vec = []
s2_vec = []
s3_vec = []

h1_vec = []
h2_vec = []
h3_vec = []

h01_vec = []
h02_vec = []
h03_vec = []


def calculo():
    print('')
    print('Datos de entrada:')
    print('')
    N = int(N_var.get())
    print('Nº de escalonamientos:', N)
    mdot = float(mdot_var.get())
    print('Flujo másico:', mdot, 'kg/s')

    C1_i = float(C1_var.get())
    print('Velocidad de entrada:', C1_i, 'm/s')

    T1_0 = int(T1_var.get())
    print('Temperatura de entrada:', round(T1_0, 2), 'K')
    P1_0 = float(P1_var.get())
    print('Presión a la entrada:', P1_0, 'Pa')

    DeltaProtor = float(DeltaP_var.get())
    print('Caída de presión en el rotor: ', DeltaProtor,
          'Pa')  # Se dejan las variables con float por si en un futuro se desean hacer cambios de unidades; y redondear sería erróneo

    w_dot_T = float(Wdot_var.get())
    print('Potencia desarrollada por la turbina:', w_dot_T, 'W')

    c_p = float(cp_var.get())
    print('Calor específico del gas ideal:', c_p, ' J/(kg*K)')

    gamma = float(gamma_var.get())
    print('Coeficiente gamma de expansión adiabática', gamma)

    P3_0 = float(P3_var.get())
    print('Presión exterior (condiciones ambientales):', P3_0, 'Pa')

    T3_0 = int(T3_var.get())
    print('Temperatura exterior (condiciones ambientales):', T3_0, 'K')

    h1_0 = c_p * T1_0

    for i in range(N):
        if i == 0:
            h1_i = h1_0
            P1_i = P1_0
            T1_i = T1_0

        # Propiedades termodinámicas
        # PUNTO 1
        # ESTATOR La entalpía total se conserva
        h01_i = h1_i + (C1_i ** 2) / 2
        s1_i = CP.PropsSI('S', 'H', h1_i, 'P', P1_i, 'air')

        # ROTOR
        if N == 1:
            P2_i = P3_0 + DeltaProtor
            # PUNTO 2
        T2_i = T1_i * (P2_i / P1_i) ** ((gamma - 1) / gamma)
        h2_i = c_p * T2_i
        # La expansión que se realiza es ideal, adiabática por lo tanto isoentrópica
        s2_i = s1_i
        # En el estator se conserva la entalpía total
        h02_i = h01_i

        C2_i = math.sqrt(2 * (h02_i - h2_i))

        # PUNTO 3
        # El enunciado dice que el diseño de los álabes en el rotor permiten una evolución isentálpica
        T3_i = T2_i

        h3_i = h2_i

        # Trabajo y potencia del escalonamiento

        w_i = w_dot_T / mdot
        h03_i = h01_i - w_i

        # Velocidad de salida
        C3_i = math.sqrt(2 * (h03_i - h3_i))

        T3s_i = T1_i * (P3_0 / P1_i) ** ((gamma - 1) / gamma)
        h3s_i = c_p * T3s_i
        h3ss_i = h3s_i
        h03ss_i = h3ss_i + (C3_i ** 2) / 2
        s3ss_i = s2_i

        P3_i = CP.PropsSI('S', 'H', h3ss_i, 'S', s3ss_i, 'air')
        s3_i = CP.PropsSI('S', 'H', h3_i, 'P', P3_i, 'air')

        # Rendimiento Total a Estático
        eta_T_E = (h01_i - h03_i) / (h01_i - h3ss_i)

        # Rendimiento Total a Total
        eta_TT_i = (h01_i - h03_i) / (h01_i - h03ss_i)

        # Grado de Reacción
        R_1 = (h2_i - h3_i) / (h01_i - h03_i)

        # Guardado de datos en vectores para la representación posterior del diagrama h-s

        s1_vec.append(round(s1_i, 3))
        s2_vec.append(round(s2_i, 3))
        s3_vec.append(round(s3_i, 3))

        h1_vec.append(round(h1_i, 3))
        h2_vec.append(round(h2_i, 3))
        h3_vec.append(round(h3_i, 3))

        h01_vec.append(round(h01_i, 3))
        h02_vec.append(round(h02_i, 3))
        h03_vec.append(round(h03_i, 3))

        if R_1 > 0:
            print('Es una turbina de reacción')
        else:
            print('Es una turbina de acción')

        if i == 0:
            h01_0 = h01_i
            s1_0 = s1_i
            C1_0 = C1_i

        print('')
        print('Resultados de la turbina')
        print('')
        print('Presión a la salida del estator:', P2_i, 'Pa')
        print('Temperatura a la salida del estator:', round(T2_i, 3), 'K')
        print('Velocidad a la salida del estator:', round(C2_i, 3), 'm/s')
        print('Entropía específica h_1:', h1_i, 'J/kg')
        print('Entropía específica total h_01:', h01_0, 'J/kg')
        print('Entropía específica h_2:', round(h2_i, 2), 'J/kg')
        print('Entropía específica total h_02:', h02_i, 'J/kg')
        print('Entropía específica h_3:', round(h3_i, 2), 'J/kg')
        print('Entropía específica total h_03:', h03_i, 'J/kg')

        print('')
        print('Grado de reacción de la turbina:', R_1)
        print('Temperatura a la salida del rotor:', round(T3_i, 3), 'K')
        print('Velocidad a la salida del rotor:', round(C3_i, 3), 'm/s')

        print('Rendimiento total a estático de la turbina:', round(eta_T_E, 3))
        eta_T_total = (h01_0 - h03_i) / (h01_0 - h03ss_i)
        print('Rendimiento total a total de la turbina:', round(eta_T_total, 3))
        print(' ')

        # Diagrama h-s
        vent = plt.figure(figsize=(7, 5))

        diag = tk.Tk()
        diag.title("Diagrama h-s")

        canvas = FigureCanvasTkAgg(vent, master=diag)
        canvas.draw()
        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

        s = np.array([s1_vec, s2_vec, s3_vec, s1_vec, s2_vec, s3_vec])
        h = np.array([h1_vec, h2_vec, h3_vec, h01_vec, h02_vec, h03_vec])

        pos1 = [f'1 E{i + 1}' for i in range(N)]
        for pos1, x, y in zip(pos1, s1_vec, h1_vec):
            plt.annotate(pos1, (x, y), textcoords="offset points", xytext=(5, -5))

        pos2 = [f'2 E{i + 1}' for i in range(N)]
        for pos2, x, y in zip(pos2, s2_vec, h2_vec):
            plt.annotate(pos2, (x, y), textcoords="offset points", xytext=(5, 5))

        pos3 = [f'3 E{i + 1}' for i in range(N)]
        for pos3, x, y in zip(pos3, s3_vec, h3_vec):
            plt.annotate(pos3, (x, y), textcoords="offset points", xytext=(5, 5))

        pos01 = [f'01 E{i + 1}' for i in range(N)]
        for pos01, x, y in zip(pos01, s1_vec, h01_vec):
            plt.annotate(pos01, (x, y), textcoords="offset points", xytext=(5, 5))
        pos02 = [f'02 E{i + 1}' for i in range(N)]
        for pos02, x, y in zip(pos02, s2_vec, h02_vec):
            plt.annotate(pos02, (x, y), textcoords="offset points", xytext=(5, 5))

        pos03 = [f'03 E{i + 1}' for i in range(N)]
        for pos03, x, y in zip(pos03, s3_vec, h03_vec):
            plt.annotate(pos03, (x, y), textcoords="offset points", xytext=(5, -5))

        spvec1 = ([s1_vec, s1_vec])
        hpvec1 = ([h1_vec, h01_vec])
        plt.plot(spvec1, hpvec1, color='red', linestyle='-')
        spvec2 = ([s2_vec, s2_vec])
        hpvec2 = ([h2_vec, h02_vec])
        plt.plot(spvec2, hpvec2, color='red', linestyle='-')
        spvec3 = ([s3_vec, s3_vec])
        hpvec3 = ([h3_vec, h03_vec])
        plt.plot(spvec3, hpvec3, color='blue', linestyle='--')
        spvec4 = ([s1_vec, s2_vec])
        hpvec4 = ([h1_vec, h2_vec])
        plt.plot(spvec4, hpvec4, color='blue')
        spvec5 = ([s1_vec, s2_vec])
        hpvec5 = ([h01_vec, h02_vec])
        plt.plot(spvec5, hpvec5, color='black')
        spvec6 = ([s2_vec, s3_vec])
        hpvec6 = ([h2_vec, h3_vec])
        plt.plot(spvec6, hpvec6, color='blue')
        # spvec7 = ([s2_vec, s3_vec])
        # hpvec7 = ([h02_vec, h03_vec])
        # plt.plot(spvec7, hpvec7, color = 'black')
        plt.xlabel('Entropía específica s (J/(kg*K))')
        plt.ylabel('Entalpía específica h (J/kg)')
        plt.title('Diagrama h-s')

        plt.plot(s, h, '.', color='blue')
        cerrar = tk.Button(diag, text='Cerrar', command=diag.destroy)
        cerrar.pack(side=tk.BOTTOM, pady=10)
        plt.grid(True)

        diag.mainloop()


# Menú emergente principal
menu = tk.Tk()
menu.title("Diseño de turbina axial")
menu.geometry("1000x900")

# Espacio entre columnas
espacio = tk.Label(menu, text="                  ")
espacio.grid(row=0, column=0)

ttk.Separator(menu, orient=tk.HORIZONTAL).grid(row=0, column=0, pady=10)

cabecera_label = tk.Label(menu, text="Software de prediseño de turbinas axiales con álabes 3D:",
                          font=('Arial', 12, 'bold'))
cabecera_label.grid(row=0, column=1, columnspan=3, padx=5, pady=5, sticky='n')

# Número de escalonamientos
N_label = tk.Label(menu, text="Nº de escalonamientos:", font=('Arial', 10, 'bold'))
N_label.grid(row=1, column=1, padx=5, pady=5, sticky='n')
N_var = tk.StringVar()
N_var.set(1)
N_entry = tk.Entry(menu, textvariable=N_var)
N_entry.grid(row=2, column=1, padx=5, pady=5, sticky='n')

# Flujo másico\n",
mdot_label = tk.Label(menu, text="Flujo másico (kg/s):", font=('Arial', 10, 'bold'))
mdot_label.grid(row=3, column=1, padx=5, pady=5, sticky='n')
mdot_var = tk.DoubleVar()
mdot_var.set(0.09)
mdot_entry = tk.Entry(menu, textvariable=mdot_var)
mdot_entry.grid(row=4, column=1, padx=5, pady=5, sticky='n')

# C1 Velocidad de entrada
C1_label = tk.Label(menu, text="Velocidad de entrada (m/s):", font=('Arial', 10, 'bold'))
C1_label.grid(row=5, column=1, padx=5, pady=5, sticky='n')
C1_var = tk.DoubleVar()
C1_var.set(30)
C1_entry = tk.Entry(menu, textvariable=C1_var)
C1_entry.grid(row=6, column=1, padx=5, pady=5, sticky='n')

# T1 Temperatura de entrada
T1_label = tk.Label(menu, text="Temperatura de entrada (K):", font=('Arial', 10, 'bold'))
T1_label.grid(row=7, column=1, padx=5, pady=5, sticky='n')
T1_var = tk.StringVar()
T1_var.set(473)
T1_entry = tk.Entry(menu, textvariable=T1_var)
T1_entry.grid(row=8, column=1, padx=5, pady=5, sticky='n')

# P1 Presión de entrada
P1_label = tk.Label(menu, text="Presión a la entrada (Pa):", font=('Arial', 10, 'bold'))
P1_label.grid(row=9, column=1, padx=5, pady=5, sticky='n')
P1_var = tk.DoubleVar()
P1_var.set(250000)
P1_entry = tk.Entry(menu, textvariable=P1_var)
P1_entry.grid(row=10, column=1, padx=5, pady=5, sticky='n')

# Delta Presión Caída de presión en el rotor
DeltaP_label = tk.Label(menu, text="Caída de presión en el rotor (Pa):", font=('Arial', 10, 'bold'))
DeltaP_label.grid(row=11, column=1, padx=5, pady=5, sticky='n')
DeltaP_var = tk.DoubleVar()
DeltaP_var.set(25000)
DeltaP_entry = tk.Entry(menu, textvariable=DeltaP_var)
DeltaP_entry.grid(row=12, column=1, padx=5, pady=5, sticky='n')

# Potencia desarrollada por la turbina (W)\n",
Wdot_label = tk.Label(menu, text="Potencia desarrollada por la turbina (W):", font=('Arial', 10, 'bold'))
Wdot_label.grid(row=13, column=1, padx=5, pady=5, sticky='n')
Wdot_var = tk.DoubleVar()
Wdot_var.set(7650)
Wdot_entry = tk.Entry(menu, textvariable=Wdot_var)
Wdot_entry.grid(row=14, column=1, padx=5, pady=5, sticky='n')

# Calor específico del gas ideal
cp_label = tk.Label(menu, text="Calor específico del gas ideal (J/(kg*K)):", font=('Arial', 10, 'bold'))
cp_label.grid(row=15, column=1, padx=5, pady=5, sticky='n')
cp_var = tk.DoubleVar()
cp_var.set(1000)
cp_entry = tk.Entry(menu, textvariable=cp_var)
cp_entry.grid(row=16, column=1, padx=5, pady=5, sticky='n')

# Coeficiente gamma de expansión adiabática
gamma_label = tk.Label(menu, text="Coeficiente gamma de expansión adiabática:", font=('Arial', 10, 'bold'))
gamma_label.grid(row=17, column=1, padx=5, pady=5, sticky='n')
gamma_var = tk.DoubleVar()
gamma_var.set(1.4)
gamma_entry = tk.Entry(menu, textvariable=gamma_var)
gamma_entry.grid(row=18, column=1, padx=5, pady=5, sticky='n')

# Presión exterior a la salida (condiciones ambientales)
P3_label = tk.Label(menu, text="Presión exterior (condiciones ambientales) (Pa):", font=('Arial', 10, 'bold'))
P3_label.grid(row=19, column=1, padx=5, pady=5, sticky='n')
P3_var = tk.DoubleVar()
P3_var.set(100000)
P3_entry = tk.Entry(menu, textvariable=P3_var)
P3_entry.grid(row=20, column=1, padx=5, pady=5, sticky='n')

# Temperatura exterior (condiciones ambientales)
T3_label = tk.Label(menu, text="Temperatura exterior (condiciones ambientales) (K):", font=('Arial', 10, 'bold'))
T3_label.grid(row=21, column=1, padx=5, pady=5, sticky='n')
T3_var = tk.StringVar()
T3_var.set(293)
T3_entry = tk.Entry(menu, textvariable=T3_var)
T3_entry.grid(row=22, column=1, padx=5, pady=5, sticky='n')

accept_button = ttk.Button(menu, text="Confirmar", command=calculo)
accept_button.grid(row=23, column=1, padx=5, pady=5)

cierre = tk.Button(menu, text="Cerrar", command=menu.destroy)
cierre.grid(row=24, column=1, padx=5, pady=5)

menu.mainloop()


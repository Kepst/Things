import time as ttime
import numpy as np
import matplotlib.pyplot as plt
import math

print("Starting programm")

t1 = ttime.time()

deltaT = 1  # time interval
tempoTotal = 21600  # 6 hours = 21600 seconds
times = int(tempoTotal/deltaT) + 1  # time intervals utilized
Es = []  # enthalpy list
div = 20  # number of control volumes

Tp = 20  # ºC  starting temperature
Tm = 0  # ºC  melting temperature
H = 333000  # J / kg  latent heat
Ks = 2.2  # W / mK  solid phase conductivity
Cs = 2092  # J / kgK  specif heat of the solid phase
Kl = 0.58  # W / mK  liquid phase conductivity
Cl = 4184  # J / kgK  specif heat of the liquid phase
rho = 1000  # kg / m^3  density
Tinf = -10  # ºC  external temperature

E = (Tp - Tm) * Cl + H  # starting enthalpy
raio = 5/100
deltaR = raio/div  # radius variation
Hconv = 50  # convection coefficient


def gama_s(enthalpy):  # function to generate game and S coefficients
    if enthalpy < 0:
        return Ks/Cs, 0
    elif enthalpy < H:
        return 0, 0
    else:
        return Kl/Cl, -H*Kl/Cl


def make_temps(enthalpy, vol):  # function to make plots with temperature X time with varying radius
    temps_ = []
    if vol >= len(enthalpy[0]):
        vol = len(enthalpy[0]) - 1
    for time_ in enthalpy:
        E_ = time_[vol]
        if E_ < 0:
            t_ = Tm + time_[vol] / Cs
        elif E_ < H:
            t_ = Tm
        else:
            t_ = Tm + (time_[vol] - H) / Cl
        temps_.append(t_)
    return temps_


def make_E(enthalpy, volume):  # function to make plots with enthalpy X time with varying radius
    enthalpies = []
    if volume >= len(enthalpy[0]):
        volume = len(enthalpy[0]) - 1
    for time in enthalpy:
        ental = time[volume]
        enthalpies.append(ental)
    return enthalpies


def make_R(ent):  # function to make plots with temperature X radius with varying times
    temps = []
    for E in ent:
        if E < 0:
            T = Tm + E / Cs
        elif E < H:
            T = Tm
        else:
            T = Tm + (E - H) / Cl
        temps.append(T)
    return temps


Es.append([])
for time in range(div):
    Es[0].append(E)


for time in range(times):
    b = []  # independent terms
    mat = []  # matrix of coeficients

    # first volume
    line = [1] + [-1] + [0]*(div-2)
    b += [[0]]
    mat += [line]

    # interior volumes
    for volume in range(1, div-1):
        r = deltaR*volume + deltaR/2
        GamaI, Si = gama_s(Es[time][volume-1])  # inicia o valor de gama e S para cada volume
        GamaP, Sp = gama_s(Es[time][volume])
        GamaE, Se = gama_s(Es[time][volume+1])

        A = (r / deltaR - 0.5)*GamaI
        B = -r * (2*GamaP/deltaR + rho*deltaR/deltaT)
        C = (r / deltaR + 0.5)*GamaE
        D = (r/deltaR - 0.5)*Si - 2*Sp*r/deltaR + (r/deltaR + 0.5)*Se + rho*r*Es[time-1][volume]*deltaR/deltaT
        line = (volume-1)*[0] + [A, B, C] + [0]*(div-volume-2)

        b += [[-D]]
        mat += [line]

    # boundary volume
    line = [0]*(div - 1)

    E = Es[time][-1]
    if E < 0:
        k = E + Hconv * deltaT * raio * (Tinf - Tm - E / Cs) / (rho * deltaR * (raio-deltaR)/2)
    elif E < H:
        k = E + Hconv * deltaT * raio * (Tinf - Tm) / (rho * deltaR * (raio-deltaR)/2)
    else:
        k = E + Hconv * deltaT * raio * (Tinf - Tm - (E - H) / Cl) / (rho * deltaR * (raio-deltaR)/2)
    line += [1]
    b += [[k]]
    mat += [line]
    # matrix calculation
    mat = np.matrix(mat)
    b = np.matrix(b)
    kk = np.linalg.solve(mat, b)
    k = []
    for kkk in kk:
        k.append(float(kkk))
    Es.append(k)

max_ent = 0
min_ent = 0
for vol in range(30):
    volume = 4*math.pi*deltaR*(deltaR*vol + deltaR/2)
    max_ent += ((Tp - Tm) * Cl + H) * volume * rho
    min_ent += ((Tinf - Tm) * Cs) * volume * rho

print("Calculation ready", ttime.time()-t1)


t1 = ttime.time()
with open("Enthalpies.txt", 'w') as thefile:
    for item in Es:
        thefile.write("%s\n" % item)
    thefile.close()
print("Results saved", ttime.time()-t1)

t1 = ttime.time()

show_divs = 5  # how many divisions to use

linestyles = ['-', '--', ':', '-.', '.', ',']

leg = []
fig1 = plt.figure()  # figure 1 => temperatures X time
plt.title("Temperature as a function of time")
plt.xlabel("Time (s)")
plt.ylabel("Temperature (ºC)")
plt.ylim(-15, 25)
style_flag = 0
for k in range(0, len(Es[0]), math.ceil((len(Es[0])-2)/show_divs)):  # plots temperature of show_divs volumes
    temps = make_temps(Es, k)
    plt.plot(temps)
    style_flag += 1
    legenda = "Volume " + str(k)
    leg.append(legenda)
if k != len(Es[0])-1:  # if boundary volume is not ploted, plot it
    k = len(Es[0])-1
    temps = make_temps(Es, k)
    plt.plot(temps)
    legenda = "Volume " + str(k)
    leg.append(legenda)
plt.grid(True)
plt.legend(leg)

leg = []
fig2 = plt.figure()  # figure 2 = enthalpies as a function of time
plt.title('Enthalpies as a function of time')
plt.xlabel("Time (s)")
plt.ylabel("Enthalpy (J/kg)")
style_flag = 0
for k in range(0, len(Es[0]), math.ceil((len(Es[0])-2)/show_divs)):  # plots enthalpy of show_divs volumes
    entalpias = make_E(Es, k)
    plt.plot(entalpias)
    style_flag += 1
    legenda = "Volume " + str(k)
    leg.append(legenda)
if k != len(Es[0])-1:  # if boundary volume is not plotted, plot it
    k = len(Es[0])-1
    entalpias = make_temps(Es, k)
    plt.plot(entalpias)
    legenda = "Volume " + str(k)
    leg.append(legenda)
locs, labels = plt.xticks()
plt.grid(True)
plt.legend(leg)

leg = []
fig3 = plt.figure()  # figura 3 = temperature as a function of control volume
plt.title("Temperatures as a function of control volume")
plt.xlabel("Control volume")
plt.ylabel("Temperature (ºC)")
plt.ylim(-15, 25)
style_flag = 0
for k in range(0, len(Es), math.ceil((len(Es)/show_divs))):  # plots the temperature of show_div times
    temps = make_R(Es[k])
    plt.plot(temps)
    style_flag += 1
    legenda = "Time " + str(k)
    leg.append(legenda)
if k != len(Es)-1:  # if the final time is not plotted, plot it
    k = len(Es)-1
    temps = make_R(Es[k])
    plt.plot(temps)
    legenda = "Time " + str(k)
    leg.append(legenda)
plt.grid(True)
plt.legend(leg)

leg = []
fig4 = plt.figure()  # figure 4 = enthalpies as a function of the control volume
plt.title("Enthalpies as a function of the control volume")
plt.xlabel("Control volume")
plt.ylabel("Enthalpy (J/kg)")
style_flag = 0
for k in range(0, len(Es), math.ceil((len(Es)/show_divs))):  # plots the temperature of show_divs times
    plt.plot(Es[k])
    style_flag += 1
    legenda = "Time " + str(k)
    leg.append(legenda)
if k != len(Es)-1:  # if the final time is not plotted, plot it
    k = len(Es)-1
    plt.plot(Es[k])
    legenda = "Time " + str(k)
    leg.append(legenda)
plt.grid(True)
plt.legend(leg)


fig5 = plt.figure()  # figure 5 = total enthalpy of system
plt.title("Enthalpy per meter of the system as a function of time")
plt.xlabel("Time (s)")
plt.ylabel("Cold fraction")
total_ent = []
flag_check_20 = True
for t, ent in enumerate(Es):
    vol_ent = 0
    for vol in range(len(ent)):
        volume = 4*math.pi*deltaR*(deltaR*vol + deltaR/2)
        vol_ent += ent[vol] * volume * rho
    vol_ent = (vol_ent - min_ent)/(max_ent - min_ent)
    if flag_check_20:
        if vol_ent < .2:
            flag_check_20 = False
            print("Time for  80% of capacity for radius =", raio, " and H =", Hconv, ": ", t)
    total_ent.append(1 - vol_ent)
plt.plot(total_ent)
plt.grid(True)

fig6 = plt.figure()  # figura 6 = heat transfer as a function of time
plt.title("Heat transfer as a function of time")
plt.xlabel("Time (s)")
plt.ylabel("Heat transfer")
trans_ent = []
for ent in range(len(Es)-1):
    vol_ent = 0
    vol_next = 0
    for vol in range(len(Es[ent])):
        volume = 4*math.pi*deltaR*(deltaR*vol + deltaR/2)
        vol_ent += Es[ent][vol] * volume * rho
        vol_next += Es[ent+1][vol] * volume * rho
    trans_ent.append(vol_next - vol_ent)
plt.plot(trans_ent)
plt.grid(True)


print("Plots ready", ttime.time()-t1)
plt.show()

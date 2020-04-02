from scipy.integrate import odeint
import matplotlib.pyplot as plt
import numpy as np
from ipywidgets import interactive, fixed

RES = 1000

class Model:
    def __init__(self, title, f, labels):
        self.title = title
        self.f = f
        self.labels = labels 

def SIR_f(y, t, ps):
    B, g = ps
    Si, Ii, Ri = y

    # Create f = (x1',y1',x2',y2'):
    return [
         -B*Si*Ii,
         B*Si*Ii - g*Ii,
         g*Ii
        ]
    return f

SIR = Model("SIR", SIR_f, ["Susceptible", "Infected", "Recovered"])


def SEIR_f(y, t, ps):
    La, mu, B, a, ga, N = ps
    Si, Ei, Ii, Ri = y

    return [
         La-mu*Si-B*Si*Ii/N,
         B*Si*Ii/N - (mu+a)*Ei,
         a*Ei-(ga+mu)*Ii,
         ga*Ii-mu*Ri
        ]
    return f

SEIR = Model("SEIR", SEIR_f, ["Susceptible","Exposed", "Infectious", "Recovered"])

def plot_method(t, res, method):
    plt.figure()
    plt.title(method.title)
    for i, r in enumerate(res):
        plt.plot(t, r, label=method.labels[i])
    plt.legend()


def run_sim(method, IVs, t_f, params):
    t = np.linspace(0,t_f,RES)

    soln = odeint(method.f, IVs, t, args=(params,))
    plot_method(t, np.transpose(soln), method)


def SIR_wrapper(S0=0.95, I0=0.05, R0=0.0, B=1.4, g=0.15):
    SIR_params = (B, g)
    SIR_IVs = [S0, I0, R0]

    run_sim(SIR, SIR_IVs, 50, SIR_params)

def SEIR_wrapper(S0=0.95, E0=0.0, I0=0.05, R0=0.0, La=0.0, mu=0.0, B=1.4, a=0.5, ga=0.15, N=1.0):
    SEIR_params = (La, mu, B, a, ga, N)
    SEIR_IVs = [S0, E0, I0, R0]

    run_sim(SEIR, SEIR_IVs, 50, SEIR_params)


if __name__ == "__main__":
    # SIR Model
    B = 1.4 
    g = 0.15
    SIR_params = (B, g)

    S0 = 0.95
    I0 = 0.05
    R0 = 0.0
    SIR_IVs = [S0, I0, R0]

    run_sim(SIR, SIR_IVs, 50, SIR_params)


    # SEIR Model
    La = 0.0 # Birth rate
    mu = 0.0 # Death rate
    B = 1.4 
    a = 0.5 # 1/(Incubation period)
    ga = 0.15
    N = 1
    SEIR_params = (La, mu, B, a, ga, N)

    S0 = 0.95
    E0 = 0.0
    I0 = 0.05
    R0 = 0.0
    SEIR_IVs = [S0, E0, I0, R0]

    run_sim(SEIR, SEIR_IVs, 50, SEIR_params)
    plt.show()




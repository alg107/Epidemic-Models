from scipy.integrate import odeint
import matplotlib.pyplot as plt
import numpy as np
from ipywidgets import interactive, fixed
import matplotlib.animation as animation


RES = 1000

def update(y, t, ps):
    r, g, gamma= ps
    theta, theta_dot = y

    # Create f = (x1',y1',x2',y2'):
    return [
         theta_dot,
         -(g/r)*np.sin(theta) -gamma*theta_dot 
        ]
    return f


def plot_method(t, res):
    plt.figure()
    for i, r in enumerate(res):
        plt.plot(t, r)


def run_sim(update_fn, IVs, t_f, params):
    t = np.linspace(0,t_f,RES)

    soln = odeint(update_fn, IVs, t, args=(params,))
    plot_method(t, np.transpose(soln))
    return t, np.transpose(soln)[0]



def update_plot(i):
    mat.set_data(xs[i], ys[i])
    line.set_data([0, xs[i]],[0, ys[i]])
    #ax.scatter(xs[i], ys[i])

if __name__ == "__main__":
    plt.gca().set_aspect('equal', adjustable='box')

    # SIR Model
    r = 1.0
    g = 9.81 
    gamma = 0.5
    params = (r, g, gamma)

    theta_0 = np.pi+0.01 
    vel_0 = 0.0
    IVs = [theta_0,vel_0] 

    ts, thetas = run_sim(update,IVs, 10, params)
    global xs
    global ys
    xs = r*np.sin(thetas)
    ys = -r*np.cos(thetas)

    fig, ax = plt.subplots()
    global mat
    ax.axis([-2,2,-2,2])
    mat, = ax.plot(xs[0], ys[0], 'o')
    line, = ax.plot([0, xs[0]], [0, ys[0]], 'o-', lw=2)
    ani = animation.FuncAnimation(fig, update_plot, interval=1)

    plt.show()




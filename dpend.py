from scipy.integrate import odeint
import matplotlib.pyplot as plt
import numpy as np
from ipywidgets import interactive, fixed
import matplotlib.animation as animation


RES = 1000
LENGTH = 20


def update(y, t, ps):
    l1, l2, m1, m2, g = ps
    th1, th2, w1, w2 = y

    # Create f = (x1',y1',x2',y2'):
    return [
         w1,
         w2,
         (-g*(2*m1+m2)*np.sin(th1)-m2*g*np.sin(th1-2*th2)-2*np.sin(th1-th2)*m2*(w2**2*l2+w1**2*l1*np.cos(th1-th2)))/(l1*(2*m1+m2-m2*np.cos(2*th1-2*th2))),
         (2*np.sin(th1-th2)*(w1**2*l1*(m1+m2)+g*(m1+m2)*np.cos(th1)+w2**2*l2*m2*np.cos(th1-th2)))/(l2*(2*m1+m2-m2*np.cos(2*th1-2*th2)))
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
    return t, np.transpose(soln)[0], np.transpose(soln)[1]



def update_plot(i):
    i = i%len(x1s)
    #pnt1.set_data(x1s[i], y1s[i])
    #pnt2.set_data(x2s[i], y2s[i])
    line1.set_data([0, x1s[i]],[0, y1s[i]])
    line2.set_data([x1s[i], x2s[i]], [y1s[i], y2s[i]])
    #ax.scatter(xs[i], ys[i])

if __name__ == "__main__":
    #plt.gca().set_aspect('equal', adjustable='box')

    # SIR Model
    l1 = 1.0
    l2 = 1.0
    m1 = 1.0
    m2 = 1.0
    g = 9.81 
    params = (l1, l2, m1, m2, g)

    th1_0 = np.pi/2 
    th2_0 = np.pi/2
    vel1_0 = 0.0
    vel2_0 = 0.0
    IVs = [th1_0, th2_0, vel1_0, vel2_0] 

    ts, th1s, th2s = run_sim(update,IVs, LENGTH, params)

    global x1s
    global y1s
    global x2s
    global y2s
    x1s = l1*np.sin(th1s)
    y1s = -l1*np.cos(th1s)
    x2s = x1s + l2*np.sin(th2s)
    y2s = y1s -l2*np.cos(th2s)

    fig, ax = plt.subplots()
    global pnt1, pnt2
    ax.axis([-2,2,-2,2])
    #pnt1, = ax.plot(x1s[0], y1s[0], 'o')
    #pnt2, = ax.plot(x2s[0], y2s[0], 'o')
    line1, = ax.plot([0, x1s[0]], [0, y1s[0]], 'o-', lw=2)
    line2, = ax.plot([x1s[0], x2s[0]], [y1s[0], y2s[0]], 'o-', lw=2)

    # Speed adjustments
    SPEED = int(4*10/LENGTH)
    x1s = x1s[::SPEED]
    x2s = x2s[::SPEED]
    y1s = y1s[::SPEED]
    y2s = y2s[::SPEED]

    ani = animation.FuncAnimation(fig, update_plot, interval=1)

    plt.show()




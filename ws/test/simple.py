import numpy as np
import matplotlib.pyplot as plt


L = 2
m = 1
g = 9.81
phi_init = np.pi/2 - 0.1

T_max = 10
dt = 0.01
T = np.arange(0, T_max, dt)

phi = []
phi.append(phi_init)

for t in T:
    tau_g = -m*g*L*np.cos(phi[-1])

    tau = tau_g + tau_u
    d_phi = tau/(m*L**2)
    phi.append(phi[-1] + d_phi*dt)


plt.plot(T, phi[:-1])
plt.show()


# Active inference functions
mu_g = np.pi/2
sigma_mu0 = 0.1
sigma_y0 = 0.1
sigma_mu1 = 0.1
sigma_y1 = 0.1

K_mu = 1

mu0_list = []
mu1_list = []
mu2_list = []
y0_list = []
u_list = []

def F(mu0, y0):
    mu1 = (mu0 - mu0_list[-1])/dt
    mu2 = (mu1 - mu1_list[-1])/dt
    mu0_list.append(mu0)
    mu1_list.append(mu1)
    mu2_list.append(mu1)

    y1 = (y0 - y0_list[-1])/dt
    y0_list.append(y0)

    # position part
    e0_y = y0 - g(mu0)
    e0_mu = mu1 - f(mu0) 
    F0 = (e0_y/sigma_y0)**2 + (e0_mu/sigma_mu0)**2

    # velocity part
    e1_y = y1 - dgdmu(mu1) * mu1
    e1_mu = mu2 - dfdmu(mu1) * mu1
    F1 = (e1_y/sigma_y1)**2 + (e1_mu/sigma_mu1)**2

    return (F0 + F1)/2


def g(mu):
    return mu

def f(mu):
    return (mu_g - mu)

def dgdmu(mu):
    return 1

def dfdmu(mu):
    return -1

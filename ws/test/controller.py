import numpy as np
import cvxpy as cp

class Controller:
    def __init__(self, L, m, g, phi_init, sigma_w, sigma_z):
        self.L = L
        self.m = m
        self.g = g

        self.sigma_w = sigma_w
        self.sigma_z = sigma_z

        self.phi = phi_init
        self.x_hypothesis = [phi_init]
        self.y_observation = [phi_init]
        self.tau_u = [0]

    def f(self, mu, tau_u): # x = phi
        tau_g = -self.m*self.g*self.L*(-(mu-np.pi/2)) # Taylor to approximate cos(x) around pi/2
        tau = tau_g + tau_u
        d_phi = tau/(self.m*self.L**2)
        return d_phi

    def g(self, mu): # x = phi
        return mu 

    def free_energie(self, x, tau_u):
        e_x = x - self.f(x, tau_u)
        e_y = self.y_observation[-1] - self.g
        return ((e_x/self.sigma_w)**2 + (e_y/self.sigma_z)**2)

    def control(self, y):
        print("Added observation")
        self.y_observation.append(y)

        print("Creating problem...")
        tau_u = cp.Variable()
        x = cp.Variable()
        objective = cp.Minimize(self.free_energie(x, tau_u))
        constraints = [x >= -np.pi, x <= np.pi, tau_u >= -10, tau_u <= 10]
        problem = cp.Problem(objective, constraints)

        print("Solving problem...")
        problem.solve()
        self.tau_u.append(tau_u.value)
        self.x_hypothesis.append(x.value)

        return tau_u.value

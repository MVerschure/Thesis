import numpy as np
from scipy.linalg import toeplitz, cholesky, sqrtm, inv
import time
import matplotlib.pyplot as plt

N = 1000
dt = 0.01
M = 1
L = 1
g = 9.81

# x is position in radians 

def f_gp(x, v):
    tau_g = -M*g*L*np.sin(x)
    dx = tau_g/(M*L**2)
    return dx

def df_gp(x, v):
    return -g*np.cos(x)

def g_gp(x, v):
    return x

def dg_gp(x, v):
    return 1

def derivativeD(p):
    D = toeplitz(np.zeros([1,p+1]),np.append(np.array([0,1]),np.zeros([1,p-1])))
    return D

def standard_vec(p):
    x = np.zeros((p+1,1))
    x[0] = 1
    return x

def standard_vec_inv(p):
    x = np.ones((p+1,1))
    x[0] = 0
    return x

def temporalC(p,s2):
    """
    Construct the temporal covariance matrix S for noise with embedding order p and smoothness parameter s
    
    Code by Sherin Grimbergen (V1 2019) and Charel van Hoof (V2 2020)
    
    INPUTS:
        p       - embedding order (>0)
        s2      - smoothness parameter (>0), variance of the filter (sigma^2)
        
    OUTPUT:
        S       - temporal covariance matrix ((p+1) x (p+1))
    """ 

    q = np.arange(p+1)
    
    r = np.zeros(1+2*(p))
    r[2*q] = np.cumprod(1-2*q)/(2*s2)**(q)    
    
    S = np.empty([0,p+1])

    for i in range(p+1):
        S = np.vstack([S,r[q+i]])
        r = -r
           
    return S

def generalize(y,p):
    """
    Construct generalised value with embedding order p 
    By [y,0,0...]
    
    INPUTS:
        y       - Input sensory signal
        p       - embedding order (>0)
        
    OUTPUT:
        y_tilde - Generalised sensory signal
    """ 
    if p<0:
        # unknown embedding order, error
        raise ValueError('Embedding order < 0')    
    
    if np.shape(y)==(p+1, 1):
        # Generalised value, use it
        y_tilde=y;
        return y_tilde
    
    # Generalize sensory observation by adding zero's
    y_tilde = np.zeros((p+1,1))
    y_tilde[0] = y

    return y_tilde


class ai_capsule():
    def __init__(self, dt, mu_v, p, sigma_w, sigma_z, a_mu, s2_w, s2_z): 
        self.p = p
        self.dt = dt
        self.mu_x = mu_v
        self.sigma_w = sigma_w
        self.sigma_z = sigma_z
        self.a_mu = a_mu
        self.D = derivativeD(p)
        self.std_vec_inv=standard_vec_inv(p)
        self.std_vec=standard_vec(p)
        self.I = np.identity(self.p+1)

        self.s2_w = s2_w # estimated variance of the gaussian filter used to create the smoothened noise w
        self.s2_z = s2_z # Estimated variance of the Gaussian filter used to create the smoothened noise zk
        self.Pi_w = inv(np.kron(temporalC(self.p,self.s2_w),self.sigma_w)) # precision matrix of smoothened noise w
        self.Pi_z = inv(np.kron(temporalC(self.p,self.s2_z),self.sigma_z)) # precision matrix of smoothened noise z

        self.eps_x = 0
        self.eps_y = 0
        self.F = 0

    def g(self, mu_x, mu_v):
        return g_gp(mu_x, mu_v)

    def dg(self, mu_x, mu_v):
        return dg_gp(mu_x, mu_v)

    def f(self, mu_x, mu_v):
        return mu_v

    def inference_step(self, mu_v, y):
        # Calculate prediction errors
        Atilde = df_gp(self.mu_x[0],mu_v[0])
        self.eps_x = (self.D-Atilde).dot(self.mu_x) - mu_v  # prediction error hidden state
        self.eps_y = y - self.std_vec*g_gp(self.mu_x[0],mu_v[0]) - self.std_vec_inv * dg_gp(self.mu_x[0],mu_v[0]) * self.mu_x #prediction error sensory observation
        # In case a linear state space model is used with linear equation of sensory mapping the below calculation is equivalent
        #self.eps_y = y - self.Ctilde.dot(self.mu_x) #prediction error sensory observation
        
        #print('mu_x=', self.mu_x[0],'mu_y=', g_gp(self.mu_x[0],mu_v[0]), 'x_dot',self.mu_x[1])
        #print( 'ex',self.eps_x)
        #print( 'ey',self.eps_y)

        # Free energy gradient
        dFdmu_x = (self.D-Atilde).T.dot(self.Pi_w).dot(self.eps_x) - (dg_gp(self.mu_x[0],mu_v[0]) * self.I).T.dot(self.Pi_z).dot(self.eps_y)
        # In case a linear state space model is used with linear equation of sensory mapping the below calculation is equivalent
        #dFdmu_x = (self.D-self.Atilde).T.dot(self.Pi_w).dot(self.eps_x) - self.Ctilde.T.dot(self.Pi_z).dot(self.eps_y)
        
        # Perception dynamics
        dmu_x   = np.dot(self.D,self.mu_x) - self.a_mu * dFdmu_x  
        self.mu_x = self.mu_x + self.dt * dmu_x
        
        
        # Calculate Free Energy to report out
        self.F= 0.5*( self.eps_x.T.dot(self.Pi_w).dot(self.eps_x) + self.eps_y.T.dot(self.Pi_z).dot(self.eps_y)) #+ np.log(self.Sigma_w * self.Sigma_z) )
        
        return self.F.item(0), self.mu_x[0] , g_gp(self.mu_x[0],mu_v[0])


def simulation (v, mu_v, Sigma_w, Sigma_z, noise, a_mu):
    """
    Basic simplist example perceptual inference    
   
    INPUTS:
        v        - Hydars actual depth, used in generative model, since it is a stationary example hidden state x = v + random fluctuation
        mu_v     - Hydar prior belief/hypotheses of the hidden state
        Sigma_w  - Estimated variance of the hidden state 
        Sigma_z  - Estimated variance of the sensory observation  
        noise    - white, smooth or none
        a_mu     - Learning rate for mu
        
    """


    
    # Init tracking
    mu_x = np.zeros(N) # Belief or estimation of hidden state 
    F = np.zeros(N) # Free Energy of AI neuron
    mu_y = np.zeros(N) # Belief or prediction of sensory signal
    x = np.zeros(N) # True hidden state
    y = np.zeros(N) # Sensory signal as input to AI neuron
    p = 2

    # Create active inference neuron
    mu_v_tilde = generalize(mu_v,p)
    capsule = ai_capsule(dt, mu_v_tilde, p, Sigma_w, Sigma_z, a_mu, 1/64, 1/64)

    
    # Simulation
    for i in np.arange(1,N):
        x[i]= v 
        y[i] = g_gp(x[i],v)

        y_tilde = generalize(y[i],p)
        #Active inference
        F[i], mu_x[i], mu_y[i] = capsule.inference_step(mu_v_tilde,y_tilde)


    return F, mu_x, mu_y, x, y

# Test case

v = 30 # actual depth Hydar
mu_v = 25 # Hydars belief of the depth
F1, mu_x1, mu_y1, x1, y1 = simulation(v,mu_v,1,1,'no noise',1) # prior and observation balanced, both variance of 1


# Plot results:
fig, axes = plt.subplots(3, 1, sharex='col');
fig.suptitle('Basic Active Inference, inference part');
axes[0].plot(mu_x1[1:],label='Belief');
axes[0].plot(x1[1:],label='Generative process');
# axes[0].hlines(mu_v, 0,T, label='Prior belief')
axes[0].set_ylabel('$\mu_x$ position');
fig.legend(bbox_to_anchor=(1.05, 1), loc='upper left', borderaxespad=0.)
axes[0].grid(1);
axes[1].plot(mu_y1[1:],label='Belief');
axes[1].plot(y1[1:],label='Generative process');
# axes[1].hlines(g_gp(mu_v,0), 0,T, label='Prior belief')
axes[1].set_ylabel('$\mu_y$ temperature');
axes[1].grid(1);
axes[2].semilogy(F1[1:],label='Belief');
axes[2].set_xlabel('time [s]');
axes[2].set_ylabel('Free energy');
axes[2].grid(1);

plt.legend()
plt.show()

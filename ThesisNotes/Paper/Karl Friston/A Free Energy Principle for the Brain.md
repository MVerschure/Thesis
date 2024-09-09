"Many people now regard the brain as an ingerence machine that conforms to the same principles that govern the interrogarion of scientific data". 
### 3. Theory
Starting with evolutionary or selectionist considerations, the quenstion of how biological systems operate is tranformed into simpler questions about their behaviour. These constraints lead to the #ensemble-density encoded by the state of the {biological} system. This density is used to construct a #free-energy the minimization of which leads to perceptual inference about the world, encoding of perceptual context, etc. 
The #free-energy-principle is the principle that the brain changes to minimize the #free-energy.
### 4.  The Nature of Biological Systems
"A key aspect of biological systems is that they act upon the environment to change their position within it, or relation to it, in a way that precludes extremes of temperature, pressure, and other external fields." "By considering the nature of biological systems in terms of selective pressure one can replace difficult questions about how biological systems emerge with questions about what behaviours they must exhibit to exist. In other words, selection explains how biological systems arise; the only outstanding issue is what characterises they must possess."
#### 4.1 The Ensemble Density
Let $\vartheta$ parameterise environmental forces or field that act upon the system, and $\lambda$ be quantities that describe the systems physical state. The #ensemble-density function is then defined as an arbitrary function $q(\vartheta;\lambda)$. For example, $\lambda$ could represent the mean and variance of a Gaussian distribution on the environments temperature, $\vartheta$. The reason $q(\vartheta:\lambda)$ is called the #ensemble-density is that it van be ragarded as the probability density that a specific environmental state $\vartheta$ would be selected from a infinite ensemble of environments given the systems state $\lambda$.
In addition to the previous mentioned variables, 2 extra are needed: $\tilde{y}$ and $\alpha$. $\tilde{y}$ represents the state of the sensory receptors and $\alpha$ represent the force exerted by effectors that oct on the environment to change sensory samples. 
### 5. The Free Energy Principle
The #free-energy is a scalar function of the ensemble density and the current sensory input. It comprises two terms
$$
\tag{1}
F = - \int q(\vartheta)\ln\frac{p(\tilde{y}, \vartheta)}{q(\vartheta)} d\vartheta
= -\langle \ln p(\tilde{y}, \vartheta) \rangle_q + \langle \ln q(\vartheta)\rangle_q
$$
The first term is the energy of this system expected under the ensemble density. The energy is simply the surprise or information about the joint occurrence of the sensory input and its causes $\vartheta$. The second therm is the negative entropy of the #ensemble-density.

Note that the #free-energy is defined by two densities: the #ensemble-density $q(\vartheta; \lambda)$ and the #generative-density $p(\tilde{y}, \vartheta)$, from which one can *generate* sensory samples and their causes. The #generative-density factorises into a likelyhood and prior density ( #basian) $p(\tilde{y}|\vartheta)p(\vartheta)$.

The #free-energy-principle states that all the quantities that can change; i.e., that are owned by the system, will change to minimise #free-energy. 
#### 5.1 Perception: optimizing $\lambda$
Rearranging Eq. $\eqref{1}$ to show the dependence of the free energy on $\lambda$.
$$
\tag{2}
F = -\ln p(\tilde{y}) + D(q(\vartheta;\lambda)||p(\vartheta|\tilde{y}))
$$
Only the second term has a dependency on $\lambda$; this is a Kullback-Leibles cross-entropy of divergence term that measures the difference between the #ensemble-density and the #conditional-density. Thus minimizing the #free-energy minimizes the difference the #ensemble-density and the #conditional-density.  "In other words, the #ensemble-density  encoded by the systems state becomes an approximation to the posterior probability of the causes of its sensory input."
####  5.2 Action: optimizing $\alpha$
A second rearrangment of Eq. $\eqref{1}$ shows the dependece on $\alpha$.
$$
\tag{3}
F = -\langle \ln p(\tilde{y}(\alpha)|\vartheta)\rangle_q + D(q(\vartheta)||p(\vartheta))
$$
Only the first term is a function of the action. Minimizing this term corresponds to maximizing the log probability of the sensory input, expected under the #ensemble-density. In other words, the system will reconfigure itself to sample sensory inputs that are the most likely under the ensemble density. "*However, as we have just seen, the #ensemble-density approximates the conditional distribution of the causes given sensory inputs. The inherent circularity obliges the system to fulfil its own expectations.*"
#### 5.3 The Mean-Field Approximation
Up to here, all quantities describing the environment have been treated together. Here we will make a distinction based upon their rate of change: $\vartheta = \vartheta_u, \vartheta_{\gamma}, \vartheta_{\theta}$, where the parameters change quickly, slowly and very slowly. The #ensemble-density becomes:
$$
\tag{4}
q(\vartheta) = \prod_i q(\vartheta_i;\lambda_i)
$$
**The approximation with three partitions is a little arbitrary**. 
### 6. Optimizing Variantional Modes
Variational techniques predominate under the #mean-field-approximation. The #free-energy in Eq. $\eqref{1}$ is also known as the variational #free-energy.  The #mean-field-approximation cannot cover the effect of random fluctuations in one partition effecting another partition.
Under the #mean-field-approximation the #ensemble-density has the following form:
$$
\tag{4}
\begin{aligned}
q(\vartheta_i) \propto \exp(I(\vartheta_i)) \\
I(\vartheta_i) = \langle \ln p(\tilde{y}, \vartheta) \rangle_{q_{\backslash1}}
\end{aligned}
$$
The mode(average?) is an important variational parameter. If we assume $q(\vartheta)$ is Gaussian, then it is parameterised by two variational parameters $\lambda_i = \mu_i, \Sigma_i$ encoding the mode and covariance. 
#### 6.1 Perceptual Inference: Optimizing $\mu_u$
Minimizing the the #free-energy with respect to neuronal states $\mu_u$ means maximizing $I(\vartheta_u)$.
$$
\tag{5}
\begin{aligned}
\mu_u = \max I(\vartheta_u) \\
I(\vartheta_u) = \langle \ln p(\tilde{y}|\vartheta) + \ln p(\vartheta) \rangle_{q_{\gamma}q_{\theta}}=\langle \ln p(\vartheta|\tilde{y}) \rangle_{q_{\gamma}q_{\theta}} + \ln p(\tilde{y})
\end{aligned}
$$
 **The brain states will come to encode the most likely state of the environment that is causing sensory input**
#### 6.2 Generalized Coordinates
 
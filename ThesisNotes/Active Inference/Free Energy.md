Here an attempt at some structured notes for the free energy principle.
#### The Ensemble Density
Let $\vartheta$  parameterise environmental forces or field that act upon the system and $\lambda$ be quantities that describe the system physical state. These can be very high dimensional and time-varying. To link these quantities we invoke an arbitrary function $q(\vartheta; \lambda)$: the #ensemble-density. 

The #ensemble-density is some arbitrary density function on the environment parameters. For example, $\lambda$ could represent the mean and variance of a Gaussian distribution on the environments temperature, $\vartheta$. The reason $q(\vartheta:\lambda)$ is called the #ensemble-density is that it van be ragarded as the probability density that a specific environmental state $\vartheta$ would be selected from a infinite ensemble of environments given the systems state $\lambda$.
#### The Free Energy Principle
In addition to the previous mentioned variables, 2 extra are needed: $\tilde{y}$ and $\alpha$. $\tilde{y}$ represents the state of the sensory receptors and $\alpha$ represent the force exerted by effectors that oct on the environment to change sensory samples. 

The #free-energy is a scalar function of the ensemble density and the current sensory input. It comprises two terms
$$
F = - \int q(\vartheta)ln\frac{p(\tilde{y}, \vartheta)}{q(\vartheta)} d\vartheta
= -\langle \ln p(\tilde{y}, \vartheta) \rangle_q + \langle\ln q(\vartheta)\rangle_q
$$
The first term is the energy of this system expected under the ensemble density. The energy is simply the surprise or information about the joint occurrence of the sensory input and its causes $\vartheta$. The second therm is the negative entropy of the #ensemble-density.

Note that the #free-energy is defined by two densities: the #ensemble-density $q(\vartheta; \lambda)$ and the #generative-density $p(\tilde{y}, \vartheta)$, from which one can *generate* sensory samples and their causes. The #generative-density factorises into a likelihood and prior density ( #basian) $p(\tilde{y}|\vartheta)p(\vartheta)$.

The #free-energy-principle states that all the quantities that can change; i.e., that are owned by the system, will change to minimise #free-energy. 
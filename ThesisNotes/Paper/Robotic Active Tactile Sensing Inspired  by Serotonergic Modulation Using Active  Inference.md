### 1. Introduction
Perception is not passive. Bio-agents explore the world such as to inform us. In humans, serotonin seems to be involved in the sensitivity of sensory processing. The level of serotonin might indicate the level of detail searched for.
Here they present a model inspired by this behaviour. 
### 2. Methods
The discrete state space #active-inference is used to model the robot's behaviour. 
$$
P(o, s, \pi, A, B) = P(\pi|A, B)P(A)P(B)\prod_{t=1}^T P(o_t|s_t, A)P(s_t|s_{t-1}, \pi, B)
$$
with
$$
\begin{aligned}
P(o_t|s_t) = Cat(A)\\
P(s_{t+1}|s_t,\pi) = Cat(B_{\pi, t}) \\
P(\pi) = \sigma(-E \cdot G) \\
Q(s_t|\pi) = Cat(s_{\pi,t}) \\
Q(\pi) = Cat(\pi)
\end{aligned}
$$
For a visual representation see the paper. The term $o$, $s$, $\pi$ and $t$ stand for the outcomes, hidden states, policies and time-steps respectively. The model parameters $A$, $B$ and $E$ refer to the likelyhood and transition matrices and a habitual vector respectively. Finaly, $Cat(\bullet)$ specifies a categorical distribution and $\sigma$ a softmax function.
#### 2.1 Agent Model
The agens is modeld using the discrete Partially-Observable Markov Decision Process (POMDP) formalism. This provides a mapping from outcomes to hidden states. The agent has a hidden state $s$ which evolves overtime depending on the transition function $B$ and is updates given the observation  $o$ at each timestep. The agens has a mapping (likelyhood) of observations given the state.
#### 2.2 Active Inference
This by now should be familiar
$$
\mathcal{F} = \underbrace{D_{KL}[Q(s)||P(s)]}_{Complexity} - \underbrace{E_{Q_{(s)}}(\ln P(o|s))}_{Accuracy}
$$
The complexity term compares the approcimate posterior distribution $Q(s)$ with the model's prior distribution $P(s)$. The accuracy term assures the agent of inferring thoe states that can explain the stimuli $o$ the most. Without the complexity term, the accuracy would lead to observations overfitting, and without the accuracy term the agent would ignore the outside world and focus on the model’s beliefs without updating them. Hence, free energy is a balance of exploitation (i.e., fulfilling our priors) and exploration (i.e., inferring the most informative hidden states).
##### 2.2.1 Action selection
The agent's action selection is defined as computing the optimal policy $\pi$, given the combination of the habitual behaviours $E$ (i.e. a behaviour occurring automatically, without a complex inference) and the optimization of the Expected Free Energy (G) of executing a plan of actions in the future:
$$
\pi = \arg \max Q(\pi) = \arg \max \sigma[\rho \ln E(\pi) - G(\pi)]
$$
Where $\rho$ is the precision parameter that modulates the interplay between habitual policies and new computed optimal policies. The policy with the higher probability is selected. 
The #expected-free-energy objective function $G$ is used, which predicts the pree energy value in the next time-point. A relevant difference between the free energy F and G is that the latter is sampled from the predictive posterior distribution. This means that the agent predicts the consequences of its actions and calculates the deviance from surprise based on these. The risk calculates the posterior value of a hidden state in the next time-step, given a policy selected at a given moment that is compared to the prior beliefs of the agent. This assures a selection of such a policy that leads to fulfilling the priors. On the other hand, the ambiguity term functions similarly to the accuracy term mentioned above, but the likelihood is predictive (over the next time step) based on the averaged approximate distribution of an expected hidden state given a policy Q(sτ |π). This means that the ambiguity term selects those policies that are most informative.
#### 2.3 Precision Modulation
Sensory precision $\zeta$ modulates the impact of the sensory input.
$$
A = \sigma(\zeta \ln(A + \epsilon))
$$
Where $\sigma$ is the softmax function and $\epsilon$ is some arbitrary small number that prevents $\ln 0$. $A$ represents the likelihood mapping between states and observations. 
#### 2.4 Model Tailored to Robotic Tactile Active Sensing

pymdp - python package which "implements active inference agents in discre time"

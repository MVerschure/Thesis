### 1. Introduction
The general idea is that objects are central in our interaction with the world. Or the idea that objects are the building blocks of the world. #OBAI is introduced, it combines deep, object-based neural networks and active inference.
#OBAI should be able to: i) learn to segment and represent objects ii) learn the action-dependent, object-based dynamics of the environmet; and iii) plan in the latent space - obviating the need to imagine detailed pixel-level outcomes in order to generate behaviour.
### 2. Methods
#### 2.1 Object-Structured Generative Model
The framework is inspired by #IODINE, a model for object representation learning. This method will depend on #iterative-amortized-inference, just like #IODINE, on an object-stuctured generative model.  This model describes images of up to K object with a Normal mixture density.
$$
\tag{1}
p(o_i|\{\textbf{s}^{(k)}\}_{k\in1:K},m_i) = \sum_k[m_i = k] \mathcal{N} \left( g_i(\textbf{s}^{(k)}), \sigma_o^2 \right)
$$
where $o_i$ is the value of the $i$-th image pixel, $\textbf{s}^{(k)}$ is the state of the $k$-th object, $g_i(\bullet)$ is a decoder function (DNN) that translates an objec state to a predicted mean value at pixel $i$, $\sigma_o^2$ is the variability of pixels around their mean values and  $m_i$ is a categorical variable that indicates which object (out of $K$ possible choises) pixel $i$ belongs to. The same decoder function is shared between objects. The pixel assignments themselces also depend on the object states:
$$
\tag{2}
p(m_i|\{\textbf{s}^{(k)}\}_{k\in1:K}) = \textrm{Cat} \left( \textrm{Softmaax} \left( \{\pi_i(\textbf{s}^{(k)})\}_{k\in1:K} \right)\right)
$$
where $\pi_i(\bullet)$ is another DNN that maps an object state to a log-probabiltiy at pixel $i$, which defines the probability that the pixel belongs to that object. Marginalized ofer the assignment probabilities, the pixel likelihoods are given by:
$$
\tag{3}
p(o_i|\{\textbf{s}^{(k)}\}_{k\in1:K}) = \sum_k \hat{m}_{ik} \mathcal{N} \left( g_i(\textbf{s}^{(k)}), \sigma_o^2 \right)
$$
$$
\tag{4}
\hat{m}_{ik} = p(m_i=k|\{\textbf{s}^{(k)}\}_{k\in1:K})
$$
#### 2.2 Incorporating Action-Dependent Dynamics
Generalized coordinates are introduced, i.e. $\textbf{s}_t^\dagger = \begin{bmatrix} \textbf{s}_t \\ \textbf{s}_t' \end{bmatrix}$. The action dependent state dynamics are then given by:
$$
\tag{5} \label{5}
\textbf{s}_t'^{(k)} = \textbf{s}_{t-1}'^{(k)} + \textbf{Da}_{t-1}^{(k)} + \sigma_s \epsilon_1
$$
$$
\tag{6} \label{6}
\textbf{s}_t^{(k)} = \textbf{s}_{t-1}^{(k)} + \textbf{s}_t'^{(k)} + \sigma_s \epsilon_2
$$
Where $\textbf{a}_t^{(k)}$ is the action on object $k$ at time $t$. This action is a 2-D vector that specifies the acceleration on the object in picel coordinates. Multiplication by $\textbf{D}$ transforms the pixel-space acceleration to its effect in the latent space. Equations $\eqref{5}$ and $\eqref{6}$ define the object dynamics model as $p(\textbf{s}_t^{\dagger(k)}|\textbf{s}_{t-1}^{\dagger(k)}, \textbf{a}_{t-1}^{(k)})$.

There is still a correspondence problem between objects representations in the model and objects in the real world. The authors solved this *action fields*. An action field $\boldsymbol{\Psi} = [\psi_1, \ldots, \psi_M]^T$ in an $[M \times 2]$ matrix ($M$ is the number of pixels in the frame), such the the $i$-th ros in this matrix, i.e. $\psi_i$, specifies the (x,y)-acceleration applied at picel $i$. Objects get affected by the sum of acceleration of all their visible pixels:
$$
\tag{7}
\textbf{a}_t^{(k)} = \sum_i [m_i=k]\psi_i + \sigma_{\psi}\epsilon_3
$$
#### 2.3 Inference
#iterative-amortized-inference generalizes variational autoencodes (VAEs), which perform inference in a single feedforward pass, to achitectures which use several iterations to minimize the Evide Lower Bound (ELBO). As in VAEs, the result is a set of variational beliefs in the latent space of the network. In our case the amounts to inferring $q(\{\textbf{s}^{\dagger(k)}, \textbf{a}^{(k)}\}_{k\in1:K})$ ( #ensemble-density ?)  Infernce and learning both minimize ELBO loss (super long formula, not going to type that).
#### 2.4 Task and Training
They created an "environment" where shapes can move along linear trajectories and be perturbed trough the action fields. For more training specifics see the paper :)
##### 2.4.1 Learning Goals in the Latent Space
The task was to move a certain object to a certain location. This goal was conceptualized as a preference distribution $\tilde{p}$. However, rather than defining this preference to be over observations, as is common, ther defined it over the latent state, i.e. $\tilde{p}(\{\textbf{s}^{\dagger(k)}\})$. This simplifies action selection (?)
### Questions
- [ ] What is #iterative-amortized-inference?
- [ ] What does it mean when objects have a Normal mixture density?
- [ ] How would this need to be adapted to 
import Pkg; Pkg.activate(".."); Pkg.instantiate();
using RxInfer, Random, Plots

# Generating data
#
# A function that returns a random one hot encoded vector
function rand_vec(rng, distribution::Categorical)
  k = ncategories(distribution)
  s = zeros(k)
  drawn_category = rand(rng, distribution)
  s[drawn_category] = 1
  return s
end
  
# A function to ....
function generate_data(rng, N)
  # Transition probabilities 
  state_transition_prob = [0.9 0.1; 0.1 0.9]

  # Emmision probabilities
  emission_prob = [0.9 0.1; 0.1 0.9]

  # Initial state
  s_init = [1, 0];

  s = Vector{Vector{Float64}}(undef, N)
  y = Vector{Vector{Float64}}(undef, N)

  s_prev = s_init

  for i in 1:N
    s_prob_vec = state_transition_prob * s_prev
    s[i] = rand_vec(rng, Categorical(s_prob_vec ./ sum(s_prob_vec)))
    obs_prob_vec = emission_prob * s[i]
    y[i] = rand_vec(rng, Categorical(obs_prob_vec ./ sum(obs_prob_vec)))
    s_prev = s[i]
  end

  return s, y
end

# Create data
rng = MersenneTwister(42)
N = 100

s, y = generate_data(rng, N)

display(scatter(argmax.(s)))
savefig(scatter(argmax.(s)), "s.png")


# Model
@model function hmm(y)
  A ~ MartrixDirichlet(ones(2, 2))
  B ~ MartrixDirichlet(ones(2, 2))

  s_0 = Categorical(fill(1/3, 3))


# Activate local environment, see `Project.toml`
import Pkg; Pkg.activate(".."); Pkg.instantiate();

println("Lets begin!!")

# So the idea is to create the simplest case possible of the sensor fusion project I'm trying 
# to accomplisch using bayesian inference. This would be to generate 2 data points, each 
# representing the state of a single object and some odometry data, and propose a model which
# is capable of generating the probability that the object in the two data points are the same,
# given the odometry data. Lets assume a stationary object 1m in front of the robot. The robot
# does not change in x,y position, but does rotate 10 degrees counter clockwise. A global 
# coordinate frame is chosen such that the robot starts at (0,0) and the object at (1,0).
#
# I'm going to first try a 1D case.


using RxInfer, Random

@model function one_dim_model(y, size, T, unobserved_prior)
  # Declare the state variable `x` as a random variable array with size `(size, length(y))`

  # Define the transition of the state
  for i in 1:size
    x[i][1] ~ Bernoulli(unobserved_prior)  # Initial state

    for t in 2:T
      x[i][t] := x[i][t - 1]  # Transition (here, simply copying the previous state)
      end
  end

  # Define the observation model
  for i in 1:size
    for t in 1:length(y)
      y[i][t] ~ Normal(mean = x[i][t], variance = 0.1)
    end
  end
end

println("Model defined")
println("Starting inference")

dataset = [[0, 0, 0, 0, 0],
           [0, 1, 1, 1, 1],
           [0, 0, 0, 0, 0]]

result = infer(
  model = one_dim_model(size = 3, T=5 , unobserved_prior = 0.5),
  data = (y = dataset,)
)

x_estimated = result.posteriors[:x]  
x11 = x_estimated[1, 1]
x15 = x_estimated[1, 5]
x23 = x_estimated[2, 3]

println(x11)
println(x15)
println(x23)


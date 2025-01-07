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

using RxInfer, Random

rng = MersenneTwister(42)


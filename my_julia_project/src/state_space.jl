import Pkg; Pkg.activate(".."); Pkg.instantiate();
using RxInfer, Random, BenchmarkTools, Plots

println("Lets begin!!")

@model function my_model(y, trend, variance)
  x[1] ~ Normal(mean = 0.0, variance = 100.0)
  y[1] ~ Normal(mean = x[1], variance = variance)

  for i in 2:length(y)
    x[i] ~ Normal(mean = x[i-1] + trend, variance = 1.0)
    y[i] ~ Normal(mean = x[i], variance = variance)
  end
end

println("Model defined")
println("Starting inference")

result = infer(
  model = my_model(trend = 5, variance =1),
  data = (y = [0.0, 5.0, 10.0, 15.0],)
)

x_estimated = result.posteriors[:x][3]
println(x_estimated)

r = range(0, 25, length = 200)
p = plot(title = "Inference results")

plot!(r, (x) -> pdf(x_estimated, x), label = "x[3]")
display(p)
savefig(p, "inference_results.png") 


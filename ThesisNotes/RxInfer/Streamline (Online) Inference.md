#### The Model
The model assumed throughout this "reference" is the following
```julia
@model function beta_bernoulli_online(y, a, b)
    θ ~ Beta(a, b)
    y ~ Bernoulli(θ)
end
```
##### @autoupdates
RxInfer needs an "incentive" to perform automatic updates over marginals. This can be done with the `@autoupdates` macro.
```julia
beta_bernoulli_autoupdates = @autoupdates begin
    # We want to update `a` and `b` to be equal to the parameters
    # of the current posterior for `θ`
    a, b = params(q(θ))
end
```
My current understanding is that this "tells" RxInfer that `a, b` are the parameters of the distrubution over $\theta$, and that we want to infer these parameters.
###### Questions
- Does the `q` in `q(θ)`  have a predetermined meaning? Is it known that it specifies the approximate posterior distribution?
- It seems that in Julia the names of variables matter. That although `a` and `b` are mentioned within two different scopes (with my python/cpp based understanding of scopes), Julia/RxInfer seems to be aware that the parameters used in the `@autoupdates` macro refer to those defined previously in the `@model` macro.
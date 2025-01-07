FROM julia:latest

# Copy project files
COPY Project.toml Manifest.toml ./

# Install Julia dependencies
RUN julia -e 'using Pkg; Pkg.instantiate()'

# Install additional packages
RUN julia -e 'using Pkg; Pkg.add(["Plots", "RxInfer", "Random", "StableRNGs", "LinearAlgebra", "StatsPlots", "LaTeXStrings", "DataFrames", "CSV", "GLM"]); Pkg.precompile()'

# Set up locale
RUN apt-get update
RUN apt-get install -y locales locales-all
ENV LC_ALL=en_US.UTF-8
ENV LANG=en_US.UTF-8
ENV LANGUAGE=en_US.UTF-8



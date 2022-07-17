# Series of tests on simulated data

#%%

# Packages
## NumPy and Pandas are required to generate the synthetic data 

import numpy
import pandas
import effectsize

#%%

# Creating simulated data

sample = numpy.random.RandomState(seed = 1234)
samplesize = 100

## Normal (loc = mu, scale = sigma)
gauss_group0 = sample.normal(loc = 1.0, scale = 0.7, size = samplesize).tolist()
gauss_group1 = sample.normal(loc = 1.2, scale = 0.9, size = samplesize).tolist()
gaussian = gauss_group0 + gauss_group1

## Exponential (scale = 1 / lambda)
exp_group0 = sample.exponential(scale = 1/3, size = samplesize).tolist()
exp_group1 = sample.exponential(scale = 1/4, size = samplesize).tolist()
exponential = exp_group0 + exp_group1

## Binomial (n = num trials, p = probability)
bin_group0 = sample.binomial(n = 1, p = 0.2, size = samplesize).tolist()
bin_group1 = sample.binomial(n = 1, p = 0.4, size = samplesize).tolist()
binomial = bin_group0 + bin_group1

## Multinomial (n = num trials, p = probability values)
mult_group0 = sample.multinomial(n = 1, pvals = [2/9, 4/9, 3/9], size = samplesize).tolist()
mult_group1 = sample.multinomial(n = 1, pvals = [3/10, 4/10, 3/10], size = samplesize).tolist()
multinomial = mult_group0 + mult_group1

## Converting results from multinomial samples to integer values

for result in multinomial:
    for i in range(len(result)):
        result[i] = result[i] * (i + 1)

multinomial_int = []

for sample in multinomial:
    multinomial_int.append(max(sample))

## Groups
group = [0]*samplesize + [1]*samplesize

## Weights
weights = numpy.random.RandomState(seed = 1234).normal(loc = 100, scale = 15, size = samplesize*2).tolist()

## Creating Pandas dataframe
df = pandas.DataFrame(list(zip(gaussian, exponential, binomial, multinomial_int, group, weights)),
                      columns = ["var1", "var2", "var3", "var4", "group", "wgt"])

#%%

# Summary statistics

## Continuous
for variable in ["var1", "var2"]:
    print(df.groupby("group")[variable].mean().round(decimals = 2))
    print(df.groupby("group")[variable].std().round(decimals = 2))

## Categorical
for variable in ["var3", "var4"]:
    print(df.groupby("group")[variable].value_counts(sort = False))
    print(df.groupby("group")[variable].value_counts(sort = False, normalize = True))

#%%

# Computing SDs

## Continuous only
effectsize.compute(data = df,
                   group = "group",
                   continuous = ["var1", "var2"])

## Continuous + skew
effectsize.compute(data = df,
                   group = "group",
                   continuous = ["var1", "var2"],
                   skewed = ["var2"])

## Categorical only
effectsize.compute(data = df,
                   group = "group",
                   categorical = ["var3", "var4"])

## ALl variables
effectsize.compute(data = df,
                   group = "group",
                   continuous = ["var1", "var2"],
                   categorical = ["var3", "var4"],
                   skewed = ["var2"])

## All + precision
effectsize.compute(data = df,
                   group = "group",
                   continuous = ["var1", "var2"],
                   categorical = ["var3", "var4"],
                   skewed = ["var2"],
                   decimals = 4)

## All + 95% CIs
effectsize.compute(data = df,
                   group = "group",
                   continuous = ["var1", "var2"],
                   categorical = ["var3", "var4"],
                   skewed = ["var2"],
                   intervals = 0.95)

## All + 99% CIs
effectsize.compute(data = df,
                   group = "group",
                   continuous = ["var1", "var2"],
                   categorical = ["var3", "var4"],
                   skewed = ["var2"],
                   intervals = 0.99)

## All + weights
effectsize.compute(data = df,
                   group = "group",
                   continuous = ["var1", "var2"],
                   categorical = ["var3", "var4"],
                   skewed = ["var2"],
                   weights = "wgt")
# Testing effectsize.compute()

import effectsize

simulation = open("{Insert path to}/simulating_data.py").read()
exec(simulation)

#%% Summary statistics

for variable in ["var1", "var2"]:
    print(df.groupby("group")[variable].mean().round(2))
    print(df.groupby("group")[variable].std().round(1))

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

## All variables
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

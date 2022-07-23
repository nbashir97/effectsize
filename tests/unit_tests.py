# Unit testing individual functions

simulation = open("{Insert path to}/simulating_data.py").read()
functions = open("{Insert path to}/functions.py").read()
exec(simulation)
exec(functions)

#%%

# list_filter()

list_a = ["apple", "banana", "cat", "dog"]
list_b = ["banana", "cat", "dog", "elephant"]
list_c = ["banana", "cat", "frog", "apple"]

## Test 1
list_filter(list1 = list_a, list2 = list_b)

## Test 2
list_filter(list1 = list_a, list2 = list_b)

# compute_intervals()

sd = 0.50 # Setting arbitrary value for effect size

## No weights
compute_intervals(data = df,
                  group = "group",
                  variable = "var1",
                  stdiff = sd)

## With weights
compute_intervals(data = df,
                  group = "group",
                  variable = "var1",
                  stdiff = sd,
                  weights = "wgt")

## Changing precision
compute_intervals(data = df,
                  group = "group",
                  variable = "var1",
                  stdiff = sd,
                  decimals = 4)

## Changing coverage
compute_intervals(data = df,
                  group = "group",
                  variable = "var1",
                  stdiff = sd,
                  coverage = 0.99)

# compute_means()

## No weights
compute_means(data = df,
              group = "group",
              variable = "var1",
              weights = None)

## With weights
compute_means(data = df,
              group = "group",
              variable = "var1",
              weights = "wgt")

# compute_continuous()

## No weights
compute_continuous(data = df,
                   group = "group",
                   variable = "var1")

## With weights
compute_continuous(data = df,
                   group = "group",
                   variable = "var1",
                   weights = "wgt")

## Skewed
compute_continuous(data = df,
                   group = "group",
                   variable = "var1",
                   skewed = True)

## 95% CI
compute_continuous(data = df,
                   group = "group",
                   variable = "var1",
                   intervals = 0.95)

## Changing precision
compute_continuous(data = df,
                   group = "group",
                   variable = "var1",
                   decimals = 4)

# compute_categorical()

## No weights
compute_categorical(data = df,
                    group = "group",
                    variable = "var3")

## With weights
compute_categorical(data = df,
                    group = "group",
                    variable = "var3",
                    weights = "wgt")

## 95% CI
compute_categorical(data = df,
                    group = "group",
                    variable = "var3",
                    intervals = 0.95)

## Changing precision
compute_categorical(data = df,
                    group = "group",
                    variable = "var3",
                    decimals = 4)

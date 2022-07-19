# Example usage on NHANES data

import numpy
import pandas
import effectsize

#%%

nhanes = pandas.read_stata("{Insert path to}/nhanes_cleaned.dta")

# Summarizing

for variable in ["age", "BMI", "cholesterol"]:
    print(nhanes.groupby("smoking")[variable].mean().round(decimals = 2))
    print(nhanes.groupby("smoking")[variable].std().round(decimals = 2))

for variable in ["sex", "ethnicity", "education"]:
    print(nhanes.groupby("smoking")[variable].value_counts(sort = False))
    print(nhanes.groupby("smoking")[variable].value_counts(sort = False, normalize = True))

# Computing SDs

effectsize.compute(data = nhanes,
                   group = "smoking", 
                   continuous = ["age", "BMI", "cholesterol"], 
                   categorical = ["sex", "ethnicity", "education"])

effectsize.compute(data = nhanes,
                   group = "smoking", 
                   continuous = ["age", "BMI", "cholesterol"], 
                   categorical = ["sex", "ethnicity", "education"],
                   skewed = ["BMI"])

effectsize.compute(data = nhanes,
                   group = "smoking", 
                   continuous = ["age", "BMI", "cholesterol"], 
                   categorical = ["sex", "ethnicity", "education"],
                   skewed = ["BMI"],
                   weights = "wtmec2yr")

# Reversing coding for smokers and non-smokers

nhanes["smoking_switched"] = numpy.where(nhanes["smoking"] == 0, 1, 0)

effectsize.compute(data = nhanes,
                   group = "smoking_switched",
                   continuous = ["age", "BMI", "cholesterol"], 
                   categorical = ["sex", "ethnicity", "education"],
                   skewed = ["BMI"],
                   weights = "wtmec2yr")

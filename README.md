# effectsize: computing effect sizes in Python

[![PyPI](https://badge.fury.io/py/effectsize.svg)][pypi]
[![Conda](https://anaconda.org/conda-forge/effectsize/badges/version.svg)][conda]
[![License](https://img.shields.io/github/license/nbashir97/effectsize)][license]

`effectsize` is a comprehensive Python package for computing effect sizes (ESs), also known as standardized differences. The package implements the methodology outlined by [Yang and Dalton (2012)][yang2012] and it provides complex functionality, such as the ability to deal with skewed variables, multinomial categories, and weighted statistics.

## Prerequisites

Before you begin, ensure you have installed Python 3.7 or higher

`effectsize` has four dependencies: [`numpy`][numpy], [`pandas`][pandas], [`scipy`][scipy], [`statsmodels`][statsmodels]

## Installation

Binary installers for the latest released version are available at the [Python Package Index (PyPI)][pypi]:

```sh
pip install effectsize
```

As well as through the conda-forge channel on [Conda][conda]:

```sh
conda install -c conda-forge effectsize
```

Source code for `effectsize` is hosted on its [GitHub repository][repo]

## Usage

To use `effectsize`, it must first be imported as a Python module:

```python
import effectsize
```

From here, all of `effectsize`'s functionality is accessible through a single function named `compute`, which is called via. `effectsize.compute()`. This function takes up to 8 arguments, which are outlined below along with their default values:

```python
effectsize.compute(data,
                   group,
                   continuous = [],
                   categorical = [],
                   skewed = [],
                   weights = None,
                   decimals = 2,
                   intervals = None)
```

Given a `Pandas DataFrame` and a variable specifying 2 groups, `effectsize.compute()` will return another `Pandas DataFrame` containing ESs for all variables that were requested by the user. Detailed description for each argument of `effectsize.compute()` is presented below:

* **data** (`Pandas DataFrame`): Each row should be an observation and each column should be a variable. In other words, all variables for which the user would like to compute an ES must be a column within the DataFrame.
* **group** (`str`): This should be the variable defining the two groups, specified as a string. Ideally, these two groups should be coded as 0 (control) and 1 (treatment), but `effectsize` will work regardless of the coding system used, provided it specifies two groups. Note that if the coding is switched then, the sign of the ES for continuous variables will be reversed, but the magnitude will stay the same. This is typically not an issue as it is the magnitude of the ES which is the most important consideration, and the direction can be inferred from summary statistics, but this may still be worth taking into account if the sign happens to be of particular importance.
* **continuous** (`list`): This should contain the names of all of the continuous variables for which the user would like an ES computed. This must be specified as a list containing the variable names as strings e.g., `continuous = ["age", "salary", "bmi"]` would be syntactically correct but `continuous = [age, salary, bmi]` would not. If there are no continuous variables for which an ES needs to be computed, then **continuous** should be passed an empty list, which is also the default object passed to the argument.
* **categorical** (`list`): This should contain the names of all of the categorical variables for which the user would like an ES computed. In the exact same way as the **continuous** argument, this must be passed a list containing the variable names as strings. If there are no categorical variables for which an ES needs to be computed, then **categorical** should be passed an empty list, which is also the default object passed to the argument.
* **skewed** (`list`): This should contain the names of all of the continuous variables which have a skewed distribution, for which the user would like an ES computed. Note that the skewed variables must be specified in both the **continuous** argument and the **skewed** argument. For example, if age follows a skewed distribution, then this should be specified as `effectsize.compute(continuous = ["age", "salary", "bmi"], skewed = ["age"])`. If this were to be specified as `effectsize.compute(skewed = ["age"])`, then the age variable will simply be ignored and no ES returned. In the exact same way as the **continuous** argument, this must be passed a list containing the variable names as strings. If there are no skewed variables for which an ES needs to be computed, then **skewed** should be passed an empty list, which is also the default object passed to the argument.
* **weights** (`None` or `str`): This should be the variable defining weights, specified as a string (examples of weights include sampling weights or propensity scores). Note that the sum of all of the weights must be >= 1, else the computed ES will not be correct. If there are no weights, then **weights** should be passed the value `None`, which is also the default value passed to the argument.
* **decimals** (`int`): This should be an integer which specifies the number of decimals to which the ESs should be computed, the default value is 2.
* **intervals** (`None` or `float`): This should be a value between 0 and 1 specifying the level of confidence interval (CI) which the user would like e.g., to compute a 95\% CI, this should be specified as `intervals = 0.95`. Note that CIs are rarely required for ESs, and if CIs do not need to be computed then **intervals** should be passed the value `None`, which is also the default value passed to the argument.

`effectsize` excludes all observations for which data is missing on **group** (i.e., it is not clear to which of the 2 groups the observation belongs), or if data is missing on the variable for which the user would like ESs computed (i.e., those in **continuous** and/or **categorical**). Therefore, it is advised that users deal with missing data in the most appropriate manner for their analyses prior to computing ESs.

The order in which the ESs appear in the output of `effectsize.compute()` is the same order in which the variables appear in the `DataFrame` passed to `data`. This is to ensure consistency between the output of `effectsize` and the user's original `DataFrame`. It does not matter in which order users specify the variable names inside of **continuous** and **categorical**, the results will always be output so that they correspond to the same order as the original `DataFrame`.

### Simulation examples

To demonstrate examples of how to use `effectsize`, we simulated 2 groups, each containing 100 observations. In each group, we simulated 4 variables of interest: `var1` is a Normally distributed continuous variable, `var2` is an exponentially ditribusted (i.e., skewed) continuous variable, `var3` is a 2-level categorical variable, and `var4` is a 3-level categorical variable. We used different parameter values to ensure that the distributions of the variables were different between the 2 groups. Summary statistics for the simulated dataset are presented in **Table 1**.

**Table 1.** Summary of simulated data. Continuous variables are presented as mean (standard deviation) and categorical variables are presented as _n_ (%).
|     Variable     |         |   Group 1 (_n_ = 100)  |   Group 2 (_n_ = 100)  |
|:----------------:|:-------:|:----------------------:|:----------------------:|
|       var1       |         |        1.02 (0.7)      |        1.23 (0.9)      |
|       var2       |         |        0.33 (0.3)      |        0.23 (0.2)      |
|       var3       | Level 0 |         82 (82%)       |         58 (58%)       |
|                  | Level 1 |         18 (18%)       |         42 (42%)       |
|       var4       | Level 0 |         29 (29%)       |         35 (35%)       |
|                  | Level 1 |         39 (39%)       |         27 (27%)       |
|                  | Level 2 |         33 (33%)       |         28 (28%)       |

We will assume that the name of the `Pandas DataFrame` in which these data are stored is `df`, and the name of the variable specifying the group to which each observation belongs is named `group`.

To compute ESs for the continuous variables only:

```python
effectsize.compute(data = df,
                   group = "group",
                   continuous = ["var1", "var2"])
```

|      |   ES  |
|:----:|:-----:|
| var1 |  0.26 |
| var2 | -0.31 |

However we know `var2` is skewed, so we may want to account for this:

```python
effectsize.compute(data = df,
                   group = "group",
                   continuous = ["var1", "var2"],
                   skewed = ["var2"])
```

|      |   ES  |
|:----:|:-----:|
| var1 |  0.26 |
| var2 | -0.29 |

We see a small change in the ES for `var2` after accounting for the fact that it is skewed. We can also compute ESs for the categorical variables only:

```python
effectsize.compute(data = df,
                   group = "group",
                   categorical = ["var3", "var4"],)
```

|      |   ES  |
|:----:|:-----:|
| var3 |  0.54 |
| var4 |  0.16 |

Finally, if we wish to compute ESs for all variables at once:

```python
effectsize.compute(data = df,
                   group = "group",
                   continuous = ["var1", "var2"],
                   categorical = ["var3", "var4"],
                   skewed = ["var2"])
```

|      |   ES  |
|:----:|:-----:|
| var1 |  0.26 |
| var2 | -0.29 |
| var3 |  0.54 |
| var4 |  0.16 |

Obtraining extra precision is also straightforward:

```python
effectsize.compute(data = df,
                   group = "group",
                   continuous = ["var1", "var2"],
                   categorical = ["var3", "var4"],
                   skewed = ["var2"],
                   decimals = 4)
```

|      |    ES   |
|:----:|:-------:|
| var1 |  0.2566 |
| var2 | -0.2934 |
| var3 |  0.5427 |
| var4 |  0.1580 |

Conifdence intervals are easily computed, in this case 95% CIs:

```python
effectsize.compute(data = df,
                   group = "group",
                   continuous = ["var1", "var2"],
                   categorical = ["var3", "var4"],
                   skewed = ["var2"],
                   intervals = 0.95)
```

|      |   ES  |    95.0% CI    |
|:----:|:-----:|:--------------:|
| var1 |  0.26 |  [-0.02, 0.54] |
| var2 | -0.29 | [-0.57, -0.01] |
| var3 |  0.54 |  [0.26, 0.82]  |
| var4 |  0.16 |  [-0.12, 0.44] |

Similarly, for 99% CIs:

```python
effectsize.compute(data = df,
                   group = "group",
                   continuous = ["var1", "var2"],
                   categorical = ["var3", "var4"],
                   skewed = ["var2"],
                   intervals = 0.99)
```

|      |   ES  |    99.0% CI   |
|:----:|:-----:|:-------------:|
| var1 |  0.26 | [-0.11, 0.63] |
| var2 | -0.29 | [-0.66, 0.08] |
| var3 |  0.54 |  [0.17, 0.91] |
| var4 |  0.16 | [-0.20, 0.52] |

We then create simulated weights for the observations by taking 200 samples from a Normal distribution with mean = 100 and standard deviation = 15. The variable containing the weights is named `wgt`, and we can compute a weighted ES by specifying this in the function call:

```python
effectsize.compute(data = df,
                   group = "group",
                   continuous = ["var1", "var2"],
                   categorical = ["var3", "var4"],
                   skewed = ["var2"],
                   weights = "wgt")
```

|      |   ES  |
|:----:|:-----:|
| var1 |  0.15 |
| var2 | -0.29 |
| var3 |  0.53 |
| var4 |  0.15 |

### Empirical examples

To demonstrate use on a real-world example, we use data from the 2017-2018 [National Health and Nutrition Examination Survey (NHANES)][nhanes], a cross-sectional study which samples the noninstitutionalized US population. Participants are first interviewed at home and then invited to a mobile examination center for further interviews, tests, and examinations. We will use data from NHANES to evaluate differences between smokers versus non-smokers, across 6 variables: 

* Age (in years)
* Sex (male / female)
* Ethnicity (White / Black / Hispanic / Other)
* Education (below high school / high school graduate / college graduate) 
* BMI (in kilograms per square metre)
* Blood cholesterol (in milligrams per deciliter)

Age, BMI, and blood cholesterol were measured as continuous variables, whilst sex, ethnicity, and education were measured as categorical variables. Summary statistics for the distribution of the variables amongst smokers and non-smokers are presented in **Table 2**.

**Table 2.** Summary of NHANES data. Continuous variables are presented as mean (standard deviation) and categorical variables are presented as _n_ (%).
|             |                      | Non-smokers (_n_ = 3981)  | Smokers (_n_ = 870) |
|:-----------:|:--------------------:|:-------------------------:|:-------------------:|
|     Age     |                      |        52.2 (17.9)        |     47.5 (15.6)     |
|     Sex     |         Male         |        1836 (46.1%)       |     495 (56.9%)     |
|             |        Female        |        2145 (53.9%)       |     375 (43.1%)     |
|  Ethnicity  |         White        |        1334 (33.5%)       |     371 (42.6%)     |
|             |         Black        |        841 (21.1%)        |     254 (29.2%)     |
|             |       Hispanic       |        999 (25.1%)        |     124 (14.3%)     |
|             |         Other        |        807 (20.3%)        |     121 (13.9%)     |
|  Education  |   Below high school  |        751 (18.9%)        |     205 (23.6%)     |
|             | High school graduate |        2155 (54.1%)       |     580 (66.7%)     |
|             |   College graduate   |        1075 (27.0%)       |      85 (9.8%)      |
|     BMI     |                      |         30.0 (7.3)        |      29.2 (7.8)     |
| Cholesterol |                      |        188.0 (40.8)       |     189.6 (43.5)    |

We will assume that the name of the `Pandas DataFrame` in which these data are stored is `nhanes`, and the name of the variable specifying whether indivduals are smokers or non-smokers is named `smoking`.

To compute ESs for all variables:

```python
effectsize.compute(data = nhanes, 
                   group = "smoking",
                   continuous = ["age", "BMI", "cholesterol"],
                   categorical = ["sex", "ethnicity", "education"])
```

|             |   ES  |
|:-----------:|:-----:|
|     age     | -0.28 |
|     sex     |  0.22 |
|  ethnicity  |  0.37 |
|  education  |  0.46 |
|     BMI     | -0.12 |
| cholesterol |  0.04 |

On further investigation, we may find that BMI is not distributed symmetrically and want to account for this:

```python
effectsize.compute(data = nhanes, 
                   group = "smoking",
                   continuous = ["age", "BMI", "cholesterol"],
                   categorical = ["sex", "ethnicity", "education"],
                   skewed = ["BMI"])
```

|             |   ES  |
|:-----------:|:-----:|
|     age     | -0.28 |
|     sex     |  0.22 |
|  ethnicity  |  0.37 |
|  education  |  0.46 |
|     BMI     | -0.15 |
| cholesterol |  0.04 |

In NHANES, probability sampling weights are used and stored in a variable named `wtmec2yr`. If we wish to account for these sampling weights:

```python
effectsize.compute(data = nhanes, 
                   group = "smoking",
                   continuous = ["age", "BMI", "cholesterol"],
                   categorical = ["sex", "ethnicity", "education"],
                   skewed = ["BMI"],
                   weights = "wtmec2yr")
```

|             |   ES  |
|:-----------:|:-----:|
|     age     | -0.32 |
|     sex     |  0.11 |
|  ethnicity  |  0.17 |
|  education  |  0.56 |
|     BMI     | -0.18 |
| cholesterol |  0.02 |

The level of precision and CIs can be modified within the `decimals` and `intervals` arguments, as demonstrated in earlier simulation examples.

Finally, to demonstrate the effect of how the group coding, we switched how smokers and non-smokers were coded. In the examples above, smokers were coded as 1 and non-smokers as 0. We now re-run the final example from above, but having switched smokers to 0 and non-smokers to 1:

```python
effectsize.compute(data = nhanes, 
                   group = "smoking_switched",
                   continuous = ["age", "BMI", "cholesterol"],
                   categorical = ["sex", "ethnicity", "education"],
                   skewed = ["BMI"],
                   weights = "wtmec2yr")
```

|             |   ES  |
|:-----------:|:-----:|
|     age     |  0.32 |
|     sex     |  0.11 |
|  ethnicity  |  0.17 |
|  education  |  0.56 |
|     BMI     |  0.18 |
| cholesterol | -0.02 |

We see that the magnitude of the ESs has remained unchanged, but the direction for the continuous variables has reversed. By referring to **Table 2**, we can see that the smokers tend to be younger, have a lower BMI, and have a higher blood cholesterol. Therefore, if smokers are our reference group, then we would expect the ESs for age and BMI to be negative, whilst the ES for cholesterol would be positive. However, if we were to take non-smokers as our reference group, then we would expect the ESs for age and BMI to be positive, whilst the ES for cholesterol would be negative, explaining the change in sign of the ESs in the above example. ESs for the categorical variables are always positive as computing them involves taking squares of matrices, which will yield positive values. 

## Contributing

Users are actively encouraged to test and implement `effectsize` in their projects, as well as leave feedback and make contributions to the packages. In particular, we welcome contributions relating to improving computational efficiency, adding features which are likely to be widely used, and developing the unerlying mathematical theory. Users can [fork the software][forking] and [create pull requests][pulling] on GitHub, or get in touch regarding any relevant developments in statistical theory.

## Contact

If you wish to contact me you can reach me at nbashir562@gmail.com

## License

[MIT License][license]

[pypi]: https://pypi.org/project/effectsize/
[conda]: https://anaconda.org/conda-forge/effectsize
[license]: https://github.com/nbashir97/effectsize/blob/main/LICENSE.md
[yang2012]: https://www.semanticscholar.org/paper/A-unified-approach-to-measuring-the-effect-size-two-Yang-Dalton/6cf4bd36ca4c90006a5d6563f646a391c255581b
[numpy]: https://numpy.org/
[pandas]: https://pandas.pydata.org/
[scipy]: https://scipy.org/
[statsmodels]: https://www.statsmodels.org/stable/index.html
[repo]: https://github.com/nbashir97/effectsize
[nhanes]: https://www.cdc.gov/nchs/nhanes/index.htm
[pulling]: https://help.github.com/en/github/collaborating-with-issues-and-pull-requests/creating-a-pull-request
[forking]: https://docs.github.com/en/get-started/quickstart/fork-a-repo

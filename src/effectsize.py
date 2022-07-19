import pandas
from functions import list_filter, compute_continuous, compute_categorical
# Note that in the function documentation the term standardized difference (SD) is preferred over effect size; both terms have the same meaning

#%%

def compute(data,
            group,
            continuous = [],
            categorical = [],
            skewed = [],
            weights = None,
            decimals = 2,
            intervals = None):
    
    """
    
    Computes SDs for all specified variables
    
    Parameters:
        data (dataframe): Pandas DataFrame containing observations (rows) and variables (columns)
        exposure (str): Variable defining the two groups
        continuous (list): List of string items which are names of the continuous variables for which the SD should be computed
        categorical (list): List of string items which are names of the categorical variables for which the SD should be computed
        skewed (list): List of string items which are names of the continuous variables which have a skewed distribution (ranked SD computed)
        weights (None or str): Variable defining weights for each observation (otherwise assumed to be equally weighted)
        decimals (int): Number of decimal places which should be computed
        intervals (None or float): Whether CIs should be computed and with what coverage e.g. for 95% CI, intervals = 0.95
    
    Returns:
        Pandas DataFrame containing the computed SDs (and CIs, if specified)

    """
      
    # Asserting input types
    
    assert type(data) == pandas.DataFrame or type(data) == pandas.core.frame.DataFrame, "Data must be specified as a Pandas DataFrame"        
    assert type(group) == str, "Group variable must be specified as a string"
    assert type(continuous) == list and type(categorical) == list and type(skewed) == list, "Variable names must be specified inside lists"
    assert weights == None or type(weights) == str, "If weight variable is present, it must be specified as a string"
    assert type(decimals) == int, "Number of decimal places must be specified as an integer"
    assert intervals == None or (intervals > 0 and intervals < 1), "CIs must be specified as None or in range (0,1) e.g. for 95% CI, intervals = 0.95"
        
    # Get combined list of variables and sort them into the order in which they appear in the dataframe
    
    specified_variables = (continuous + categorical).copy()
    all_variables = list(data)
    
    for variable in specified_variables:
        assert type(variable) == str, "The variable names inside lists must all be specified as strings"
        if variable not in all_variables: 
            print("The following variable was not computed as it could not be found in dataframe columns:", variable)        
    
    ordered_variables = list_filter(list1 = all_variables, list2 = specified_variables)
    
    # Computing the standardized difference
    
    results = []
    
    for variable in ordered_variables:

        if variable in continuous:
            
            if variable in skewed:
                
                stdiff = compute_continuous(data = data,
                                            group = group,
                                            variable = variable,
                                            skewed = True,
                                            weights = weights,
                                            decimals = decimals,
                                            intervals = intervals)
                
                results.append(stdiff)
                
            else:
                
                stdiff = compute_continuous(data = data,
                                            group = group,
                                            variable = variable,
                                            skewed = False,
                                            weights = weights,
                                            decimals = decimals,
                                            intervals = intervals)
                
                results.append(stdiff)
        
        else:
            
            stdiff = compute_categorical(data = data,
                                         group = group, 
                                         variable = variable,
                                         weights = weights,
                                         decimals = decimals,
                                         intervals = intervals)
            
            results.append(stdiff)
    
    results = pandas.DataFrame(data = results)
    results.set_axis([ordered_variables], axis = 0, inplace = True)
    
    # Computing the CIs
    
    if intervals == None:
        
        results.set_axis(['ES'], axis = 1, inplace = True)
    
    else:
        
        ci_label = round(( intervals * 100 ), ndigits = 2)
        results.set_axis(['ES', str(ci_label) + '% CI'], axis = 1, inplace = True)     
    
    return results
import numpy
import scipy
import pandas
from statsmodels.stats.weightstats import DescrStatsW
# Note that in the function documentation the term standardized difference (SD) is preferred over effect size; both terms have the same meaning

#%%

def list_filter(list1,
                list2):
    
    """
    
    Returns a list containing the common elements between the two passed lists
    Maintains the order of list1, but ensures it only has the elements from list2
       
    Parameters:
        list1 (list): First list to be compared
        list2 (list): Second list to be compared
    
    Returns:
        List containing the common elements of list1 and list2 
        
    """    
    
    # Copying list1 so there are no issues with simulatenous indexing and removal of items
    
    filtered_list = list1.copy()
    
    for variable in list1:
        
        if variable not in list2:
            
            filtered_list.remove(variable)
        
    return filtered_list

#%%

def compute_intervals(data,
                      group,
                      variable,
                      stdiff, 
                      weights = None,
                      decimals = 2,
                      coverage = 0.95):
        
    """
    
    Constructs two-sided confidence intervals for SDs
       
    Parameters:
        data (dataframe): Pandas DataFrame containing observations (rows) and variables (columns)
        group (str): Variable defining the two groups
        variable (str): Variable to be compared across exposed and unexposed
        stdiff (float): The SD between exposed and unexposed for the given covariate
        decimals (int): Number of decimal places which should be computed
        coverage (float): Value in range (0,1) specfiying coverage of confidence interval e.g. for 95% CI, intervals = 0.95
    
    Returns:
        List in the format: [upper CI, lower CI] 
        
    """
    
    data = data.dropna(axis = 0, subset = [group, variable])
        
    if weights == None:
        
        # Number of observations in group 1, group 0, and total
    
        n0 = data.groupby(group).size()[0]
        n1 = data.groupby(group).size()[1]
    
        total = n0 + n1
    
    else:
        
        # Sum of weights in group 1, group 0, and total
        
        data = data.dropna(axis = 0, subset = [weights])
    
        n0 = data.groupby(group)[weights].sum()[0]
        n1 = data.groupby(group)[weights].sum()[1]
    
        total = n0 + n1
        
    # Computing the corresponding value from the standard Normal for specified CI coverage
    
    percentile = 1 - ((1 - coverage) / 2)
    zscore = scipy.stats.norm.ppf(percentile)
    
    # Computing the standard deviation
    
    deviation = numpy.sqrt( (total / (n0 * n1)) + ((stdiff ** 2) / (2 * total)) )
    
    # Constructing the CIs using the Z-score and standard deviation
    
    lower_ci = stdiff - zscore * deviation
    upper_ci = stdiff + zscore * deviation
        
    lower_ci = lower_ci.round(decimals)
    upper_ci = upper_ci.round(decimals)
    
    return [lower_ci, upper_ci]

#%%

def compute_means(data,
                  group,
                  variable,
                  weights):

    """
    
    Computes mean and variance for continuous variables, conditional on group
       
    Parameters:
        data (dataframe): Pandas DataFrame containing observations (rows) and variables (columns)
        group (str): Variable defining the two groups
        variable (str): Variable to be compared across the two groups
        weights (None or str): Variable defining weights for each observation (otherwise assumed to be equally weighted)
    
    Returns:
        List in the format: [group 0 mean, group 1 mean, group 0 variance, group 1 variance]
        
    """
    
    data = data.dropna(axis = 0, subset = [group, variable])
    
    if weights == None:
        
        # Mean and variance in group 1, group 0, and total
        
        mean0 = data.groupby(by = group, axis = 0)[variable].mean()[0]
        mean1 = data.groupby(by = group, axis = 0)[variable].mean()[1]
        
        variance0 = data.groupby(by = group, axis = 0)[variable].var(ddof = 1)[0]
        variance1 = data.groupby(by = group, axis = 0)[variable].var(ddof = 1)[1]
        
        return [mean0, mean1, variance0, variance1]
    
    else:
        
        # Extracting variable values and weights for statsmodels
        
        data = data.dropna(axis = 0, subset = [weights])
        
        vals0 = numpy.asarray(data.groupby(by = group, axis = 0)[variable].apply(list)[0])
        wgts0 = numpy.asarray(data.groupby(by = group, axis = 0)[weights].apply(list)[0])
        df0 = pandas.DataFrame({'vals0': vals0, 'wgts0': wgts0})
        
        vals1 = numpy.asarray(data.groupby(by = group, axis = 0)[variable].apply(list)[1])
        wgts1 = numpy.asarray(data.groupby(by = group, axis = 0)[weights].apply(list)[1])
        df1 = pandas.DataFrame({'vals1': vals1, 'wgts1': wgts1})
        
        d0 = DescrStatsW(data = df0['vals0'].to_numpy(), weights = df0['wgts0'].to_numpy())
        d1 = DescrStatsW(data = df1['vals1'].to_numpy(), weights = df1['wgts1'].to_numpy())
        
        # Weighted mean and variance in group 1, group 0, and total
        
        mean0 = d0.mean
        mean1 = d1.mean
        
        variance0 = d0.var_ddof(ddof = 1)
        variance1 = d1.var_ddof(ddof = 1)
        
        return [mean0, mean1, variance0, variance1]

#%%

def compute_continuous(data,
                       group,
                       variable,
                       skewed = False, 
                       weights = None,
                       decimals = 2,
                       intervals = None):
    
    """
    
    Computes SD for continuous variables
       
    Parameters:
        data (dataframe): Pandas DataFrame containing observations (rows) and variables (columns)
        group (str): Variable defining the two groups
        variable (str): Variable to be compared across the two groups
        skewed (list): List of string items which are names of the continuous variables which have a skewed distribution (ranked SD computed)
        weights (None or str): Variable defining weights for each observation (otherwise assumed to be equally weighted)
        decimals (int): Number of decimal places which should be computed
        intervals (None or float): Whether CIs should be computed and with what coverage e.g. for 95% CI, intervals = 0.95
    
    Returns:
        Computed SD or list containing SD and CI, if requested
        
    """
           
    if weights == None:
        subset = data[[group, variable]]
    else:
        subset = data[[group, variable, weights]]
              
    if skewed == False:
        results = compute_means(data = subset, group = group, variable = variable, weights = weights)
    else:
        ranks = subset[variable].rank(axis = 0, method = 'average', na_option = 'keep', ascending = True)
        subset = subset.assign(ranks = ranks)
        results = compute_means(data = subset, group = group, variable = 'ranks', weights = weights)
    
    mean0 = results[0]
    mean1 = results[1]
    variance0 = results[2]
    variance1 = results[3]
    
    # Computing the standardized difference
    
    stdiff = (mean1 - mean0) / numpy.sqrt((variance0 + variance1) / 2) 
    stdiff = stdiff.round(decimals)   
    
    # Computing the CIs
    
    if intervals == None:
        
        return stdiff
    
    else:
        
        ci = compute_intervals(data = data, group = group, variable = variable, stdiff = stdiff,
                               weights = weights, decimals = decimals, coverage = intervals)
        
        return stdiff, ci
    
#%%

def compute_categorical(data,
                        group,
                        variable,
                        weights = None,
                        decimals = 2,
                        intervals = None):
    
    """
    
    Computes SD for categorical variables
    
    Parameters:
        data (dataframe): Pandas DataFrame containing observations (rows) and variables (columns)
        group (str): Variable defining the two groups
        variable (str): Variable to be compared across the two groups
        weights (None or str): Variable defining weights for each observation (otherwise assumed to be equally weighted)
        decimals (int): Number of decimal places which should be computed
        intervals (None or float): Whether CIs should be computed and with what coverage e.g. for 95% CI, intervals = 0.95
    
    Returns:
        Computed SD or list containing SD and CI, if requested
    
    """
    
    data = data.dropna(axis = 0, subset = [group, variable])    
    
    if weights == None:
        
        # Computing the probability matrix for each level of the categorical variable, conditional on group
        
        group0 = data.groupby(by = group, axis = 0)[variable].value_counts(normalize = True, sort = False)[0].to_frame().to_numpy()
        group1 = data.groupby(by = group, axis = 0)[variable].value_counts(normalize = True, sort = False)[1].to_frame().to_numpy()
        
    else:
        
        # Computing the weighted probability matrix for each level of the categorical variable, conditional on group
        
        data = data.dropna(axis = 0, subset = [weights])
        grouped = data.groupby(by = [group, variable], axis = 0, dropna = True)[weights].sum().to_frame()
        n_rows = grouped.shape[0]

        group0 = grouped.head(int(n_rows/2))[weights].to_frame()
        group0 = group0[weights].div(group0[weights].sum()).to_frame().to_numpy()

        group1 = grouped.tail(int(n_rows/2))[weights].to_frame()
        group1 = group1[weights].div(group1[weights].sum()).to_frame().to_numpy()
    
    prob_matrix = numpy.concatenate((group1, group0), axis = 1)
    
    # Computing the  probability difference between group 1 and group 0
    # Dropping the 1st difference as there are n-1 degrees of freedom

    prob_difference = numpy.subtract(group1, group0)
    prob_difference = numpy.delete(prob_difference, (0), axis = 0)

    # Computing the covariance matrix
    
    levels = prob_matrix.shape[0]
    covariance = numpy.zeros(shape = (levels, levels))
    
    for row in range(levels):
        
        for col in range(levels):
            
            if row == col: 
                
                covariance[row][col] = ( prob_matrix[row][0] * (1 - prob_matrix[row][0]) + prob_matrix[row][1] * (1 - prob_matrix[row][1]) ) / 2 
            
            else: 
                
                covariance[row][col] = -( prob_matrix[row][0] * prob_matrix[col][0] + prob_matrix[row][1] * prob_matrix[col][1] ) / 2
    
    # Dropping the 1st line and row as there are n-1 degrees of freedom
    # Computing the inverse of the covariance matrix
        
    covariance = numpy.delete(covariance, (0), axis = 0)
    covariance = numpy.delete(covariance, (0), axis = 1)
    
    inverse = numpy.linalg.inv(covariance)
    
    # Computing the standardized difference (using Mahalanobis distance)
    
    stdiff = numpy.sqrt(numpy.linalg.multi_dot([prob_difference.T, inverse, prob_difference]))
    stdiff = stdiff[0][0]
    stdiff = stdiff.round(decimals)  
    
    # Computing the CIs
    
    if intervals == None:
        
        return stdiff
    
    else:
        
        ci = compute_intervals(data = data, group = group, variable = variable, stdiff = stdiff, 
                               weights = weights, decimals = decimals, coverage = intervals)
        
        return stdiff, ci
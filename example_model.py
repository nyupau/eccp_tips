import numpy as np
import pandas as pd
# ...

def predict(data):
    
    ordered_columns = [] #...

    # Load ... 
    
    ## PAU update: compute a 0/1 col to hide scores for A/B testing
    # helper function to add robustness for different Z and E prefixed strings. 
    dataframe['mod'] = (dataframe['ID'].apply(lambda x: coerce_ID_to_int(x)) % 2)
    dataframe['to_hide_bool'] = dataframe['mod'] == 1
    # can be replaced with any function/logic that returns a boolean column

    # Transform ... 
    
    # Predict ...
    # use helper function to predict probabilities and contributions
    scores, contributions = predict_df() #...
    
    ## PAU update
    # masking any randomized scores
    #warnings.warn("Hiding {} scores from {}.".format(copy['to_hide_bool'].sum(), len(copy)))
    score_masked = []
    for to_hide, score, eligible in zip(dataframe['a'], dataframe['b'], dataframe['c']):
        # tiered logic, if Hidden ALWAYS return hidden, even if missing data for ex
        if to_hide: # if assigned to hide, return string 
            score_masked.append("Hidden")
        else: 
            if np.isnan(score): # if failed to estimate score due to missing data, replace with string
                score_masked.append("Missing data") 
            elif eligible: ## allow score but flip and round to 2 d.p.
                #score_masked.append(str(np.round(score, 2))) ## UNFLIPPED
                score_masked.append(str(np.round(100 - score, 2))) ## FLIP scores
            else: ## shouldn't get here, return None for tracing
                score_masked.append(None)
    
    ## PAU update: scale contributions by absolute sum but keep positive and negative signs
    total_contribution = contributions.abs().sum(axis=1, skipna=False)
    contributions_normed = pd.DataFrame()
    for key in contributions.columns:
        #contributions_normed[key] = np.round((contributions[key] / total_contribution) * 100, 2) ## UNFLIPPED
        contributions_normed[key] = np.round(0 - ((contributions[key] / total_contribution) * 100), 2) ## FLIP IT
    # each row does not sum to 100, but the absolute values do.
    
    ## PAU update: limit to NINE largest features of either sign for simple display
    # helper function
    contributions_out = restrict_to_top_nine(contributions_normed)
    
    ## PAU update: masking all contributions for any randomized scores
    for to_hide, i in zip(copy['to_hide_bool'], range(contributions_out.shape[0])):
        if to_hide:
            contributions_out.loc[i, :] = 0 ## whole row 0s.
    
    # Return ...
    return_value = {} #...
    print("Done!")
    return return_value

#...

#### PAU helper functions ----
    
def restrict_to_top_nine(df):
    """
    Take a input df of contributions and, by row, omit all contributions except the absolute largest nine, keeping original signs. 
    """
    out = df.copy()
    for i in range(df.shape[0]):
        temp = out.columns ## init as full columns as set difference below becomes empty, nothing is changed.
        temp = out.iloc[i, :].abs().sort_values(ascending = False)[0:9].index ## TOP 9!
        if len(temp) == 9: ## sanity check, skip if something fails
            ## set values for all columns except those top 9, to 0
            out.loc[i, out.columns.difference(temp)] = 0
    return out

def coerce_ID_to_int(x):
    """
    Take a patient ID, x, and try to find an integer stripping characters present in several common formats.
    """
    if type(x) == float and np.isnan(x):
        return 0
    if type(x) == float or type(x) == int:
        return int(x)
    if x == "None" or not x:
        return 0
    if '<' in x:
        x = x.replace("<", "")
        x = x.replace(">", "")
    if 'Z' in x:
        x = x.replace("Z", "")
    if 'E' in x:
        x = x.replace("E", "")
    try: 
        return int(x)
    except:
        warnings.warn("failed to parse ID: {}, assigning 0".format(x))
        return 0

# print(coerce_ID_to_int(12345))     ## 12345
# print(coerce_ID_to_int('12345'))   ## 12345
# print(coerce_ID_to_int(-1)) ## -1
# print(coerce_ID_to_int('-1')) ## -1
# print(coerce_ID_to_int('E<12345>'))## 012345
# print(coerce_ID_to_int('<E12345>'))## 12345
# print(coerce_ID_to_int('<12345>')) ## 12345
# print(coerce_ID_to_int('E<12345')) ## 12345
# print(coerce_ID_to_int('Z<12345>'))## 12345
# print(coerce_ID_to_int('Z12345'))  ## 12345
# print(coerce_ID_to_int('E12345'))  ## 12345
# print(coerce_ID_to_int('foobar'))  ## triggers warning, returns 0
# print(coerce_ID_to_int(np.nan))  ## returns 0, no warning.
import numpy as np
from scipy import stats, linalg

def partial_corr(C):
    """
    Code source: https://gist.github.com/fabianp/9396204419c7b638d38f
    
    Adpoted from Matlab's partialcorr
    Uses the linear regression approach to compute the partial correlation,
    algorithms detailed here: http://en.wikipedia.org/wiki/Partial_correlation#Using_linear_regression
    
    --- Summary:
    Taking two variables of interest: X & Y, and the Z matrix with all the variables minus {X, Y}, 
    the algorithm:
    
    1) performs a normal linear least-squares regression with X as the target and Z as the predictor
    2) calculates the residuals in step #1
    3) performs a normal linear least-squars regression with Y as the target and Z as the predictor
    4) calcualtes the residuals in step #3
    5) calculates the correlation coefficient between the residuals from step #2 & step #4
    6) results give you the partial correlation between X & Y while controlling for the effect of Z
    
    --- Parameters:
    C: array-like, shape (n, p)
       Array with the different variables - can be a pandas dataframe
       Each column of C is taken as a variable.
    
    --- Returns:
    P: array-like, shape (p, p)
       p[i, j] contains the partial correlation of C[:, i] and C[:, j]
       while controlling for the remaining variables in C
    """
    
    C = np.asarray(C)
    p = C.shape[1]
    p_corr = np.zeros((p, p), dtype=np.float)
    for i in range(p):
        p_corr[i, i] = 1
        for j in range(i+1, p):
            idx = np.ones(p, dtype=np.bool)
            idx[i] = False
            idx[j] = False
            beta_i = linalg.lstsq(C[:, idx], C[:, j])[0]
            beta_j = linalg.lstsq(C[:, idx], C[:, i])[0]
            
            res_j = C[:, j] - C[:, idx].dot(beta_i)
            res_i = C[:, i] - C[:, idx].dot(beta_j)
            
            corr = stats.pearsonr(res_i, res_j)[0] # might want to switch this to Spearman
            p_corr[i, j] = corr
            p_corr[j, i] = corr # this line is just to mirrow the results to fill out whole matrix
    
    
    return p_corr
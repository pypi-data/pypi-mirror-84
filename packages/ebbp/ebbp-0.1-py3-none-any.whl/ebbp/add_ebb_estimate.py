"""
one function that fits the prior from data and augments the estimates in the dataframe
"""

import numpy as np
import pandas as pd

from .ebb_fit_prior import ebb_fit_prior as fit, augment


def add_ebb_estimate(x, n, data, method = 'mm'):
    
    # get the estimate and the CIs
    est = fit(x, n, method)
    
    # augment it with the data
    return augment(est, data, x, n)
    
    pass


if __name__ == '__main__':
    x = np.random.randint(0,100,100)
    n = 100
    p = x/n
    dt = pd.DataFrame({'S':x, 'Tot': n, 'est':p})
    
    aug_df = add_ebb_estimate(dt.S, dt.Tot, dt, method = 'mm')
    print(aug_df.head(10))
    
   

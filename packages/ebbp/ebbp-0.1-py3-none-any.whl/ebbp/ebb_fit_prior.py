"""
ebb_fit_prior : fits a Beta prior by estimating the parameters from the data using 
method of moments and MLE estimates
augment : given data and prior, computes the shrinked estimate, credible intervals and 
augments those in the given dataframe
check_fit : plots the true average and the shrinked average

"""

import numpy as np     
import pandas as pd
from scipy.stats import beta as beta_dist

from dataclasses import dataclass

import matplotlib.pyplot as plt


@dataclass
class Beta:
    """ minimal Beta class, for prior and posterior objects"""
    alpha: float
    beta: float
    
    def pdf(self, x):
        return beta_dist.pdf(x, self.alpha, self.beta)
        pass
    
        
    def plot(self, x, n):
        """ plots the prior pdf density over the data histogram"""
        # add various plotting args
        x_ax = np.linspace(0,1,1000)
        rv = beta_dist(self.alpha, self.beta)
        p = x/n
        plt.hist(p, density = True)
        plt.plot(x_ax, rv.pdf(x_ax))
        plt.title(f'Beta({self.alpha.round(2)},{self.beta.round(2)})')
        plt.show()
           
    
    
    
def ebb_fit_prior(x, n, method = 'mm', start = (0.5,0.5)):
    p = x/n
    if (method == 'mm'):
        mu, sig = np.mean(p), np.var(p)
        a = ((1-mu)/sig - 1/mu)*mu**2
        b = a*(1/mu - 1)
        
        fitted_prior = Beta(a,b)
                
        pass
    elif (method == 'mle'):
        
        # starting value
        # if (np.isnan(start)):
        #     mm_est = ebb_fit_prior(x, n, 'mm')
        #     start = (mm_est.alpha, mm_est.beta)
        #     #print(start)
        
        # likelihood function: f(a, b)
        def likelihood(pars):
            return (-np.sum(beta_dist.pdf(p, pars[0], pars[1])))
            
        
        # optimization function: over a series of params, optimise likelihood
        # outp = minimize(likelihood, x0 = start, method = 'BFGS')
        # fitted_prior = Beta(outp.x[0], outp.x[1])
        
        a,b,*ls = beta_dist.fit(p)
        fitted_prior = Beta(a,b)
        pass
    else:
        return ('Method should be MM or MLE')
    
    return fitted_prior
    
    
    pass 


def augment(prior, data, x, n):
    
    # compute the estimates 
    post_alpha = prior.alpha + x
    post_beta = prior.beta + n - x 
    
    eb_est = (x + prior.alpha)/(n + prior.alpha + prior.beta)
    
    posterior = Beta(post_alpha, post_beta)
    
    # compute the posterior credible intervals 
    post_l = beta_dist.ppf(0.025, posterior.alpha, posterior.beta)
    post_u = beta_dist.ppf(0.975, posterior.alpha, posterior.beta)
    
    # add the column
    new_cols = pd.DataFrame({'alpha':post_alpha, 'beta': post_beta, 'eb_est': eb_est, 'cred_lower': post_l, 'cred_upper':post_u})
    aug_df = pd.concat([data, new_cols], axis = 1)
    
    return aug_df

    pass


    
def check_fit(aug_df):
    plt.plot(aug_df.est, aug_df.eb_est)
    plt.show()

if __name__ == '__main__':  
    x = np.random.randint(0,50,20)
    n = np.random.randint(50,100, 20)
    p = x/n
    dt = pd.DataFrame({'S':x, 'Tot':n, 'est':p})
        
    est1 = ebb_fit_prior(x,n, 'mm')
    print(est1)
    est1.plot(x, n)
    
    new_dt = augment(est1, dt, dt.S, dt.Tot)
    print(new_dt.head(10))
    check_fit(new_dt)
       
    print('=============================')
    est2 = ebb_fit_prior(x,n,'mle')
    print(est2)
    est2.plot(x,n)
    new_dt = augment(est2, dt, dt.S, dt.Tot)
    print(new_dt.head(10))
    check_fit(new_dt)
    


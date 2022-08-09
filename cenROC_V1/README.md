# censoredROC

This function computes the time-dependent ROC curve for right censored survival data using the cumulative sensitivity and dynamic specificity definitions. The ROC curves can be either empirical (non-smoothed) or smoothed with/wtihout boundary correction. It also calculates the time-dependent area under the ROC curve (AUC).

This package was built taken the cenROC package in R (https://cran.rstudio.com/web/packages/cenROC/index.html) as a main reference. The main idea was to allow Python users to apply the same tools.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites

___cenroc___ requires following packages to be installed 

```
['numpy', 'pandas', 'matplotlib', 'scipy','statsmodels']
```
if you don't have them installed ___cenroc___ will install the latest versions of these packages on your machine

### Installing

Use the following command to install the ___cenroc___ package from PyPi

```
pip install cenroc
```

## Main class

The main class of this package is __cenROC__

In order to use the methods you have to intialise this class

__cenROC(Y, M, censor, t, U = NULL, h = NULL, bw = "NR", method = "tra",
    ktype = "normal", ktype1 = "normal", B = 0, alpha = 0.05, plot = "TRUE")__


## Arguments 

__Y__

The numeric vector of event-times or observed times.

__M__

The numeric vector of marker values for which the time-dependent ROC curves is computed.

__censor__

The censoring indicator, 1 if event, 0 otherwise.

__t__

A scaler time point at which the time-dependent ROC curve is computed.

__U__

The vector of grid points where the ROC curve is estimated. The default is a sequence of 151 numbers between 0 and 1.

__h__

A scaler for the bandwidth of Beran's weight calculaions. The defualt is the value obtained by using the method of Sheather and Jones (1991).

__bw__

A character string specifying the bandwidth estimation method for the ROC itself. The default is the "NR" normal reference method. The user can also introduce a numerical value.

__method__

The method of ROC curve estimation. The possible options are "emp" emperical metod; "untra" smooth without boundary correction and "tra" is smooth ROC curve estimation with boundary correction. The default is the "tra" smooth ROC curve estimate with boundary correction.

__ktype__

A character string giving the type kernel distribution to be used for smoothing the ROC curve: "normal", "epanechnikov", "biweight", or "triweight". By default, the "normal" kernel is used.

__ktype1__

A character string specifying the desired kernel needed for Beran weight calculation. The possible options are "normal", "epanechnikov", "tricube", "boxcar", "triangular", or "quartic". The defaults is "normal" kernel density. ___this one is not used currently___

__B__

The number of bootstrap samples to be used for variance estimation. The default is 0, no variance estimation.

__alpha__

The significance level. The default is 0.05.


## Methods

__ROC()__

Produces a numpy array with ROC estimations

__AUC()__

Produces a float showing AUC estimate

__plot()__

Plots the bootstrapped plot of ROC 


## Example

Install the lifelines package to import the dataset

```
pip install lifelines
```
Import the datasets from the lifelines package along with ___cenroc___ package

```
import lifelines.datasets as data
from cenroc import cenROC

df_test = data.load_panel_test()

cenROC_test1 = cenROC(Y=df_test['t'], M=df_test['var2'], censor=df_test['E'],
                     t=3, U=None, h=None, bw='NR', method="tra",
                     ktype="normal", ktype1="normal", B=3, alpha=0.05)

print(cenROC_test1.ROC())
```
Output

```
0.110000
0.177072
0.207249
0.228440
0.245245
0.259397
0.271749
0.282792
0.292835
0.302087
0.310696
...
```

```
cenROC_test2 = cenROC(Y=df_test['t'], M=df_test['var1'], censor=df_test['E'],
                                    t=2, U=None, h=None, bw=0.1, method="untra",
                                    ktype="epanechnikov", ktype1="normal", B=2, alpha=0.05)

print(cenROC_test2.AUC())
```

Output

```
0.6287878787878787
```

Due to the stochastic nature of bootstraping the graphs will be different each time.
We can set seed to produce the same result for demonstartion purposes.

```
import numpy as np
np.random.seed(3)
cenROC_test1.plot()

```

Output

![demo_pic](https://user-images.githubusercontent.com/48184866/183108886-26b99e69-5c8d-4df6-91a7-389c2d0c13b8.png)


## Contributing

Please read [CONTRIBUTING.md](https://gist.github.com/PurpleBooth/b24679402957c63ec426) for details on our code of conduct, and the process for submitting pull requests to us.

## Versioning

We use [SemVer](http://semver.org/) for versioning. For the versions available, see the [tags on this repository](https://github.com/your/project/tags). 

## Authors

This package was developed by **plaindata.ai** 

* **Yury Moskaltsov** - *Initial programming and package building* - [YuryMoskaltsov](https://github.com/YuryMoskaltsov)
* **Miguel Pereira** - *Mathematical analysis, project oversight*

See also the list of [contributors](https://github.com/your/project/contributors) who participated in this project.

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details

## Acknowledgments

* Hat tip to anyone whose code was used
* Inspiration
* etc

## Potential bugs and improvements

* Figure out translation of C function in Python correctly. Currently our function is calculating based on pure censored data instead of estimated conditional probabilities.
* Youden optimal cutpoint metric is not the same in R and Python, although they are very similar. This is due to the discrepancy in the interpolation functions. scipy.interpolate.interp1d() in Python and approx() in R. This should be tested more thoroughly to achieve identical results. All other metrics in Youden function are identical.




# censoredROC

CensoredROC allows the computation of the time-dependent ROC curve for right censored survival data using the cumulative sensitivity and dynamic specificity definitions. The ROC curves can be either empirical (non-smoothed) or smoothed with/wtihout boundary correction. It also calculates the time-dependent area under the ROC curve (AUC), the Youden index and can define an optimal cutoff for an independent continuous variables based on the Youden idex.

This package is based on the cenROC package that exists for R. The main idea was to allow Python users to apply the same tools.

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
0.110795
0.180722
0.212862
0.235690
0.253942
0.269407
0.282974
0.295154
0.306269
0.316538
0.326117
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
0.6742424242424243
```

Due to the stochastic nature of bootstraping the graphs will be different each time.
We can set seed to produce the same result for demonstartion purposes.

```
import numpy as np
np.random.seed(3)
cenROC_test1.plot()

```

Output

!![output_example](https://user-images.githubusercontent.com/48184866/183537148-d11d7333-47ca-4d1e-a1af-a55ef1e85a97.png)


## Contributing

Please read [CONTRIBUTING.md](https://gist.github.com/PurpleBooth/b24679402957c63ec426) for details on our code of conduct, and the process for submitting pull requests to us.

## Versioning

We use [SemVer](http://semver.org/) for versioning. For the versions available, see the [tags on this repository](https://github.com/your/project/tags). 

## Authors

This package was developed by **plaindata.ai** 

* **Yury Moskaltsov** - *Initial programming and package building* - [YuryMoskaltsov](https://github.com/YuryMoskaltsov)
* **Miguel Pereira** - *Mathematical analysis and implementation, project oversight* - [miguelmspereira](https://github.com/miguelmspereira)

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details

## Acknowledgments

* Kassu Mehari Beyene, Catholic University of Louvain. <kasu.beyene@uclouvain.be> - author of the cenROC R Package
* Anouar El Ghouch, Catholic University of Louvain. <anouar.elghouch@uclouvain.be> - author of the cenROC R Package

## References

* Beyene KM, El Ghouch A. Time-dependent ROC curve estimation for interval-censored data. Biom J. 2022 May 6. doi: 10.1002/bimj.202000382. PMID: 35523738.
* cenROC R package: . FYI the package is no longer on CRAN (according to the repo: *Archived on 2022-04-25 as email to the maintainer was undeliverable.*). The archived versions can be downloaded here: https://cran.r-project.org/src/contrib/Archive/cenROC/

## Improvements to be made/Planned additional features

* There is a slight discrepancy in the optimal cutpoint metric based on the Youden index obtained here and the one obtained using the cenROC package in R. This is due to a discrepancy in the interpolation functions scipy.interpolate.interp1d() in Python and approx() in R. This should be tested more thoroughly to achieve identical results. The other metrics were compared with the R output and there are no differences.
* Add a function that calculates the optimal cutpoint for a continuous variables based on the log-rank test (akin to the survminer::survcutpoint function that exists in R).
* Let us know of other functions that would be useful additions.




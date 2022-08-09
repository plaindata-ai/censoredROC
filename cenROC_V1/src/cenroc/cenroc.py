"""
This module implements the censored ROC curve estimation.
Author: Yury Moskaltsov from plaindata.ai
"""

__author__ = "Yury Moskaltsov, plaindata.ai"
__email__ = "yury-m@hotmail.com.com"
__status__ = "planning"


import numpy as np
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt
import scipy.interpolate
from matplotlib.patches import Polygon
from scipy.stats import norm
from statsmodels.sandbox.nonparametric import kernels

class cenROC():

    def __init__(self, Y, M, censor,t,
                 U=None, h=None, bw='NR', method="tra", ktype="normal",
                 ktype1="normal", B=0, alpha=0.05):

        self.Y = Y
        self.M = M
        self.censor = censor
        self.t = t
        self.U = U
        self.h = h
        self.bw = bw
        self.method = method
        self.ktype = ktype
        self.ktype1 = ktype1
        self.B = B
        self.alpha = alpha

    def kfunc(self,ktype,difmat):

        if ktype == 'normal':

            estim = norm.cdf(difmat)

        else:

            estim = difmat.copy()
            low = (difmat <= -1)
            up = (difmat >= 1)
            btwn = (difmat > -1) & (difmat < 1)
            estim[low] = 0
            estim[up] = 1
            X = estim[btwn]


            if ktype == 'epanechnikov':

                estim[btwn] = (0.75 * X * (1 - (X**2) / 3) + 0.5)

            elif ktype == 'biweight':

                estim[btwn] = (15/16) * X - (5/8) * (X**3) + (3/16) * (X**5) + 0.5

            elif ktype == 'triweight':

                estim[btwn] = (35/32) * X - (35/32) * X**3 + (21/32) * X**5 - (5/32) * X**7 + 0.5

        return estim

    def wquantile(self,X,wt,p=0.5):

        try:

            X.astype(float)
            wt.astype(float)
            float(p)

        except:

            'X, wt and p must be numeric'

        assert len(X) == len(wt), "X and wt must be equal-length vectors"
        assert p <= 1 and p >=0, "Quartiles must be 0<=p<=1"
        assert min(wt) >= 0, "Weights must be non-negative numbers"

        ord = np.argsort(X)
        X = X[ord].ravel()
        cusumw = np.cumsum(wt[ord].ravel())
        sumW = np.sum(wt)
        plist = cusumw/sumW
        interp = scipy.interpolate.interp1d(plist,X, kind='linear')

        for i in range(30):

            try:

                p += 0.05
                qua = interp(p)
                break

            except ValueError:

                continue


        return qua


    def RocFun(self,U, D, M, method, ktype=None, bw = "NR"):

        oM = np.argsort(M.ravel(),kind='mergesort')
        D = D.iloc[oM].ravel()
        nD = len(D)
        sumD = sum(D)
        Z = 1 - np.cumsum(1 - D) / (nD - sumD)
        AUC = sum(D * Z) / sumD


        assert ktype in ['normal', 'epanechnikov', 'biweight', 'triweight'], \
            ''' ktype should be on of the following: ['normal', 'epanechnikov', 'biweight', 'triweight'] '''

        assert method in ['emp', 'untra', 'tra'], \
            ''' method should be on of the following: ['emp', 'untra', 'tra'] '''

        assert bw in ['NR'] or type(bw)==float or type(bw)==int, \
            ''' bw should be a number or one of the following: ['NR'] '''

        if method == 'emp':

            difmat = np.round(np.subtract.outer(U, Z),8)
            result = difmat >= 0
            ROC1 = result * D
            ROC = np.round((np.sum(ROC1, axis=1)) / sumD,8)
            bw1 = np.nan

        if ktype == 'normal':

            kernel = kernels.Gaussian()
            ro = 2 * 0.28209
            mu2 = 1

        elif ktype == 'epanechnikov':

            kernel = kernels.Epanechnikov()
            ro = 2 * 0.12857
            mu2 = 1/5

        elif ktype == 'biweight':

            kernel = kernels.Biweight()
            ro = 2 * 0.10823
            mu2 = 1/7

        elif ktype == 'triweight':

            kernel = kernels.Triweight()
            ro = 2 * 0.095183
            mu2 = 1/9


        if method == 'untra':

            Zt = Z
            Ut = U
            Ztt = Z[D!=0]
            wt = D[D!=0]

            try:

                float(bw)
                bw1=bw

            except ValueError:

                if bw == 'NR':

                    nx = len(Ztt)
                    mul = (nx * sum(wt * wt))/((sum(wt))**2)
                    average_weighted = np.average(Ztt,weights = wt)
                    var_weighted = np.average((Ztt-average_weighted)**2, weights=wt)
                    stdv = np.sqrt(var_weighted)
                    IQR = self.wquantile(Ztt,wt,0.75) - self.wquantile(Ztt,wt,0.25)
                    sigma = min([stdv,IQR/1.349])
                    c = (4 * np.sqrt(np.pi) * (ro)/((mu2)**2))**(1/3)
                    bw1 = (c * sigma) * (mul**(1/3)) * nx**(-1/3)


            difmat = np.round(np.subtract.outer(Ut, Ztt),8) / bw1
            result = self.kfunc(ktype=ktype, difmat=difmat)
            w = wt/sum(wt)
            ROC1 = result * w
            ROC = np.round((np.sum(ROC1, axis=1)),8)

        elif method == 'tra':

            mul = nD / (nD + 1)
            Zt = norm.ppf(mul * Z + (1 / nD ** 2))
            Ut = norm.ppf(mul * U + (1 / nD ** 2))
            Ztt = Zt[D != 0]
            wt = D[D != 0]

            try:

                float(bw)
                bw1=bw

            except ValueError:

                if bw == 'NR':

                    nx = len(Ztt)
                    mul = (nx * sum(wt * wt))/((sum(wt))**2)
                    average_weighted = np.average(Ztt,weights = wt)
                    var_weighted = np.average((Ztt-average_weighted)**2, weights=wt)
                    stdv = np.sqrt(var_weighted)
                    IQR = self.wquantile(Ztt,wt,0.75) - self.wquantile(Ztt,wt,0.25)
                    sigma = min([stdv,IQR/1.349])
                    c = (4 * np.sqrt(np.pi) * (ro)/((mu2)**2))**(1/3)
                    bw1 = (c * sigma) * (mul**(1/3)) * nx**(-1/3)


            difmat = np.round(np.subtract.outer(Ut, Ztt), 8) / bw1
            result = self.kfunc(ktype=ktype, difmat=difmat)
            w = wt / sum(wt)
            ROC1 = result * w
            ROC = np.round((np.sum(ROC1, axis=1)), 8)


        return ROC, AUC, bw1


    def cenROC(self):

        '''This function calculates '''

        Y = self.Y
        M = self.M
        censor = self.censor
        t = self.t
        U = self.U
        h = self.h
        bw = self.bw
        method = self.method
        ktype = self.ktype
        ktype1 = self.ktype1
        B = self.B
        alpha = self.alpha
        plot = self.plot

        if U == None:

            U = np.linspace(0,1,151)

        try:

            Y.astype(float)
            M.astype(float)
            censor.astype(float)

        except ValueError:

            print("Error! all vectors Y, M and censor should be specified and numeric")


        ROC, AUC, bw1 = self.RocFun(U=np.array(U), D=censor, M=M, bw=bw, method = method, ktype=ktype)

        AUCc = 1- AUC

        return AUCc, ROC

    def AUC(self):

        self.auc = self.cenROC()[0]

        return self.auc

    def ROC(self):

        self.roc = self.cenROC()[1]

        return self.roc


    def plot(self):

        mpl.rcParams['figure.dpi'] = 300

        ROC = self.cenROC()[1]
        Y = self.Y
        M = self.M
        censor = self.censor
        U = self.U
        B = self.B
        method=self.method
        bw = self.bw
        ktype = self.ktype
        alpha = self.alpha

        if U == None:

            U = np.linspace(0,1,151)

        if B == 0:

            x = np.concatenate((np.array([0]), U, np.array([1])))
            y = np.concatenate((np.array([0]), ROC, np.array([1])))
            plt.plot(x, y, linewidth=1.5, color='blue')
            plt.plot([0, 1], [0, 1], color='black', linewidth=0.8)


        else:

            data = pd.DataFrame({'Y': Y, 'M': M, 'cen': censor})
            aucb = []
            rocb = np.empty((len(U), B))
            rocb[:] = np.nan

            for i in range(B):
                bootsample = np.random.randint(0, data.shape[0] - 1, data.shape[0])
                dat = data.iloc[bootsample, :]
                ROC_b, AUC_b, bw1_b = self.RocFun(U=U, D=dat['cen'], M=dat['M'], method=method,
                                             bw=bw, ktype=ktype)
                aucb.append(1 - AUC_b)
                rocb[:, i] = ROC_b

            SP = np.quantile(aucb, [alpha / 2, 1 - alpha / 2])

            AUC = pd.DataFrame(
                {'AUC': [np.round(np.mean(aucb), 4)],  # 'AUC': [np.round(AUCc, 4)],
                 'sd': [np.round(np.std(aucb, ddof=1), 4)],
                 'LCL': [np.round(SP[0], 4)],
                 'UCL': [np.round(SP[1], 4)]

                 })

            qroc = np.apply_along_axis(np.quantile, 1, rocb, [alpha / 2, 1 - alpha / 2])

            ROC = pd.DataFrame({'ROC': np.apply_along_axis(np.mean, 1, rocb), 'LCL': qroc[:, 0], 'UCL': qroc[:, 1]})

            fig, ax = plt.subplots()

            x = np.concatenate((np.array([0]), U, np.array([1])))
            y = np.concatenate((np.array([0]), ROC['ROC'], np.array([1])))
            plt.plot(x, y, linewidth=1.5, color='blue')

            x_pol_1 = np.flip(np.concatenate((np.array([0]), U, np.array([1]))))
            x_pol_2 = np.concatenate((np.array([0]), U, np.array([1])))
            x_pol = np.concatenate((x_pol_1, x_pol_2))

            y_pol_1 = np.concatenate((np.array([0]), ROC['UCL'], np.array([1])))
            y_pol_2 = np.concatenate((np.array([0]), ROC['LCL'], np.array([1])))
            y_pol = np.concatenate((np.flip(y_pol_1), y_pol_2))

            coordinates_pol = np.array([x_pol, y_pol]).T

            p = Polygon(coordinates_pol,
                        facecolor='skyblue', edgecolor='red',
                        linestyle='--', alpha=0.5)

            ax.add_patch(p)

        plt.xlabel("False positive rate", color='blue')
        plt.ylabel("True positive rate", color='blue')

        return fig

    def youden(self):

        U = self.U

        if U == None:

            U = np.linspace(0,1,151)

        ROC = self.cenROC()[1]
        M = self.M
        D = self.censor

        ord = np.argsort(M.ravel(),kind='mergesort')
        M = M.iloc[ord].ravel()
        D = D.iloc[ord].ravel()

        sens = []
        spec = None

        for m in M:

            sens.append(np.sum(D*np.where(M > m, 1,0))/np.sum(D))

        Jm = ROC - U
        opt_Jm = max(Jm)
        opt_Jm_index = np.argmax(Jm)
        opt_sens = ROC[opt_Jm_index]
        opt_spec = 1 - U[opt_Jm_index]
        opt_cut = scipy.interpolate.interp1d(sens,M, kind='linear').__call__(opt_sens)

        out = pd.DataFrame({'Youden_index': [opt_Jm], 'cutopt': [opt_cut], 'sens': [opt_sens], 'spec': [opt_spec]})

        return out

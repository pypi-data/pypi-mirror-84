#!/usr/bin/env python
# coding: utf-8

# ## Importing The Libraries

'''
The first step is to import the relevant modules and libraries. We're going to import the LogisticRegression, LDA and QDA classifiers for this forecaster:
'''
# In[7]:

import datetime
import numpy as np
import pandas as pd
import sklearn

from pandas_datareader import DataReader
from past.builtins import xrange
from sklearn.linear_model import LogisticRegression
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis as LDA
from sklearn.discriminant_analysis import QuadraticDiscriminantAnalysis as QDA

# ## The main Class

# In[8]:

class FinForecast:
    ''' Constructor '''
    def __init__(self):
        None
    
    def create_lagged_series(symbol, start_date, end_date, lags=5):
    
    # Obtain stock information from Yahoo Finance
        ts = DataReader(symbol, "yahoo", start_date-datetime.timedelta(days=365), end_date)

    # Create the new lagged DataFrame
        tslag = pd.DataFrame(index=ts.index)
        tslag["Today"] = ts["Adj Close"]
        tslag["Volume"] = ts["Volume"]

    # Create the shifted lag series of prior trading period close values
        for i in xrange(0,lags):
            tslag["Lag%s" % str(i+1)] = ts["Adj Close"].shift(i+1)

    # Create the returns DataFrame
        tsret = pd.DataFrame(index=tslag.index)
        tsret["Volume"] = tslag["Volume"]
        tsret["Today"] = tslag["Today"].pct_change()*100.0

    # If any of the values of percentage returns equal zero, set them to
    # a small number (stops issues with QDA model in scikit-learn)
        for i,x in enumerate(tsret["Today"]):
            if (abs(x) < 0.0001):
                tsret["Today"][i] = 0.0001

    # Create the lagged percentage returns columns
        for i in xrange(0,lags):
            tsret["Lag%s" % str(i+1)] = tslag["Lag%s" % str(i+1)].pct_change()*100.0

    # Create the "Direction" column (+1 or -1) indicating an up/down day
        tsret["Direction"] = np.sign(tsret["Today"])
        tsret = tsret[tsret.index >= start_date]

        return tsret

    def fit_model(name, model, X_train, y_train, X_test, pred):

    # Fit and predict the model on the training, and then test, data
        model.fit(X_train, y_train)
        pred[name] = model.predict(X_test)

    # Create a series with 1 being correct direction, 0 being wrong
    # and then calculate the hit rate based on the actual direction
        pred["%s_Correct" % name] = (1.0+pred[name]*pred["Actual"])/2.0
        hit_rate = np.mean(pred["%s_Correct" % name])
        print("%s: %.3f" % (name, hit_rate))

if __name__ == "__main__":
    # Create a lagged series of the S&P500 US stock market index
    snpret = create_lagged_series("^GSPC", datetime.datetime(2001,1,10), datetime.datetime(2005,12,31), lags=5)

    # Use the prior two days of returns as predictor values, with direction as the response
    X = snpret[["Lag1","Lag2"]]
    y = snpret["Direction"]

    # The test data is split into two parts: Before and after 1st Jan 2005.
    start_test = datetime.datetime(2005,1,1)

    # Create training and test sets
    X_train = X[X.index < start_test]
    X_test = X[X.index >= start_test]
    y_train = y[y.index < start_test]
    y_test = y[y.index >= start_test]

    # Create prediction DataFrame
    pred = pd.DataFrame(index=y_test.index)
    pred["Actual"] = y_test
    
    # Create and fit the three models    
    print("Hit Rates:")
    models = [("LR", LogisticRegression()), ("LDA", LDA()), ("QDA", QDA())]
    for m in models:
        fit_model(m[0], m[1], X_train, y_train, X_test, pred)


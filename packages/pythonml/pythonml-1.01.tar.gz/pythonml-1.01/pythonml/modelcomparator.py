import numpy as np
import pandas as pd


# __2.1___

def reg_comparator(X, y, test_size=0.2, random_state=42, scaler=False, plot=False, verbose=True):
    '''
    Author: Aru Raghuvanshi

    Function takes 4 arguments of datasets split by train test split
    method and fits 6 well known regressive machine learning models of
    Linear Regression, KNN, Random Forests, Decision Tree, XGBoost
    and LightGBM Regressors with their defaults arguments
    and returns a dataframe with metrics plot.

    ----------------------------------------------
    Usage example:

    X = df.drop('target', axis=1)
    y = df.target
    reg_comparator(X, y)

    --------------------------------

    Returns: Dataframe, plot
    '''
    from sklearn.model_selection import train_test_split
    from sklearn.linear_model import LinearRegression
    from sklearn.ensemble import RandomForestRegressor
    from sklearn.tree import DecisionTreeRegressor
    from xgboost import XGBRegressor
    from lightgbm import LGBMRegressor
    from sklearn.neighbors import KNeighborsRegressor
    from sklearn.metrics import mean_squared_error
    from sklearn.preprocessing import StandardScaler
    import warnings
    warnings.filterwarnings('ignore')
    import matplotlib.pyplot as plt
    import seaborn as sns
    sns.set()

    sc = StandardScaler()

    xtr, xt, ytr, yt = train_test_split(X, y, test_size=test_size, random_state=random_state)

    if scaler == True:
        if verbose == True: print('> Initiating standard scaler...')
        xtr = sc.fit_transform(xtr)
        xt = sc.transform(xt)
        if verbose == True: print('> Data scaling \033[1;32msuccessful\033[0m.')
    else:
        if verbose == True: print('> Initializing models on \033[1;34munscaled\033[0m dataset.')

    models = []
    models.append((LinearRegression()))
    models.append((DecisionTreeRegressor()))
    models.append((RandomForestRegressor()))
    models.append((XGBRegressor()))
    models.append((LGBMRegressor()))
    models.append((KNeighborsRegressor()))

    trresults = []
    teresults = []
    rmres = []

    if verbose == True: print('> Commencing all model fittings...')
    for model in models:
        model.fit(xtr, ytr)
        #         global prd
        prd = model.predict(xt)
        trs = model.score(xtr, ytr)
        tes = model.score(xt, yt)
        RMSE = np.round(np.sqrt(mean_squared_error(yt, prd)), 4)
        trresults.append(trs)
        teresults.append(tes)
        rmres.append(RMSE)
    if verbose == True: print('> \033[1;32mFittings completed\033[0m.')

    allscores = pd.DataFrame({
        'LinReg': [trresults[0], teresults[0], rmres[0]],
        'D-Tree': [trresults[1], teresults[1], rmres[1]],
        'R-Forest': [trresults[2], teresults[2], rmres[2]],
        'XGBoost': [trresults[3], teresults[3], rmres[3]],
        'LGBM': [trresults[4], teresults[4], rmres[4]],
        'KNN': [trresults[5], teresults[5], rmres[5]],
        'Scores': ['Training Score', 'Test Scores', 'RMSE']
    })

    allscores.set_index('Scores', drop=True, inplace=True)
    t_allscores = allscores.drop('RMSE', axis=0)

    if plot == True:
        if verbose == True: print('> Generating Plot...')
        t_allscores.plot(kind='bar', rot=0, figsize=(16, 6), colormap='Accent')

    return allscores





## __2.1___

def clf_comparator(X, y, test_size=0.2, random_state=42, scaler=False, plot=False, k=2, verbose=True):

    '''
    Author: Aru Raghuvanshi

    Function takes the 4 arguments of the 'train test split' method
    along with one of KFold value 'k', and fits 6 well known
    classifier machine learning models of LogisticReg, Random Forest,
    Decision Tree, XGBoost and LightGBM classifiers and returns a
    dataframe with metrics and plots..

    ----------------------------------------------
    Usage example:

    X = df.drop('target', axis=1)
    y = df.target
    clf_comparator(X, y)

    --------------------------------
    Returns: Dataframe of metrics, plot
    '''

    from sklearn.preprocessing import StandardScaler
    from sklearn.model_selection import train_test_split
    from sklearn.linear_model import LogisticRegression
    from sklearn.ensemble import RandomForestClassifier
    from sklearn.tree import DecisionTreeClassifier
    from sklearn.neighbors import KNeighborsClassifier
    from xgboost import XGBClassifier
    from lightgbm import LGBMClassifier
    from sklearn.model_selection import KFold, cross_val_score
    import seaborn as sns
    import warnings
    warnings.filterwarnings('ignore')
    sns.set()

    sc = StandardScaler()

    xtr, xt, ytr, yt = train_test_split(X, y, test_size=test_size, random_state=random_state)

    if scaler == True:
        if verbose == True: print('> Initiating standard scaler...')
        xtr = sc.fit_transform(xtr)
        xt = sc.transform(xt)
        if verbose == True: print('> Data scaling \033[1;32msuccessful\033[0m.')
    else:
        if verbose == True: print('> Initializing LogReg, DTree, RForest, XGB, LGBM, KNN on \033[1;31munscaled\033[0m dataset...')

    models = []
    models.append((LogisticRegression(solver='lbfgs')))
    models.append((DecisionTreeClassifier()))
    models.append((RandomForestClassifier()))
    models.append((XGBClassifier()))
    models.append((LGBMClassifier()))
    models.append((KNeighborsClassifier()))
#     print('Models appended.')
    trresult = []
    teresult = []

    if verbose == True: print('> Commencing all model fittings...')
    for model in models:
        model.fit(xtr, ytr)

        prd = model.predict(xt)
        Kfold = KFold(n_splits=k, random_state=42)
        cv_result = np.mean(cross_val_score(model, xtr, ytr, cv=Kfold, scoring='accuracy'))
        trresult.append(cv_result)
        tes = model.score(xt, yt)
        teresult.append(tes)
    if verbose == True: print('> \033[1;32mFittings completed\033[0m.')

    allscores = pd.DataFrame({'Log Reg': [trresult[0], teresult[0]],
                              'D-Tree': [trresult[1], teresult[1]],
                              'R-Forest': [trresult[2], teresult[2]],
                              'XGBoost': [trresult[3], teresult[3]],
                              'LGBM': [trresult[4], teresult[4]],
                              'KNN':[trresult[5], teresult[5]],
                              'Score': ['Training', 'Test']
                             })

    allscores.set_index('Score', drop=True, inplace=True)

    if plot == True:
        if verbose == True: print('> Generating Plot...')
        allscores.plot(kind='bar', rot=0, figsize=(16, 6), colormap='terrain')

    return allscores
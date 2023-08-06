import pandas as pd
import numpy as np


# ======================= CUSTOM REGRESSORS ===================== ]

# __2.1.2___

def run_regressor(model, X, y, test_size=0.2, random_state=42, k=2, scaler=False, rd=4, plot=False):
    '''
    Author: Aru Raghuvanshi

    This Functions Fits a Regression model with the Train Datasets and
    predicts on a Test Dataset and evaluates its various metrics.
    Returns the fitted model to be used on other test datasets.
    If Scaler is set to true, it performs standard scaling on train and test sets.

    Arguments: estimator, predictor_matrix, label_array, test_size, random_state, k, scaler,
    rounding values of metrics and plot of cross validated scores.
    ---------------------------------------------------------------------------------------------

    Example usage:

    X = df.drop('target', axis=1)
    y = df.target

    rr = RandomForestRegressor(n_estimators=100, max_depth=3, verbose=1)

    model_xg, y_pred = run_regressor(rr, X, y, ts=0.2, rs=42, k=5, scaler=False)

    score = mean_squared_error(y_test, y_pred)


    y_pred2 = model_xg.predict(X_test2)   # Using fittedmoddel to predict on other test sets

    score2 = mean_absolute_error(y_test2, y_pred2)
    ------------------------------------------------------------

    Returns: Fittedmodel, predictions, Plot
    '''

    import warnings
    from warnings import filterwarnings
    from sklearn.metrics import mean_squared_error, mean_absolute_error
    from sklearn.model_selection import cross_val_score, KFold, train_test_split
    from sklearn.preprocessing import StandardScaler
    import matplotlib.pyplot as plt
    import numpy as np
    import pandas as pd

    sc = StandardScaler()

    plt.style.use('seaborn')
    warnings.filterwarnings('ignore')

    xtr, xt, ytr, yt = train_test_split(X, y, test_size=test_size, random_state=random_state)

    if scaler == True:
        xtr = sc.fit_transform(xtr)
        xt = sc.transform(xt)

    fittedmodel = model.fit(xtr, ytr)

    kf = KFold(n_splits=k, random_state=22)
    trsc = cross_val_score(model, xtr, ytr, cv=kf)
    tesc = cross_val_score(model, xt, yt, cv=kf)
    tr = round(np.mean(trsc), rd)
    te = round(np.mean(tesc), rd)
    #     global pred
    pred = model.predict(xt)

    rmse = round(np.sqrt(mean_squared_error(yt, pred)), rd)
    mae = round(mean_absolute_error(yt, pred), rd)
    try:
        mape = round((np.mean(np.abs((yt - pred) / yt)) * 100), rd)
    except:
        mape = 'NA'

    #     tr = round(tr, rd)
    #     te = round(te, rd)

    if 1.1 > tr / te > 1.07:
        fit = 'Slight Over-Fit'
    elif 0.89 < tr / te < 0.93:
        fit = 'Slight Under-Fit'
    elif tr / te > 1.1:
        fit = 'Over-Fitted'
    elif tr / te < 0.89:
        fit = 'Under-Fitted'
    else:
        fit = 'Good Fit'

    table = pd.DataFrame({'CV Training Score': [tr],
                          'CV Test Score': [te],
                          'RMSE': [rmse],
                          'MAE': [mae],
                          'MAPE %': [mape],
                          'Fit': [fit]
                          }).T

    if plot == True:
        fig = plt.figure(figsize=(14, 5))
        plt.ylim(0, 1)
        plt.plot(range(1, k + 1), trsc, label='Cross Validated Training Scores', color='navy',
                 marker='o', mfc='black', ls='dashed')
        plt.plot(range(1, k + 1), tesc, label='Cross Validated Test Scores', color='salmon',
                 marker='o', mfc='red')
        plt.xlabel('Cross Validation Iterations', fontsize=14)
        plt.ylabel('Model Scores', fontsize=14)
        plt.title('Train vs Test Scores', fontsize=16)
        plt.legend(fontsize=14)

    table.rename(columns={0: 'Score'}, inplace=True)

    display(table)

    return fittedmodel, pred


# ============================= FIT CLASSIFY ============================ ]


# __2.1.2__

def run_classifier(model, X, y, test_size=0.2, random_state=42, k=2, scaler=False, rd=4, plot=False):
    '''
    Author: Aru Raghuvanshi

    This Functions Fits a classification model with the Train Datasets and
    predicts on a Test Dataset and evaluates its various metrics.
    Also returns fittedmodel that can be used to predict on other test datasets.
    If Scaler is set to true, it performs standard scaling on train and test sets.

    Arguments: estimator, predictor matrix, labels, test size, random state,
    Kfolds, rounding value of metrics and plot of scores
    ----------------------------------------------------------------------------------------------------

    Example usage:

    rr = RandomForestClassifier(n_estimators=100, max_depth=3, verbose=1)

    mod, y_pred = run_classifier(rr, X_train, X_test, y_train, y_test, k=5)

    score = accuracy_score(y_test, y_pred)

    y_pred2 = mod.predict(X_test2)
    conf_matrix = confusion_matrix(y_test2, y_pred2)
    ------------------------------------------------------------

    Returns: Fittedmodel, Predictions, Plot

    '''

    import warnings
    from warnings import filterwarnings
    from sklearn.model_selection import KFold, cross_val_score, train_test_split
    from sklearn.metrics import classification_report, confusion_matrix
    import matplotlib.pyplot as plt
    from sklearn.preprocessing import StandardScaler
    import numpy as np
    import pandas as pd

    warnings.filterwarnings('ignore')
    sc = StandardScaler()

    xtr, xt, ytr, yt = train_test_split(X, y, test_size=test_size, random_state=random_state)

    if scaler == True:
        xtr = sc.fit_transform(xtr)
        xt = sc.transform(xt)

    fittedmodel = model.fit(xtr, ytr)

    pred = model.predict(xt)

    kf = KFold(n_splits=k, random_state=random_state)

    graphtr = cross_val_score(model, xtr, ytr, cv=kf, scoring='accuracy')
    graphte = cross_val_score(model, xt, yt, cv=kf, scoring='accuracy')

    tr = np.mean(cross_val_score(model, xtr, ytr, cv=kf, scoring='accuracy'))
    te = np.mean(cross_val_score(model, xt, yt, cv=kf, scoring='accuracy'))

    #     tepr = round(np.mean(cross_val_score(model, xt, yt, cv=kf, scoring='precision_weighted')), rd)
    #     tere = round(np.mean(cross_val_score(model, xt, yt, cv=kf, scoring='recall_weighted')), rd)
    #     tef1 = round(np.mean(cross_val_score(model, xt, yt, cv=kf, scoring='f1')), rd)
    tr = round(tr, rd)
    te = round(te, rd)

    if 1.1 > tr / te > 1.07:
        fit = 'Slight Over-Fit'
    elif 0.89 < tr / te < 0.93:
        fit = 'Slight Under-Fit'
    elif tr / te > 1.1:
        fit = 'Over-Fitted'
    elif tr / te < 0.89:
        fit = 'Under-Fitted'
    else:
        fit = 'Good Fit'

    cm = confusion_matrix(yt, pred)

    cr = classification_report(yt, pred, output_dict=True)
    cr = pd.DataFrame(cr).T

    for i in cr.columns:
        cr[i] = round(cr[i], rd)

    table = pd.DataFrame({
        'CV Training Score': [tr],
        'CV Test Score': [te],
        'Fit': [fit]
    }).T

    table.rename(columns={0: 'Accuracy Score'}, inplace=True)

    if plot == True:
        fig = plt.figure(figsize=(14, 5))
        plt.ylim(0, 1)
        plt.plot(range(1, k + 1), graphtr, label='Cross Validated Training Scores', color='navy',
                 marker='o', mfc='black', ls='dashed')
        plt.plot(range(1, k + 1), graphte, label='Cross Validated Test Scores', color='salmon',
                 marker='o', mfc='red')
        plt.xlabel('Cross Validation Iterations', fontsize=14)
        plt.ylabel('Model Scores', fontsize=14)
        plt.title('Train vs Test Scores', fontsize=16)
        plt.legend(fontsize=14)

    print('\n\t\t\033[1;30mClassification Report\033[0m')
    display(cr)
    display(table)
    print(f'\n\033[1;30mConfusion Matrix:\033[0m \n{cm}')

    return fittedmodel, pred


# ---------------------------------KMEANS K FINDER ------------------------------]


def kmeans_kfinder(dtf, lower=1, upper=9):

    '''
    Author: Aru Raghuvanshi

    Standardize (StandardScaler) data before feeding to function.
    This functions plots the Elbow Curve for KMeans Clustering
    to find the elbow value of K.

    Arguments: (dataframe, lower=1, upper=9)
    Returns: Plot

    Defaults of lower=0, upper=7
    Example: e = elbowplot(df, 0, 5)
    '''

    from sklearn.cluster import KMeans
    import matplotlib.pyplot as plt
    plt.style.use('seaborn')

    #     from scipy.spatial.distance import cdist
    k_range = range(lower, upper)
    sse = []
    for i in k_range:
        km = KMeans(n_clusters=i)
        km.fit(dtf)
        sse.append(km.inertia_)
    #       sse.append(sum(np.min(cdist(dtf, km.cluster_centers_, 'euclidean'), axis=1)) / dtf.shape[0]))

    plt.figure(figsize=(14, 6))
    plt.plot(k_range, sse, label='K vs SSE', color='g', lw=3, marker='o', mec='black')
    plt.xlabel('K', fontsize=18)
    plt.title('KMEANS ELBOW PLOT - K vs Sum of Square Error', fontsize=16)
    plt.legend()
    plt.show()



# ----------------------------- KNN K FINDER --------------------------------]


def knn_kfinder(xtr, xt, ytr, yt, lower=1, upper=30):

    '''
    Author: Aru Raghuvanshi

    This function plots the KNN elbow plot to figure out
    the best value for K in the KNN Classifier.

    Arguments: (xtr, xt, ytr, yt, lower=1, upper=30)
    Returns: Plot

    Example: p = knn_plot(X_train, X_test, y_train, y_test, 1, 30)

    '''
    from sklearn.neighbors import KNeighborsClassifier
    from sklearn.metrics import accuracy_score
    import matplotlib.pyplot as plt
    plt.style.use('seaborn')

    krange = range(lower, upper)
    acc_score = []
    # Might take some time
    for i in krange:
        knn = KNeighborsClassifier(n_neighbors=i)
        knn.fit(xtr, ytr)
        pred_i = knn.predict(xt)
        acc_score.append(accuracy_score(yt, pred_i))

    plt.figure(figsize=(14, 6))
    plt.plot(krange, acc_score, color='salmon', linestyle='solid',
             marker='o', mfc='purple', label='K vs Testing Accuracy', lw=2)
    plt.title('KNN K-GRAPH')
    plt.xlabel('K', fontsize=18)
    plt.ylabel('Test Accuracy', fontsize=16)
    plt.legend()
    plt.show()




# ----------------------------- STRATIFIED KFOLD PREDICTOR --------------------------------]


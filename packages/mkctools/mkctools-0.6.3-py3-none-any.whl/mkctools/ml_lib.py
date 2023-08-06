import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import GridSearchCV 
from sklearn.metrics import accuracy_score
from sklearn.model_selection import learning_curve 
import pickle
from datetime import datetime

class simple_ml():
    def __init__(self, X, y):
        self.X = X
        self.y = y
        
    def train(self, clf, standardize = False):
        X_train, X_test, y_train, y_test = train_test_split(self.X, self.y, test_size = 0.2)
        
        self.standardize = standardize
        if standardize:
            self.StandardScaler1 = StandardScaler()
            self.StandardScaler1.fit(X_train)
            X_train = self.StandardScaler1.transform(X_train)
            X_test = self.StandardScaler1.transform(X_test)
            
        #X_train.shape, X_test.shape, y_train.shape, y_test.shape
        clf.fit(X_train, y_train)

        score = clf.score(X_test, y_test)
        self.clf= clf
        
        return score
        
    def save(self, model_file_name='model.pickle'):
        with open(model_file_name, 'wb') as f:
            pickle.dump(self.clf, f)
        return model_file_name
        
    def load(self, model_file_name='model.pickle'):
        with open(model_file_name, 'rb') as f:
            return pickle.load(f)
        
    def predict(self, X):
        if self.standardize:
            X = self.StandardScaler1.transform(X)
        return self.clf.predict(X)

    # https://jonathonbechtel.com/blog/2018/02/06/wines/
    def plot_learning_curve(self, estimator, title, X, y, ylim=None, cv=None,
                        n_jobs=1, train_sizes=np.linspace(.6, 1.0, 5)):
        """
        Generate a simple plot of the test and traning learning curve.

        Parameters
        ----------
        estimator : object type that implements the "fit" and "predict" methods
            An object of that type which is cloned for each validation.

        title : string
            Title for the chart.

        X : array-like, shape (n_samples, n_features)
            Training vector, where n_samples is the number of samples and
            n_features is the number of features.

        y : array-like, shape (n_samples) or (n_samples, n_features), optional
            Target relative to X for classification or regression;
            None for unsupervised learning.

        ylim : tuple, shape (ymin, ymax), optional
            Defines minimum and maximum yvalues plotted.

        cv : integer, cross-validation generator, optional
            If an integer is passed, it is the number of folds (defaults to 3).
            Specific cross-validation objects can be passed, see
            sklearn.cross_validation module for the list of possible objects

        n_jobs : integer, optional
            Number of jobs to run in parallel (default 1).
        """
        plt.figure()
        plt.title(title)
        if ylim is not None:
            plt.ylim(*ylim)
        plt.xlabel("Training examples")
        plt.ylabel("Score")
        train_sizes, train_scores, test_scores = learning_curve(
            estimator, X, y, cv=cv, n_jobs=n_jobs, train_sizes=train_sizes)
        train_scores_mean = np.mean(train_scores, axis=1)
        train_scores_std = np.std(train_scores, axis=1)
        test_scores_mean = np.mean(test_scores, axis=1)
        test_scores_std = np.std(test_scores, axis=1)
        plt.grid()

        plt.fill_between(train_sizes, train_scores_mean - train_scores_std,
                         train_scores_mean + train_scores_std, alpha=0.1,
                         color="r")
        plt.fill_between(train_sizes, test_scores_mean - test_scores_std,
                         test_scores_mean + test_scores_std, alpha=0.1, color="g")
        plt.plot(train_sizes, train_scores_mean, 'o-', color="r",
                 label="Training score")
        plt.plot(train_sizes, test_scores_mean, 'o-', color="g",
                 label="Cross-validation score")

        plt.legend(loc="best")
        return plt

    # https://jonathonbechtel.com/blog/2018/02/06/wines/
    def evaluate(self, classifiers_dict, plot=False, verbose = True):
        X_train, X_test, y_train, y_test = train_test_split(self.X, self.y, test_size = 0.2)
        
        num_classifiers = len(classifiers_dict.keys())
        df_results = pd.DataFrame(
            data=np.zeros(shape=(num_classifiers,4)),
            columns = ['classifier',
                       'train_score', 
                       'test_score',
                       'training_time'])
        count = 0
        plt_list=[]
        for key, classifier in classifiers_dict.items():
            if verbose:
                print(f"start training {key} ...")

            t_start = datetime.now()
            grid = GridSearchCV(classifier['classifier'], 
                          classifier['params'],
                          refit=True,
                            cv = 10, # 9+1
                            scoring = 'accuracy', # scoring metric
                            n_jobs = -1
                            )
            estimator = grid.fit(X_train,
                                 y_train)
            t_end = datetime.now()
            t_diff = t_end - t_start
            train_score = estimator.score(X_train,
                                          y_train)
            test_score = estimator.score(X_test,
                                         y_test)
            df_results.loc[count,'classifier'] = key
            df_results.loc[count,'train_score'] = train_score
            df_results.loc[count,'test_score'] = test_score
            df_results.loc[count,'training_time'] = t_diff
            if verbose:
                print(f"trained {key} in {t_diff:.2f} s")
            count+=1
            if plot:
                plt1 = self.plot_learning_curve(estimator, 
                                      "{}".format(key),
                                      X_train,
                                      y_train,
                                      ylim=(0.75,1.0),
                                      cv=10)
                plt_list.append(plt1)
        return df_results, plt_list
        
if __name__ == "__main__":
    import pandas as pd
    from sklearn import datasets
    from sklearn.neighbors import KNeighborsClassifier
    from mkctools.mkctools.ml_lib import simple_ml


    ds = datasets.load_wine()
    print(ds.DESCR)

    print('取得資料集的資料')
    X = ds.data
    df = pd.DataFrame(ds.data, columns=ds.feature_names)
    print(df.head())
    print('')

    y = ds.target
    print(f'y={y[:10]}')
    print('')

    print('檢查資料中是否有null值')
    print(df.isna().sum())
    print('')

    # simple_ml test
    ml_process = simple_ml(X, y)
    clf = KNeighborsClassifier(n_neighbors=3)
    score = ml_process.train(clf, True)
    print(f'score = {score}')

    ml_process.save()
    model = ml_process.load()

    print(f'predict = {model.predict(df.sample(2))}')

    # evaluate test
    from sklearn.naive_bayes import GaussianNB
    from sklearn.svm import SVC, LinearSVC
    from sklearn.neighbors import KNeighborsClassifier
    from sklearn.linear_model import LogisticRegression
    from sklearn import tree
    from sklearn.neural_network import MLPClassifier
    from sklearn.ensemble import GradientBoostingClassifier
    from sklearn.gaussian_process.kernels import RBF
    from sklearn.ensemble import RandomForestClassifier

    classifiers_dict = {
        "Logistic Regression": 
                {'classifier': LogisticRegression(solver='liblinear'),
                    'params' : [
                                {
                                 'max_iter': [1000],
                                 'penalty': ['l1','l2'],
                                 'C': [0.01,0.1,1,10,100,1000]
                                }
                               ]
                },
        "Nearest Neighbors": 
                {'classifier': KNeighborsClassifier(),
                     'params': [
                                {
                                'n_neighbors': [1, 3, 5, 10],
                                'leaf_size': [3, 30]
                                }
                               ]
                },
                 
        "Linear SVM": 
                {'classifier': SVC(),
                     'params': [
                                {
                                 'C': [1, 10, 100, 1000],
                                 'gamma': [0.001, 0.0001],
                                 'kernel': ['linear']
                                }
                               ]
                },
        # "Gradient Boosting Classifier": 
                # {'classifier': GradientBoostingClassifier(),
                     # 'params': [
                                # {
                                 # 'learning_rate': [0.05, 0.1],
                                 # 'n_estimators' :[50, 100, 200],
                                 # 'max_depth':[3,None]
                                # }
                               # ]
                # },
        "Decision Tree":
                {'classifier': tree.DecisionTreeClassifier(),
                     'params': [
                                {
                                 'max_depth':[3,None]
                                }
                                 ]
                },
        "Random Forest": 
                {'classifier': RandomForestClassifier(),
                     'params': {}
                },
        "Naive Bayes": 
                {'classifier': GaussianNB(),
                     'params': {}
                }
    }
    df_results, chart_list = ml_process.evaluate(classifiers_dict, plot=True)
    from IPython.display import display, HTML
    print('')
    display(df_results.sort_values(by='test_score', ascending=False))

    for chart1 in chart_list:
        chart1.show()
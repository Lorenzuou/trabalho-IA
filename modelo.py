# import base estimators
from sklearn.base import BaseEstimator
# import classifiers
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.naive_bayes import GaussianNB
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)
from scipy import stats
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split

import pandas as pd
import numpy as np
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import RepeatedStratifiedKFold
from sklearn.model_selection import GridSearchCV
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

  
from sklearn.discriminant_analysis import StandardScaler
from sklearn.pipeline import Pipeline
from tqdm import tqdm



def train_model(model,params_grid,name, df): 
    scalar = StandardScaler()
    pipe = Pipeline(steps=[('s',scalar), ('m', model)])

    gs = GridSearchCV(pipe, param_grid=params_grid, scoring='accuracy', cv=RepeatedStratifiedKFold(n_splits=4, n_repeats=3, random_state=36851234), n_jobs=-1)

    scores = cross_val_score(gs, X_train, y_train.values.ravel(), scoring='accuracy', cv=RepeatedStratifiedKFold(n_splits=10, n_repeats=3, random_state=36851234), n_jobs=-1)

    df_awnser = pd.concat([df, pd.DataFrame({'method': [name], 'mean': [np.mean(scores)], 'std': [np.std(scores)], 'lower': [np.mean(scores) - np.std(scores)], 'upper': [np.mean(scores) + np.std(scores)]})], ignore_index=True)
    
    return df_awnser, " "


class HeterogeneousEnsemble(BaseEstimator):
    # define o construtor para o classificador
    def __init__(self,n_samples=3):
        
        self.classifiers  =  [DecisionTreeClassifier(), KNeighborsClassifier(), GaussianNB()]
        self.n_samples = n_samples
        self.trained_classifiers = []


    def train_classifiers(self, X_train, y_train):

        # converter para numpy array
        X_train = X_train.to_numpy()
        y_train = y_train.to_numpy()

        # faz o loop sobre os classificadores individuais
        for clf in self.classifiers:
            # treina o classificador no conjunto de treinamento atual
            clf.fit(X_train, y_train.ravel())
            # adiciona o classificador treinado à lista
            self.trained_classifiers.append(clf)
        # retorna a lista de classificadores treinados
        return self.trained_classifiers

    def sample_data(self,X_train, y_train, random_state):
        # amostra as características com reposição e obtém os rótulos correspondentes
        X_train_sampled = X_train.sample(frac=1, replace=True, random_state=random_state)
        y_train_sampled = y_train.loc[X_train_sampled.index]
        # retorna o conjunto de dados amostrado
        return X_train_sampled, y_train_sampled


    def predict_hp(self, X_test, class_order):
        # cria um dicionário para armazenar as predições de cada classificador
        votes = {}
        X_test = X_test.to_numpy().reshape(1, -1)
        # faz o loop sobre os classificadores individuais
        for clf in self.trained_classifiers:
            # prediz a classe do exemplo de teste usando o classificador atual
            pred = clf.predict(X_test)
            # armazena a predição no dicionário
            if pred[0] in votes:
                votes[pred[0]] += 1
            else:
                votes[pred[0]] = 1
                

        # obtém a(s) classe(s) mais votada(s) e as armazena em uma lista
        max_votes = max(votes.values())
        most_voted_classes = [k for k,v in votes.items() if v == max_votes]
        
        hp_pred = None

        # se houver mais de uma classe mais votada, quebra o empate usando a ordem das classes do conjunto de treinamento
        if len(most_voted_classes) > 1:
            for c in class_order:
                if c in most_voted_classes:
                    hp_pred = c
                    break
            if hp_pred is None:
                hp_pred = most_voted_classes[0]
        # caso contrário, retorna a classe mais votada como a predição do conjunto HP
        else:
            hp_pred = most_voted_classes[0]

        # retorna a predição
        return hp_pred



    def fit(self,X_train,y_train): 

        # # if data is numpy array, convert to pandas dataframe
        if isinstance(X_train, np.ndarray):
            X_train = pd.DataFrame(X_train)
        if isinstance(y_train, np.ndarray):
            y_train = pd.Series(y_train)

        # reset index
        X_train.reset_index(drop=True, inplace=True)
        y_train.reset_index(drop=True, inplace=True)

        classifiers = [] # ciclo para treinar os classificadores individuais
        for i in range(self.n_samples):
            # se for a primeira iteração, use os dados de treinamento originais
            if i == 0:
                X_train_current = X_train.copy()
                y_train_current = y_train.copy()
            # caso contrário, crie um novo conjunto de treinamento amostrando com reposição os dados originais usando a função sample_data
            else:
                X_train_current, y_train_current = self.sample_data(X_train, y_train, i)
            
            # treina os classificadores individuais nos dados de treinamento atuais usando a função train_classifiers e os estende à lista
            classifiers.extend(self.train_classifiers(X_train_current, y_train_current))

    def predict(self,X_test): 
        if(isinstance(X_test, np.ndarray)):
            X_test = pd.DataFrame(X_test)
        
        class_order = y_train.value_counts().index.tolist()
        # cria uma lista vazia para armazenar as predições do conjunto HP
        hp_predictions = []
        # faz o loop sobre os exemplos de teste
        for index, row in X_test.iterrows():
            # predict the class of the test example using the predict_hp function and append it to the list # prediz a classe do exemplo de teste usando a função predict_hp e a adiciona à lista
            hp_pred = self.predict_hp(row, class_order)
            hp_predictions.append(hp_pred)
        return hp_predictions

    

if __name__ == "__main__":

    X = pd.read_csv('X.csv')
    y = pd.read_csv('y.csv')
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=11)

    df = pd.DataFrame(columns=['method', 'mean', 'std', 'lower', 'upper'])


    # divide o conjunto de dados em conjuntos de treinamento e teste
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=7)
    hp = HeterogeneousEnsemble()

    name = 'HP'

    params_grid = {
        'm__n_samples': [3,9,15,21]
        }

    df,df_per_fold = train_model(hp,params_grid,name,df)

    print(df)

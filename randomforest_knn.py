import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.neighbors import KNeighborsClassifier
from imblearn.under_sampling import RandomUnderSampler
from sklearn.svm import SVC
from sklearn.model_selection import train_test_split
import sklearn.metrics
import keras
import joblib
import matplotlib.pyplot as plt
import seaborn as sns

def readData():
    features = pd.read_csv("large_data.csv")
    features = features.rename(columns={'TYPE' : 'CLASS'})  
    colnames = features.columns
    label_encoder = LabelEncoder()
    features['CLASS']= label_encoder.fit_transform(features['CLASS']) #codificando as labels
    labels = features.pop('CLASS') #removendo a coluna de classe das features
    keys = label_encoder.classes_  
    values = label_encoder.transform(label_encoder.classes_)
    dictionary = dict(zip(keys, values)) #storing the converted column entries as (key,value) pairs
    print(dictionary)
    X_train, X_test, y_train, y_test = train_test_split(features, labels, test_size=0.20,random_state=5)  #separando o dataset em dados de teste e dados para treinamento
    scaler = StandardScaler()
    scaler.fit(X_train)
    X_train = scaler.transform(X_train) 
    X_test = scaler.transform(X_test)
    rus = RandomUnderSampler()
    X_res, y_res = rus.fit_resample(X_train, y_train)
    X_test_res, y_test_res = rus.fit_resample(X_test, y_test)
    return X_res,y_res,X_test_res, y_test_res   

def trainingDataRF(X_train, y_train, X_test, y_test):
    print("---------------- Random Forest ----------------")
    global accuracyRF
    RFclassifier = RandomForestClassifier(n_estimators = 10, criterion = 'entropy', random_state = 42) # 10 arvóres de decisão para a classificação
    RFclassifier.fit(X_train, y_train) #treinando
    filename = 'rf_model.sav'
    y_pred = RFclassifier.predict(X_test) 
    accuracyRF = sklearn.metrics.accuracy_score(y_test, y_pred)
    conf_matrix = sklearn.metrics.confusion_matrix(y_test, y_pred)
    #matriz de confusão
    fig, ax = plt.subplots(figsize=(7.5, 7.5))
    ax.matshow(conf_matrix, cmap=plt.cm.Blues, alpha=0.3)
    for i in range(conf_matrix.shape[0]):
        for j in range(conf_matrix.shape[1]):
            ax.text(x=j, y=i,s=conf_matrix[i, j], va='center', ha='center', size='xx-large')
    
    plt.xlabel('Predictions', fontsize=18)
    plt.ylabel('Actuals', fontsize=18)
    plt.title('Confusion Matrix', fontsize=18)
    plt.show()
    print(sklearn.metrics.classification_report(y_test,y_pred))
    joblib.dump(RFclassifier, filename)  #salvando modelo(utilizado em chatbot.py)

def trainingDataKNN(X_train, y_train, X_test, y_test):
    print("---------------- K-Nearest neighbor ----------------")
    KnnClassifier = KNeighborsClassifier(n_neighbors=10,metric='euclidean') 
    KnnClassifier.fit(X_train, y_train) # treina o KnnClassifier 
    y_pred = KnnClassifier.predict(X_test)
    conf_matrix = sklearn.metrics.confusion_matrix(y_test, y_pred)
    fig, ax = plt.subplots(figsize=(7.5, 7.5))
    ax.matshow(conf_matrix, cmap=plt.cm.Blues, alpha=0.3)
    for i in range(conf_matrix.shape[0]):
        for j in range(conf_matrix.shape[1]):
            ax.text(x=j, y=i,s=conf_matrix[i, j], va='center', ha='center', size='xx-large')
    
    plt.xlabel('Predictions', fontsize=18)
    plt.ylabel('Actuals', fontsize=18)
    plt.title('Confusion Matrix', fontsize=18)
    plt.show()
    print(sklearn.metrics.classification_report(y_test,y_pred))
    joblib.dump(KnnClassifier, 'knn_model.sav')  #salvando modelo(utilizado em chatbot.py)


def main():
    X_train,Y_train,X_test,Y_test=readData()
    trainingDataRF(X_train, Y_train, X_test, Y_test)
    trainingDataKNN(X_train, Y_train, X_test, Y_test)


if __name__ == "__main__": 
  main()

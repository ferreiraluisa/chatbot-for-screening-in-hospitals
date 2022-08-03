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
    features['CLASS']= label_encoder.fit_transform(features['CLASS']) #performing label encoding in the given column
    labels = features.pop('CLASS')  #removing the class column from the features table
    keys = label_encoder.classes_  
    values = label_encoder.transform(label_encoder.classes_)
    dictionary = dict(zip(keys, values)) #storing the converted column entries as (key,value) pairs
    print(dictionary)
    X_train, X_test, y_train, y_test = train_test_split(features, labels, test_size=0.20,random_state=5)  #splitting the dataset into train and test set
    scaler = StandardScaler()
    scaler.fit(X_train)
    X_train = scaler.transform(X_train) 
    X_test = scaler.transform(X_test)
    rus = RandomUnderSampler()
    X_res, y_res = rus.fit_resample(X_train, y_train)
    # ver o balanceamento das classes
    sns.countplot(y_res)
    return X_res,y_res, X_test, y_test    

def trainingDataRF(X_train, y_train, X_test, y_test):
    global accuracyRF
    RFclassifier = RandomForestClassifier(n_estimators = 10, criterion = 'entropy', random_state = 42) # 10 decision trees used in this classifier
    RFclassifier.fit(X_train, y_train)  #training  
    filename = 'rf_model.sav'
    joblib.dump(RFclassifier, filename)  #save the model
    y_pred = RFclassifier.predict(X_test) #predict on test set
    accuracyRF = sklearn.metrics.accuracy_score(y_test, y_pred)
    conf_matrix = sklearn.metrics.confusion_matrix(y_test, y_pred)
    #
    # Print the confusion matrix using Matplotlib
    #
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

def trainingDataKNN(X_train, y_train, X_test, y_test):
    # instancia um knn
    # n_neighbors indica a quantidade de vizinhos
    # metric indica a medida de distancia utilizada
    knn = KNeighborsClassifier(n_neighbors=10,metric='euclidean')
    # treina o knn  
    knn.fit(X_train, y_train)
    # testa o knn com X_teste
    # y_pred consistira em um numpy.array onde
    # cada posicao contem a classe predita pelo knn
    # para o respectivo objeto em X_teste
    y_pred = knn.predict(X_test)
    conf_matrix = sklearn.metrics.confusion_matrix(y_test, y_pred)
    #
    # Print the confusion matrix using Matplotlib
    #
    print(knn.predict([[1,0,1,0,0,0,1,0,1,0,1,0,1,0,1,1,0,1,0,1]]))
    # fig, ax = plt.subplots(figsize=(7.5, 7.5))
    # ax.matshow(conf_matrix, cmap=plt.cm.Blues, alpha=0.3)
    # for i in range(conf_matrix.shape[0]):
    #     for j in range(conf_matrix.shape[1]):
    #         ax.text(x=j, y=i,s=conf_matrix[i, j], va='center', ha='center', size='xx-large')
    
    # plt.xlabel('Predictions', fontsize=18)
    # plt.ylabel('Actuals', fontsize=18)
    # plt.title('Confusion Matrix', fontsize=18)
    # plt.show()
    # print(sklearn.metrics.classification_report(y_test,y_pred))
    


def main():
    X_train,Y_train,X_test,Y_test=readData()
    trainingDataKNN(X_train, Y_train, X_test, Y_test)
# Tell python to run main method
if __name__ == "__main__": 
  main()

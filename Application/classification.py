#Libraries

#Create and read csv files
import os 
import pathlib
import csv
import librosa #to create musin info for csv file

import pandas as pd #to process data from csv
import numpy as np #to process data from csv

#For machine learning preprocess
import sklearn as skl
from sklearn.model_selection import train_test_split
from sklearn.model_selection import GroupShuffleSplit
from sklearn.preprocessing import LabelEncoder, StandardScaler

#Naive Bayes
from sklearn.naive_bayes import BernoulliNB

#Support Vector Machine
from sklearn.svm import SVC

#Neural Network
import keras
from keras import models
from keras import layers
import warnings  #To turn off warning messages
warnings.filterwarnings('ignore')

import math


class Classifier():
    dataSet=""
    genre_list=""
    genres=""
    X=""
    y=""
    test=""
    def __init__(self, **kwargs):
        super(Classifier, self).__init__(**kwargs)
        self.dataSet= pd.read_csv("data_train.csv")
        self.genre_list = self.dataSet.iloc[:, -1]
        self.genres = pd.unique(self.genre_list)
        encoder = LabelEncoder()
        self.y = encoder.fit_transform(self.genre_list)
        scaler = StandardScaler()
        self.X = scaler.fit_transform(np.array(self.dataSet.iloc[:, :-1], dtype = float))

        print("Classifier init")

    def euclidean_distance(self,x, y): 
        summ=0
        for j in range(0,len(x)-1):
            summ+=(x[j]-y[j])**2
        return math.sqrt(summ) 

    def kNN(self,k=25,clsCount=5):
        trainX=self.X
        trainY=self.y
        testX=self.test[0]

        distances={}
        for i in range(0,len(trainX)):
            distances[i]=self.euclidean_distance(trainX[i],testX)
        sortedDistance= {k: v for k, v in sorted(distances.items(), key=lambda item: item[1])}
        sortedDistanceListForK=list(sortedDistance.keys())[:k]
        freqs=[0 for i in range(clsCount)]
        for i in range(len(sortedDistanceListForK)):
            freqs[ trainY[ sortedDistanceListForK[i] ] ] += 1
        y_prob=[(i/sum(freqs))*100 for i in freqs]
        y_prob2 = [float("{:.2f}".format(float(i))) for i in y_prob]
        return y_prob2

    def bnb(self):
        trainX=self.X
        trainY=self.y
        testX=self.test

        bnb = BernoulliNB()
        y_pred = bnb.fit(trainX, trainY).predict(testX)
        y_prob = bnb.fit(trainX, trainY).predict_proba(testX)
        y_prob = y_prob.tolist()[0]
        y_prob2 = [float("{:.3f}".format(float(i))) for i in y_prob]
        y_prob2 = [(i/sum(y_prob2))*100 for i in y_prob2]
        y_prob2 = [float("{:.2f}".format(float(i))) for i in y_prob2]
        return y_prob2
    
    def svma(self):
        trainX=self.X
        trainY=self.y
        testX=self.test

        clf = SVC(probability=True)
        y_pred = clf.fit(trainX, trainY).predict(testX)
        y_prob = clf.fit(trainX, trainY).predict_proba(testX)
        y_prob = y_prob.tolist()[0]
        y_prob2 = [float("{:.3f}".format(float(i))) for i in y_prob]
        y_prob2 = [(i/sum(y_prob2))*100 for i in y_prob2]
        y_prob2 = [float("{:.2f}".format(float(i))) for i in y_prob2]
        return y_prob2

    def nn(self):
        trainX=self.X
        trainY=self.y
        testX=self.test

        model = models.Sequential()
        model.add(layers.Dense(256, activation='relu', input_shape=(trainX.shape[1],)))

        model.add(layers.Dense(128, activation='relu'))

        model.add(layers.Dense(64, activation='relu'))

        model.add(layers.Dense(5, activation='softmax'))
        model.compile(optimizer='Nadam',
                    loss='sparse_categorical_crossentropy')
        model.fit(trainX,
                trainY,
                epochs=25,
                batch_size=256)
        
        y_pred=model.predict([testX])
        y_pred = y_pred.tolist()[0]
        y_prob=model.predict_proba([testX])

        y_prob = y_prob.tolist()[0]
        y_prob2 = [float("{:.3f}".format(float(i))) for i in y_prob]
        y_prob2 = [(i/sum(y_prob2))*100 for i in y_prob2]
        y_prob2 = [float("{:.2f}".format(float(i))) for i in y_prob2]
        return y_prob2

    def setMusic(self,filePath):
        self.test=[]
        y, sr = librosa.load(filePath, mono=True, duration=30)
        chroma_stft = librosa.feature.chroma_stft(y=y, sr=sr)
        spec_cent = librosa.feature.spectral_centroid(y=y, sr=sr)
        spec_bw = librosa.feature.spectral_bandwidth(y=y, sr=sr)
        rolloff = librosa.feature.spectral_rolloff(y=y, sr=sr)
        zcr = librosa.feature.zero_crossing_rate(y)
        mfcc = librosa.feature.mfcc(y=y, sr=sr)
        self.test.append(np.mean(chroma_stft))
        self.test.append(np.mean(spec_cent))
        self.test.append(np.mean(spec_bw))
        self.test.append(np.mean(rolloff))
        self.test.append(np.mean(zcr))
        for e in mfcc:
            self.test.append(np.mean(e))
        self.test = [self.test]
        print("Test Ready")


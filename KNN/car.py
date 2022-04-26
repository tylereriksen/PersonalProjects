# REFERENCES: Tech With Tim Video on KNN Learning, Chingis Oinar's Toward Data Science article
'''
    File that aims to make its own KNN machine learning algorithm and then
    comparing it to the sklearn package for KNN Learning.
'''

import pandas as pd
import math
import numpy as np
import sklearn
from sklearn import linear_model, preprocessing
from sklearn.neighbors import KNeighborsClassifier
from sklearn.utils import shuffle

# method for finding the distance between data points
def distanceNeighbor(trainSet, compareSet, weights = []):
    if weights == []:
        weights = [1 for x in range(len(trainSet))]

    sum = 0.0
    for idx, num in enumerate(trainSet):
        sum += ((num - compareSet[idx]) ** 2) * weights[idx]
    return math.sqrt(sum)

# method for finding the indexes, distances, and values that we want to find from the data set
def findKeyMax(trainXData, trainYData, testXDataPoint):
    listDist = []

    for idx, num in enumerate(trainXData):
        listDist.append((idx, trainYData[idx], distanceNeighbor(num, testXDataPoint)))

    listDist.sort(key = lambda x: x[2])

    return listDist

# print out the values, distances, and expected predictions from the learning done
def printInnerCalculations(Knum, trainXData, trainYData, testXDataPoint):
    orderedList = findKeyMax(trainXData, trainYData, testXDataPoint)[:Knum]
    for idx, num in enumerate(orderedList):
        print(testXDataPoint, "-->", trainXData[idx], "=", num[2], "VALUE:", trainYData[idx])

# predict the outcome value based on the functions for KNN that were programmed above
def myKNNLearn(Knum, trainXData, trainYData, testXDataPoint):
    orderedList = findKeyMax(trainXData, trainYData, testXDataPoint)
    newOrder = [x[1] for x in orderedList]

    subset = newOrder[:Knum]
    maxValue = max(subset, key = subset.count)
    return maxValue




# read the data
data = pd.read_csv("./student/car.data")

# convert to numerical data
le = preprocessing.LabelEncoder()
buying = le.fit_transform(list(data["buying"]))
maint = le.fit_transform(list(data["maint"]))
door = le.fit_transform(list(data["door"]))
persons = le.fit_transform(list(data["persons"]))
lug_boot = le.fit_transform(list(data["lug_boot"]))
safety = le.fit_transform(list(data["safety"]))
cls = le.fit_transform(list(data["class"]))

# define what the predictor is
predict = "class"

# define the inputs/covariates and the outputs
X = list(zip(buying, maint, door, persons, lug_boot, safety))
y = list(cls)

x_train, x_test, y_train, y_test = sklearn.model_selection.train_test_split(X, y, test_size = 0.1)

K = 7

# this is the SKLearn model for KNN to compare to our model
model = KNeighborsClassifier(n_neighbors=K)
model.fit(x_train, y_train)
acc = model.score(x_test, y_test)

predicted = model.predict(x_test)

# tests to see how many were correct
correct = 0
total = 0

# tests for seeing how many of the outcomes that were NOT 2 were correct
# this is of interest since most of the cls data is a 2
testNot2 = 0
totalTestNot2 = 0
for x in range(len(x_test)):
    print("-----------------------------------------------------------------------")
    printInnerCalculations(K, x_train, y_train, x_test[x])
    if myKNNLearn(K, x_train, y_train, x_test[x]) == y_test[x]:
        correct += 1
    if not y_test[x] == 2:
        if myKNNLearn(K, x_train, y_train, x_test[x]) == y_test[x]:
            testNot2 += 1
        totalTestNot2 += 1
    print("PREDICTED:", myKNNLearn(K, x_train, y_train, x_test[x]))
    print("EXPECTED:", y_test[x])
    total += 1
    print()
print(acc)
print("%d out of the %d tests passed giving an accruacy of %f percent" %(correct, total, correct / total * 100))
print(testNot2 / totalTestNot2, (correct - testNot2) / (total - totalTestNot2)) # there is a significant discrepancy
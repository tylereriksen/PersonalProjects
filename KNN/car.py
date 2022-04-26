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

def getCertainIndex(listX, idx):
    return [listX[x] for x in idx]

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

list0 = [idx for idx in range(len(cls)) if cls[idx] == 0]
list1 = [idx for idx in range(len(cls)) if cls[idx] == 1]
list2 = [idx for idx in range(len(cls)) if cls[idx] == 2]
list3 = [idx for idx in range(len(cls)) if cls[idx] == 3]
x0_train, x0_test, y0_train, y0_test = sklearn.model_selection.train_test_split(list(zip(getCertainIndex(buying, list0), getCertainIndex(maint, list0), getCertainIndex(door, list0), getCertainIndex(persons, list0), getCertainIndex(lug_boot, list0), getCertainIndex(safety, list0))), getCertainIndex(y, list0), test_size = 0.1)
x1_train, x1_test, y1_train, y1_test = sklearn.model_selection.train_test_split(list(zip(getCertainIndex(buying, list1), getCertainIndex(maint, list1), getCertainIndex(door, list1), getCertainIndex(persons, list1), getCertainIndex(lug_boot, list1), getCertainIndex(safety, list1))), getCertainIndex(y, list1), test_size = 0.1)
x2_train, x2_test, y2_train, y2_test = sklearn.model_selection.train_test_split(list(zip(getCertainIndex(buying, list2), getCertainIndex(maint, list2), getCertainIndex(door, list2), getCertainIndex(persons, list2), getCertainIndex(lug_boot, list2), getCertainIndex(safety, list2))), getCertainIndex(y, list2), test_size = 0.1)
x3_train, x3_test, y3_train, y3_test = sklearn.model_selection.train_test_split(list(zip(getCertainIndex(buying, list3), getCertainIndex(maint, list3), getCertainIndex(door, list3), getCertainIndex(persons, list3), getCertainIndex(lug_boot, list3), getCertainIndex(safety, list3))), getCertainIndex(y, list3), test_size = 0.1)

x_train, x_test, y_train, y_test = sklearn.model_selection.train_test_split(X, y, test_size = 0.1)

K = 9

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


# this is to see if learning can be done better if there are equal portions of data being split per outcome
x_train = x0_train + x1_train + x2_train + x3_train
x_test = x0_test + x1_test + x2_test + x3_test
y_train = y0_train + y1_train + y2_train + y3_train
y_test = y0_test + y1_test + y2_test + y3_test
model = KNeighborsClassifier(n_neighbors=K)
model.fit(x_train, y_train)
not2Indexes = [x for x in range(len(y_test)) if not y_test[x] == 2]
is2Indexes = [x for x in range(len(y_test)) if y_test[x] == 2]
acc = model.score(x_test, y_test)
accN2 = model.score(getCertainIndex(x_test, not2Indexes), getCertainIndex(y_test, not2Indexes))
acc2 = model.score(getCertainIndex(x_test, is2Indexes), getCertainIndex(y_test, is2Indexes))
print(acc)
print(accN2, acc2) # differences in the discrepancies of the accruacy levels of output of 2 and not 2
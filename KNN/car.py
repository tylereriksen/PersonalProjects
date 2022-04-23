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

    sum = 0
    for idx, num in enumerate(trainSet):
        sum += ((num - compareSet[idx]) ** 2) * weights[idx]
    return math.sqrt(sum)

# method for finding the indexes of the keys with the highest values (list form)
def findKeyMax(dict):
    returnList = [0]
    for idx, num in enumerate(dict.keys()):
        if idx == 0:
            returnList = [idx]
        else:
            if dict[num] > dict[list(dict.keys())[returnList[0]]]:
                returnList = [idx]
            elif dict[num] == dict[list(dict.keys())[returnList[0]]]:
                returnList.append(idx)
    return returnList


cov = []
m = []
s = []
a = []



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

# define important variables for the self-made implementation of KNN
correctTests = 0
totalTests = 0
K = 9

for idx in range(len(x_test)):
    pointTest1 = x_test[idx]
    pointTester1 = y_test[idx]
    cov.append(pointTest1)
    a.append(pointTester1)

    print()
    dict_neighbors = {}
    res = sorted(range(len(x_train)), key = lambda sub: distanceNeighbor(x_train[sub], pointTest1))
    for thing in res[:K]:
        print(thing, "Distance:", distanceNeighbor(x_train[thing], pointTest1), "Class:", y_train[thing])
        dict_neighbors[y_train[thing]] = 0
    print()
    for thing in res[:K]:
        dict_neighbors[y_train[thing]] += 1
        # print(pointTest1, "-->", x_train[thing], "=", distanceNeighbor(x_train[thing], pointTest1))



    dict = findKeyMax(dict_neighbors)
    counter = 0
    while not len(dict) == 1:
        newP = res[K + counter]
        if y_train[newP] not in dict_neighbors.keys():
            dict_neighbors[y_train[newP]] = 1
        else:
            dict_neighbors[y_train[newP]] += 1
        dict = findKeyMax(dict_neighbors)
        print()
        print("----------NEED ANOTHER TEST POINT----------")
        print(newP, "Distance:", distanceNeighbor(x_train[newP], pointTest1), "Score:", y_train[newP])
        counter += 1

    print()
    print("Predicted Value:", list(dict_neighbors.keys())[dict[0]])
    m.append(list(dict_neighbors.keys())[dict[0]])
    print("Actual Value of Test Point:", pointTester1)
    totalTests += 1
    if list(dict_neighbors.keys())[dict[0]] == y_train[thing]:
        correctTests += 1

print("%d out of %d tests matched with the machine learning prediction, giving an accuracy of %f percent." %(correctTests, totalTests, (100 * correctTests) / totalTests))

# this is the SciKitLearn model for KNN to compare to our model
model = KNeighborsClassifier(n_neighbors=K)
model.fit(x_train, y_train)
acc = model.score(x_test, y_test)
print(acc)

predicted = model.predict(x_test)
for x in range(len(predicted)):
    s.append(predicted[x])

d = {"covariates values": cov, "my result": m, "scikit result": s, "actual result": a}
df = pd.DataFrame(data = d)
print(df)
df.to_csv("carDataComparison.csv") # write to csv file
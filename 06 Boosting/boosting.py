import subprocess
from nltk.stem.porter import *
import math
import operator

D1 = []
for i in range(5485):
    D1.append(1/5485)

myData = open('first_SVM_classify_output.dat')
realData = open('first_SVM_indexed_train_data.dat')


correct = 0
incorrect = 0
epsilon1 = 0
index = -1
#맞는거 틀린거 개수 새기.
for myEachData in myData :
    index+=1

    myDataValue = float(myEachData.strip())
    eachRealData = int(realData.readline().split(' ')[0])

    if eachRealData == -1:
        if myDataValue < 0: #맞음
            correct+=1
        else:
            incorrect+=1
            epsilon1 += D1[index]
    else:
        if myDataValue < 0: #틀림
            incorrect+=1
            epsilon1 += D1[index]
        else:
            correct+=1

myData.seek(0,0)
realData.seek(0,0)

alpha1 = 0.5 * math.log( (1-epsilon1) / epsilon1, math.e)

index = -1
sumOfD1 = 0
D2 = []
for myEachData in myData :
    index+=1

    myDataValue = float(myEachData.strip())
    eachRealData = int(realData.readline().split(' ')[0])

    if eachRealData == -1:
        if myDataValue < 0: #맞음
            D2.append(D1[index] * (math.e ** -alpha1))
        else:
            D2.append(D1[index] * (math.e ** alpha1))
    else:
        if myDataValue < 0: #틀림
            D2.append(D1[index] * (math.e ** alpha1))
        else:
            D2.append(D1[index] * (math.e ** -alpha1))
    sumOfD1 += D2[index]

for i in range(len(D2)):
    D2[i] = D2[i] / sumOfD1

firstIndexedFile = open('first_SVM_indexed_train_data.dat')
secondIndexFile = open('second_SVM_indexed_train_data.dat', 'w')

index = -1
for firstLine in firstIndexedFile:
    index+=1
    firstLine = firstLine.strip().split(' ')
    toOutput = ''
    if firstLine[0] == '+1' :
        toOutput = '+1 '
    else:
        toOutput = '-1 '

    for eachComp in firstLine[1 : ] :
        eachComp = eachComp.split(':')
        toOutput += eachComp[0] + ':'
        toOutput += str(float(eachComp[1]) * D2[index]) + ' '
    toOutput+='\n'
    secondIndexFile.write(toOutput)

training = subprocess.check_output(['svm_learn.exe', 'second_SVM_indexed_train_data.dat', 'second_SVM_trained_model.dat'])
print(training)

classifying = subprocess.check_output(['svm_classify.exe', 'second_SVM_indexed_train_data.dat', 'second_SVM_trained_model.dat', 'second_SVM_classify_output.dat',])
myData = open('second_SVM_classify_output.dat')
realData = open('second_SVM_indexed_train_data.dat')

correct = 0
incorrect = 0
epsilon2 = 0
index = -1
#맞는거 틀린거 개수 새기.
for myEachData in myData :
    index+=1

    myDataValue = float(myEachData.strip())
    eachRealData = int(realData.readline().split(' ')[0])

    if eachRealData == -1:
        if myDataValue < 0: #맞음
            correct+=1
        else:
            incorrect+=1
            epsilon2 += D2[index]
    else:
        if myDataValue < 0: #틀림
            incorrect+=1
            epsilon2 += D2[index]
        else:
            correct+=1
print('epsilon2 : ' ,epsilon2)
alpha2 = 0.5 * math.log( (1-epsilon2) / epsilon2, math.e)
print('alpha2: ', alpha2)

myLastResult = []

realData.seek(0,0)
myFirstData = open('first_SVM_classify_output.dat')
mySecondData = open('second_SVM_classify_output.dat')

correct = 0
incorrect = 0
for firstLine in myFirstData :
    try:
        firstValue = float(firstLine.strip())
        secondLine = mySecondData.readline().strip()
        secondValue = float(secondLine)
    except:
        continue
    result = firstValue * alpha1 + secondValue * alpha2
    eachRealData = int(realData.readline().split(' ')[0])
    if result > 0 :
        if eachRealData == 1:
            correct+=1
        else:
            incorrect+=1
    else:
        if eachRealData == 1:
            incorrect+=1
        else :
            correct+=1

print('accuracy : ' , correct / (incorrect+correct))
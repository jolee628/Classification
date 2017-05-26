###############################################
#     Shuo Yuan (Steve) Yang, Joseph Lee      #
###############################################

from __future__ import division
from math import *
import sys

training = sys.argv[1]
testing = sys.argv[2]
outputName = sys.argv[3]

##################################################################
#  Build the node class for decision tree                         #
#                                                                 #
################################################################## 
class Node(object):
    def __init__(self, label = None):
        self.label = label
        self.children = {}

    def add_child(self, obj, value):
        self.children[value] = obj



##################################################################
#    Use the entropy for different subsets to determine           #
#    the attribute for split that gives the best gain ratio       #
################################################################## 
def chooseBestInfoGain(dataset):
    numberOfColumns = len(dataset[0])-1 
    EntropyOfCurrentData = entropy(dataset)

    bestInfoGain = 0.0
    bestAttribute4split = -1
#Take out each attribute
    for col in range(0, numberOfColumns):
        columnUniqueValues = getColumn(dataset, col)
        entropyOfThisAttribute = 0.0
        splitInfo = 0.0
#Take each category for the selected attribute and calculate the entropy of subsets
#Return the attribute that gives the highest gain ratio
        for val in columnUniqueValues:
            Dj = generateDj(dataset, val, col)
            probability = len(Dj)/float(len(dataset))
            entropyOfThisAttribute += probability * entropy(Dj)
            splitInfo -= probability * log(probability,2)

        if (EntropyOfCurrentData - entropyOfThisAttribute) == 0:
            continue

        gain = (EntropyOfCurrentData - entropyOfThisAttribute)
        
        gainRatio = 0
        if  splitInfo == 0:
            gainRatio = 0
        else:
            gainRatio = gain/splitInfo

        if (gainRatio > bestInfoGain):
            bestInfoGain = gainRatio
            bestAttribute4split = col

    return bestAttribute4split

###################################################################
#   Calculate the entropy for the given dataset table             #                                                 
#                                                                 #
################################################################### 

def entropy(dataSet):    

    totalCount = len(dataSet)  
    
    catagory = {}  
    for each in dataSet:
        currentLabel = each[0] 
        
        boolean = currentLabel in catagory.keys()

        if boolean == False:  
            catagory[currentLabel] = 0;
        else:
            catagory[currentLabel] += 1
    
    Entropy = 0.0  

    for key in catagory:  
        probability = catagory[key]/totalCount
        Entropy -= probability * log(probability, 2)
        
    return Entropy;  

##################################################################
#    Use Majority count when there's a single column              #
#    Return P or E which appears more than the other              #
################################################################## 
def majority(alist):
    count = {}
    for item in alist:
        if item not in count.keys():
            count[item] = 0
        count[item] += 1
    v = list(count.values())
    k = list(count.keys())
    return k[v.index(max(v))]

##################################################################
#    Given the attribute for split, generate the subsets           #
#    Take all the values in attribute list except                  #
#    the corresponding value of that attribute                     #
################################################################## 

def generateDj(sets, Key, attribute):    #DONE
    Dj = []
    for row in sets:

        if row[attribute+1] == Key:
            newRow = row[:attribute+1]+row[attribute+2:]

            Dj.append(newRow)

    return Dj 

##################################################################
#    Take all the values of one column                            #
################################################################## 
def getColumn (dataset, column):
    columnList = []       #All letters in the column
    for row in dataset:
        columnList.append(row[column+1])
    columnItems = list(set(columnList))#Unique letters in the column    
    return columnItems

##################################################################
#    Build the decision tree with recursion                       #
################################################################## 
def Generate_Decision_Tree(dataSet, attributeL):
    result = []
    #Base Case
    #if tuples in D are all of the same class, C, then
    #return N as a leaf node labeled with the class C;
    #if attribute list is empty then
    #return N as a leaf node labeled with the majority class in
    for row in dataSet:
        result.append(row[0])
    if len(result) == result.count(result[0]):
        return result[0] #P or E
    if len(dataSet[0]) == 1:
        return majority(result)
    
    
    #Choose the best splitting criterion
    splitting_criterion = chooseBestInfoGain(dataSet)

    n = Node(attributeL[splitting_criterion])

    #attribute list  attribute list - splitting attribute
    del attributeL[splitting_criterion]

    featureValues = getColumn(dataSet, splitting_criterion)

    #for each outcome j of splitting criterion
    #partition the tuples and grow subtrees for each partition
    #let Dj be the set of data tuples in D satisfying outcome j;
    for featureValue in featureValues:
        Dj = generateDj(dataSet, featureValue, splitting_criterion)
        subAttributeList = attributeL[:]
    #attach the node returned by Generate decision tree(Dj , attribute list) to node N;
        n.children[featureValue] = Generate_Decision_Tree(Dj, subAttributeList)
    return n

##################################################################
#   Classify using the decision tree built by training data       #
################################################################## 
def testclassification(dTree, attributeList, testRow):  
    treeLabel = dTree.label

    treeChildren = dTree.children

    attrIndex = attributeList.index(treeLabel) 

    attrValue = treeChildren[testRow[attrIndex+1]]

    if type(attrValue).__name__ == 'Node':

        classLabel = testclassification(attrValue, attributeList, testRow)  

    else: 

        classLabel = attrValue

    return classLabel 



##################################################################
#   takes in the TRAINING set                                     #
#   go through line by line and seperate them into                #
#   one List of List and store as training set                    #
#                                                                 #
################################################################## 

linesForTraining = []
with open(training) as file:
    for line in file.readlines():
        line = [each for each in line.split()]
        linesForTraining.append(line)
trainingData = linesForTraining
attributeList = [str(i) for i in range(len(trainingData[0])-1)] # label each attribute
dTree = Generate_Decision_Tree(trainingData, attributeList)


##################################################################
#   takes in the TESTING  set                                     #
#   go through line by line and seperate them into                #
#   one List of List and store as TESTING  set                    #
#                                                                 #
################################################################## 

linesForTest = []
with open(testing) as file:
    for line in file.readlines():
        line = [each for each in line.split()]
        linesForTest.append(line)
testData = linesForTest

##################################################################
#       put the testing file into the decision tree,              # 
#       compare the copmuted result with the acutal result        #
#       generate output file with the percentage accuracy at the  #
#       bottom of the file                                        #
################################################################## 

f = open(outputName,"w")

attributeList = [str(i) for i in range(len(trainingData[0]))] # label each attribute

testResult = []
for testRow in testData:
    classt= testclassification(dTree, attributeList, testRow)
    testResult.append(classt)
    

real_testResult = [row[0] for row in testData]
accuracy = 0

for i in range(len(testResult)):
    if testResult[i] == real_testResult[i]:
        accuracy += 1

for i in range(len(real_testResult)):

    f.write("Correct Answer:  " + real_testResult[i] + "   Answer Computed:  " + testResult[i] +'\n')
f.write("Percentage of Correctness:  " + str((accuracy/len(testResult))*100)+'%')

f.close()




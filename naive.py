###############################################
#     Shuo Yuan (Steve) Yang, Joseph Lee      #
###############################################
from __future__ import division
import sys
import time
import itertools
from collections import *

training = sys.argv[1]
testing = sys.argv[2]
outputName = sys.argv[3]



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



##################################################################
#   takes in the TESTING  set                                     #
#   go through line by line and seperate them into                #
#   one List of List and store as TESTING  set                    #
#                                                                 #
################################################################## 
linesForTesting = []

with open(testing) as file:
	for line in file.readlines():
		line = [each for each in line.split()]
		linesForTesting.append(line)

tesingData = linesForTesting





##################################################################
#   take in the list of training data                             #
#   return a list of list of dictionaries with count              #
#         generate a list of list of dictionaries like this:      #
#		[[{p:_ , e:_}],[{        }],[{},{},{},{}]]                #
#                                                                 #
#		RETURN A LIST OF GENERAL COUNT                            #
#                                                                 #
################################################################## 


def generate_total_count(trainingData):
	list_of_dictionaries =[]
	count = -1

	for elem in trainingData:
		count += 1
		for index, item in enumerate(elem):
			
			if count == 0:            ## this is for the first pass
				intermeidate_list = []
				intermeidate_dict = {}
				intermeidate_dict[item] = 1
				intermeidate_list.append(intermeidate_dict)
				list_of_dictionaries.append(intermeidate_list)
			
			else:
				intermeidate_dict = {}
								
				if item in list_of_dictionaries[index][0]:
					
					list_of_dictionaries[index][0][item] += 1
				else:
					list_of_dictionaries[index][0][item] = 1

	return list_of_dictionaries




##################################################################
#   take in list of dictionaries   of training set                #
#   calculate the probE and probP and then put it in global var   #
#                                                                 #
#                                                                 #
################################################################## 


def probE_probP(general_count):

	Ecount = general_count[0][0]['e']
	Pcount = general_count[0][0]['p']
	total = Ecount+Pcount

	global probE 
	probE = Ecount/total
	
	global probP
	probP = Pcount/total

	return


##################################################################
#   take in list of training set                                  #
#   construct 2 list of P and E correcsponding to the occurance   #
#   of each element                                               #
#                                                                 #
################################################################## 


list_of_P =[]
list_of_E = []

def constructListforPandE(trainingData):



	countP = -1
	countE = -1
	for elem in trainingData:
		
		if elem[0] == 'p':
			
			countP +=1 
			
			for index, item in enumerate(elem):
				
				
				if countP == 0:
					intermeidate_dict = {}
					intermeidate_dict[item] = 1
					list_of_P.append(intermeidate_dict)
				
				else:
								
					if item in list_of_P[index]:
					
						list_of_P[index][item] += 1
					else:
						list_of_P[index][item] = 1
		else:
			
			countE +=1 
			
			for index, item in enumerate(elem):
				
				
				if countE == 0:
					intermeidate_dict = {}
					intermeidate_dict[item] = 1
					list_of_E.append(intermeidate_dict)
				
				else:
					
					if item in list_of_E[index]:
					
						list_of_E[index][item] += 1
					else:
						list_of_E[index][item] = 1
				

	return 



##################################################################
#   classify the testing data, and                    #
#   return a list of list of dictionaries with count              #
#         generate a list of list of dictionaries like this:      #
#		[[{p:_ , e:_}],[{        }],[{},{},{},{}]]                #
#                                                                 #
#		RETURN A LIST OF GENERAL COUNT                            #
#                                                                 #
################################################################## 

list_of_correct_answers = []
algorithm_answer = []
per = None

def classify(tesingData, list_of_P, list_of_E):
	
	totalCount = 0
	correctCount = 0
	



	for row in tesingData:
		
		XgivenP = []
		XgivenE = []
		
		correctAnswer = row[0]
		list_of_correct_answers.append(correctAnswer)
		totalCount+=1

		for index, item in enumerate(row):
			
			if index == 0:  ##skipping the first index

				continue

			if item in list_of_P[index]:
				percentage = list_of_P[index][item]/list_of_P[0]['p']
				XgivenP.append(percentage)
			else:
				XgivenP.append(0)   ##extreme case, barely happen

			if item in list_of_E[index]:
				percentage = list_of_E[index][item]/list_of_E[0]['e']
				XgivenE.append(percentage)
			else:
				XgivenE.append(0)  ##extreme case, barely happen



		
		P_of_x_given_P = XgivenP[0]

		for elem in XgivenP[1:]:
			P_of_x_given_P *= elem

		P_of_x_given_E = XgivenE[0]

		for elem in XgivenE[1:]:
			P_of_x_given_E *= elem


		bayesP = P_of_x_given_P * probP

		bayesE = P_of_x_given_E * probE

		if bayesP>bayesE:
			algorithm_answer.append('p')
		else:
			algorithm_answer.append('e')



	for i in range(len(list_of_correct_answers)):
		if algorithm_answer[i] == list_of_correct_answers[i]:
			correctCount += 1
		
	global per
	per = percentageOfCorrectness(correctCount, totalCount)
	

	return 


def percentageOfCorrectness(correct, totalCount):
	percentage = correct/totalCount
	percentage *= 100
	return percentage




##################################################################
#                                                                 #
#       serves as a temporary main method                         #
#                                                                 #
################################################################## 

general_count = generate_total_count(trainingData)


probE = 0.0
probP = 0.0

probE_probP(general_count)    ##now probability of E and probability of P


constructListforPandE(trainingData)


classify(tesingData,list_of_P,list_of_E)




##################################################################
#                                                                 #
#       output file                                               #
#                                                                 #
################################################################## 


f = open(outputName,"w")

for i in range(len(list_of_correct_answers)):

	f.write("Correct Answer:  " + list_of_correct_answers[i] + "   Answer Computed:  " + algorithm_answer[i] +'\n')
f.write("Percentage of Correctness:  " + str(per))


f.close()









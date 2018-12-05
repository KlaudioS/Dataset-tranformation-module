#########################################
######                             ######
#####  Dataset-tranformation-module #####
######                             ######
#########################################

#©ClaudioSilva
#klaudio.ads@gmail.com


import sys
import csv
import statistics
import re
import os
import urllib.request
import gzip
from urllib.request import urlopen
import datetime
from urllib.error import URLError
from socket import timeout
import os
from copy import deepcopy
import array
import numpy as np
import itertools

#Variable
files = []
attributeList = []
files = []
dataset = []
attCombi= 0
tempDS1 = []
tempDS2 = []
attributeListTemp = []

#Location of Raw CSV files
path = ""

#Create multiple datasets with all possible configurations until max granularity and history
def dsConfig(maxGranularity,maxHourHistory,objectiveID):
	global counter
	allDS = []
	attList = []

	header = 0 
	counter = 0
	monthNum=1
	originalDataset =[]
	files = getFileNames()
	maxMonthNum = len(files)
	allDS = getAllFiles()
	attList = createUsableAttList(allDS[0],objectiveID)
	print("attlist:", attList)
	monthDS = []

	while(monthNum<=maxMonthNum):
		print("Enter")	
		monthDS = addMonths(allDS,monthNum)
		print("monthDS: " ,monthDS)
		print("months: ", len(monthDS))
		for gra in range(4,maxGranularity+1,4):
			print("gra: ",gra) 
			for his in range(1,maxHourHistory+1):
				print("history")
				for norm in range(2):	
					for att in attList:		
						dsCreator(gra,his,att,norm,monthDS,monthNum,objectiveID)
		monthNum += 1
	print("end")
	print("total iterations: " , counter)

#Create a single dataset with specific configuration
def dsCreator(granularity,hourHistory,usableAttributes,norm,originalDataset,monthNum,objectiveID,name):
	global dataset
	global counter
	global granu
	global hourHis

	hourHis = hourHistory
	granu = granularity
	tempDataset = []
	tempDataset2 = []
	tempRow = []
	DS = []
	tempDataset3 = []

	tempDataset = deleteMetrics(usableAttributes,originalDataset)
	tempDataset2 = list(tempDataset) 

	if(granu > 1):	
		tempDataset = granularityIndexer(tempDataset2,granu)
	else:
		tempDataset = tempDataset2
	if(norm == 1):
		tempDataset3 = normalization(tempDataset)
	else:
		tempDataset3=tempDataset
	counter += 1
	if(hourHistory>1):
		DS = history(hourHistory,tempDataset3)
		writeCSV4(DS,monthNum,norm,name)
	else:
		writeCSV4(tempDataset3,monthNum,norm,name)

#Creates a single dataset composed by N months
def addMonths(allDS,monthNumber):
	tempList= []
	addedMonths = []

	for actualMonth in range(monthNumber):
		tempList = list(allDS[actualMonth])
		if(actualMonth != 0):
			del tempList[0]
		addedMonths += tempList	
		tempList = []

	return addedMonths

#Set usable attributes in the dataset
def createUsableAttList(file,objectiveID):
	attributeList = []
	index = 0
	indexers = []
	attsize = len(file[0])
						
	attributeList = list(itertools.product([0, 1], repeat=attsize))
	for att in attributeList:
		if (sum(att) == 0 ) or (att[objectiveID] == 0):
			indexers.append(index)
		index += 1
	for ind in sorted(indexers, reverse=True):
		del attributeList[ind]

	return attributeList

#Delete specific attirbutes
def deleteMetrics(metrics,tempDS):
	indexes = []
	tempDataset = []

	for i in range(len(metrics)):
		if(metrics[i] == 0):
			indexes.append(i)
	for row in tempDS:
		row2 = list(row)
		for index in sorted(indexes, reverse=True):
			del row2[index]
		tempDataset.append(row2)
	tempDS = list(tempDataset)
	tempDataset = []
	
	return tempDS

#Create history for records
def history(hourHistory,allDS):
	tempRow = []
	tempDataset = []
	DS = allDS

	for i in range(1,len(DS)):
		for a in range(hourHistory):
			if(i+hourHistory <= len(DS)):
				for b in range(len(DS[0])):
					tempRow.append(DS[i+a][b])
		if(tempRow != []):
			tempDataset.append(tempRow)
			tempRow=[]
	tempDataset.insert(0,createHistoryHeader(hourHistory,allDS))

	return tempDataset

#Create header for when using history
def createHistoryHeader(hourHistory,allDS):
	header = []
	tempheader = []
	header = allDS[0]

	for a in range(hourHistory):
		for i in range(len(header)):
			tempheader.append(header[i] +"_"+ str(a))

	return tempheader

#Create array with all files of the main directory
def getAllFiles():
	allDS = []
	names = getFileNames()
	originalDataset = []
	for file in names:
		with open(file, 'r') as f:
			reader = csv.reader(f)
			for row in reader:
				tuple(row)
				try:
					row = list(map(int, row))
				except ValueError:
					print("Error: ", ValueError)
				originalDataset.append(row)
		allDS.append(originalDataset)
		originalDataset= []	

	return allDS

#Get all CSV file locations in the main directory
def getOnlyNames():
	names = []

	for file in os.listdir(path):
		if file.endswith(".csv"):
			names.append(file)
	return names

#Get only names of all the CSV files in the main directory
def getFileNames():
	dsnames = []

	for file in os.listdir(path):
		if file.endswith(".csv"):
			dsnames.append(path + file)
	return dsnames

#Normalize dataset using min max
def normalization(allDS):
	dataset= []

	dataset = allDS
	finalDS = []
	normDS = list(dataset)
	label = list(dataset[0])
	DS = []
	del normDS[0]

	x = np.array(normDS).astype(np.float)
	x_normed = x / x.max(axis=0)
	finalDS.append(x_normed)
	DS= finalDS[0].tolist()
	DS.insert(0,label)

	return DS

#Write a dastaset to a CSV file
def writeCSV4(tempDataset,monthNum,norm,name):
	global dataset
	global counter
	global granu
	global hourHis

	print("path: ",path)
	print("file", path+'attNum = '+ str(len(tempDataset[0]))+', gra= '+str(granu)+', hist= '+str(hourHis)+', addMon= '+str(monthNum) +', norm= '+str(norm) +'.csv')
	with open(path+'month= '+name +', gra= '+str(granu)+', hist= '+str(hourHis)+', attNum = '+ str(len(tempDataset[0])) +', addMon= '+str(monthNum) +', norm= '+str(norm) +'.csv', 'a',newline='') as f:
		writer = csv.writer(f)
		for row in tempDataset:
			writer.writerow(row)

#Tranform dataset into N granularity
def granularityIndexer(tmpDS,granu):
	tempDataset = []
	tempRow = []
	tempDS = list(tmpDS)

	for rowIndex in range(1,len(tempDS),granu):
		for columnIndex in range(len(tempDS[0])):
			print("print",tempDS[rowIndex][columnIndex])
			tempItem = float(tempDS[rowIndex][columnIndex])
			for granularityValue in range(1,granu):
				if(rowIndex+granularityValue< len(tempDS)):
					tempItem += float(tempDS[rowIndex+granularityValue][columnIndex])
			tempRow.append(tempItem)
			tempItem = []
		if(rowIndex+granu<= len(tempDS)):
			tempDataset.append(tempRow)
		tempRow = []
	tempDS = list(tempDataset)
	tempDataset = []
	tempDS.insert(0,tmpDS[0])

	return tempDS

#Read configuration parameters from file
def readFromFile():
	config=[]

	for line in open("C:/Users/klaud/Desktop/configuraçao.txt"):
		li=line.strip()
		if not li.startswith("#"):
			config.append(line.rstrip())


	return config

#Use configuration file for 
def dsConfigFile(objectiveID,addMonthBool):
	global counter
	config =[]
	config2 = []
	allDS = []
	attList = []
	gran = [] 
	histo = []
	name = getOnlyNames()


	config = readFromFile()
	del config[0]
	for line in config:
		config2.append(line.split(','))
	
	for a in config2:
		histo.append(int(a[0]))

	for b in config2:
		gran.append(int(b[1]))
	
	header = 0 
	counter = 0
	monthNum=1
	originalDataset =[]
	files = getFileNames()
	maxMonthNum = len(files)
	allDS = getAllFiles()
	attList = createUsableAttList(allDS[0],objectiveID)

	monthDS = []
	while(monthNum<=maxMonthNum):
		if addMonthBool == 0:
			monthDS = deepcopy(allDS[monthNum-1])
		else:
			monthDS = addMonths(allDS,monthNum)
		for gra in set(gran):
			print("granularity: ",gra) 
			for his in set(histo):
				print("history: ",his)
				for norm in range(2):
					print("normalization: ",norm)	
					for att in attList:
						print("attribute: ",att)	
						dsCreator(gra,his,att,norm,monthDS,monthNum,objectiveID,name[monthNum-1])
		
		monthNum += 1

	print("end")
	print("total iterations: " , counter)

#Configure file for future
def dsConfigFileFutureExactly(objectiveID,addMon,non_hour):
	global counter
	config =[]
	config2 = []
	allDS = []
	attList = []
	gran = [] 
	histo = []
	futureTW = []
	name = getOnlyNames()

	config = readFromFile()
	del config[0]
	for line in config:
		config2.append(line.split(','))
	
	for a in config2:
		histo.append(int(a[0]))

	for b in config2:
		gran.append(int(b[1]))

	for c in config2:
		futureTW.append(int(c[2]))

	print("gran: ",gran)
	print("histo: ",histo)
	print("futureTW",futureTW)

	header = 0 
	counter = 0
	monthNum=1
	originalDataset =[]
	files = getFileNames()
	maxMonthNum = len(files)
	allDS = getAllFiles()
	attList = createUsableAttList(allDS[0],objectiveID)
	monthDS = []

	while(monthNum<=maxMonthNum):
		if(addMon == 1):
			monthDS = addMonths(allDS,monthNum)
		else:
			monthDS = addMonths(allDS,1)
		print("MonthDS: len " ,len(monthDS))
		
		for norm in range(2):
			print("norm: ",norm)	
			for att in attList:
				print("att: ",att)
				for i in range(len(config)):
					dsCreatorFuture(int(gran[i]),int(histo[i]),att,norm,monthDS,monthNum,objectiveID,name[monthNum-1],int(futureTW[i]),non_hour)
		monthNum += 1
	print("end")
	print("total iterations: " , counter)

def dsConfigFileFutureCombinations(objectiveID,addMon,non_hour):
	global counter
	config =[]
	config2 = []
	allDS = []
	attList = []
	gran = [] 
	histo = []
	futureTW = []
	name = getOnlyNames()

	config = readFromFile()
	del config[0]
	for line in config:
		config2.append(line.split(','))
	
	for a in config2:
		histo.append(int(a[0]))

	for b in config2:
		gran.append(int(b[1]))

	for c in config2:
		futureTW.append(int(c[2]))

	print("gran: ",gran)
	print("histo: ",histo)
	print("futureTW",futureTW)

	header = 0 
	counter = 0
	monthNum=1
	originalDataset =[]
	files = getFileNames()
	maxMonthNum = len(files)
	allDS = getAllFiles()
	attList = createUsableAttList(allDS[0],objectiveID)
	monthDS = []

	while(monthNum<=maxMonthNum):
		if(addMon == 1):
			monthDS = addMonths(allDS,monthNum)
		else:
			monthDS = addMonths(allDS,1)
		print("MonthDS: len " ,len(monthDS))
		
		for gra in set(gran):
			print("gra: ",gra) 
			for his in set(histo):
				print("history: ",his)
				for norm in range(2):
					print("norm: ",norm)	
					for att in attList:
						print("att: ",att)
						for futureTimeWindow in futureTW:
							print("futTW: ",futureTimeWindow)
							dsCreatorFuture(gra,his,att,norm,monthDS,monthNum,objectiveID,name[monthNum-1],futureTimeWindow,non_hour)
		
		monthNum += 1
	print("end")
	print("total iterations: " , counter)

def dsCreatorFuture(granularity,hourHistory,usableAttributes,norm,originalDataset,monthNum,objectiveID,name,futureTimeWindow,non_hour):
	global dataset
	global counter
	global granu
	global hourHis

	hourHis = hourHistory
	granu = granularity
	tempDataset = []
	tempDataset2 = []
	tempRow = []
	DS = []
	tempDataset3 = []
	tempDataset = deleteMetrics(usableAttributes,originalDataset)
	tempDataset2 = list(tempDataset) 

	if(non_hour == 1 ):
		tempDataset3 = granularityIndexer(tempDataset2,4)
		tempDataset2= tempDataset3
	if(granu > 1):	
		tempDataset = granularityIndexer(tempDataset2,granu)
	else:
		tempDataset = tempDataset2

	if(norm == 1):
		tempDataset3 = normalization(tempDataset)
	else:
		tempDataset3=tempDataset

	counter += 1

	DS = historyFuture(hourHistory,tempDataset3,futureTimeWindow,objectiveID)
	tempDataset3 = futureDS(DS,futureTimeWindow,objectiveID,hourHistory)
	writeCSVFuture(tempDataset3,monthNum,norm,name,futureTimeWindow)


def createHistoryHeaderFuture(hourHistory,allDS,futureTimeWindow,objectiveID):
	header = []
	tempheader = []
	header = allDS[0]


	for a in range(hourHistory):
		for i in range(len(header)):
			tempheader.append(header[i] +"_"+ str(a))
	tempheader.append(header[objectiveID]+"_"+str(futureTimeWindow) +"_OC")

	return tempheader

def historyFuture(hourHistory,allDS,futureTimeWindow,objectiveID):
	tempRow = []
	tempDataset = []
	DS = allDS

	for i in range(1,len(DS)):
		for a in range(hourHistory):
			if(i+hourHistory <= len(DS)):
				for b in range(len(DS[0])):
					tempRow.append(DS[i+a][b])
		if(tempRow != []):
			tempDataset.append(tempRow)
			tempRow=[]
	tempDataset.insert(0,createHistoryHeaderFuture(hourHistory,allDS,futureTimeWindow,objectiveID))

	return tempDataset

def futureDS(allDS,futureTimeWindow,objectiveID,history):
	tempRow = []
	tempDataset = []

	for i in range(1,len(allDS)):
		if(i+futureTimeWindow+history<len(allDS)):
			tempRow = allDS[i]
			tempRow.append(allDS[i+futureTimeWindow+history][0])
			print("tempRow with future", tempRow)
			tempDataset.append(tempRow)
			tempRow =[]
	tempDataset.insert(0,allDS[0])
	return tempDataset

def writeCSVFuture(tempDataset,monthNum,norm,name,futureTimeWindow):
	global dataset
	global counter
	global granu
	global hourHis

	print("path: ",path)
	print("file", path+'attNum = '+ str(len(tempDataset[0]))+', gra= '+str(granu)+', hist= '+str(hourHis)+', addMon= '+str(monthNum) +', futureTW= '+str(futureTimeWindow) +', norm= '+str(norm) +'.csv')

	with open(path+'month= '+name +', gra= '+str(granu)+', hist= '+str(hourHis)+', attNum = '+ str(len(tempDataset[0])) +', addMon= '+str(monthNum) +', futureTW= '+str(futureTimeWindow) +', norm= '+str(norm) +'.csv', 'a',newline='') as f:
		writer = csv.writer(f)
		for row in tempDataset:
			writer.writerow(row)

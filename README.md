# Dataset tranformation module API

The Dataset tranformation module API is a simple and efficient tool to add extra temporal information to time-series datasets, altough it still can be used in any numeric only datasets. The API allows an easy integration in researchers python projects.

##### Disclosure
API stil under development


# Requirements
- python 3.5.2

# API functions

The API comes with a different set of functions that lets the user models its dataset to its needs.

#### Grid search approach
```python
#Create multiple datasets with all possible configurations until max granularity and history
def dsConfig(maxGranularity,maxHourHistory,objectiveID):
```

```python
#Create multiple datasets with all possible configurations until max granularity and history with a range of specific future hours for objective class
def dsCreatorFuture(granularity,hourHistory,usableAttributes,norm,originalDataset,monthNum,objectiveID,name,futureTimeWindow,non_hour):
```


#### Create single dataset
```python
#Create a single dataset with specific configuration
def dsCreator(granularity,hourHistory,usableAttributes,norm,originalDataset,monthNum,objectiveID,name):
```

```python
#Create a single dataset composed by N months
def addMonths(allDS,monthNumber):
```

```python
#Create a single dataset composed by N months and a future hour for objective class
def futureDS(allDS,futureTimeWindow,objectiveID,history):
```

```python
#Tranform dataset into N granularity
def granularityIndexer(tmpDS,granu):
```

```python
#Normalize dataset using min max
def normalization(allDS):
```

#### Configuration functions
```python
#Set usable attributes in the dataset
def createUsableAttList(file,objectiveID):
```

```python
#Delete specific attirbutes
def deleteMetrics(metrics,tempDS):
```

```python
#Create history for records
def history(hourHistory,allDS):
```

```python
#Create header for when using history
def createHistoryHeader(hourHistory,allDS):
```

```python
#Create array with all files of the main directory
def getAllFiles():
```

```python
#Get all CSV file locations in the main directory
def getOnlyNames():
```

```python
#Get only names of all the CSV files in the main directory
def getFileNames():
```

```python
#Create a header for future objective class
def createHistoryHeaderFuture(hourHistory,allDS,futureTimeWindow,objectiveID):
```

```python
#Create a record with specific history containing the future objective class
def historyFuture(hourHistory,allDS,futureTimeWindow,objectiveID):
```

#### Specific tasks

```python
#Write a dastaset to a CSV file
def writeCSV4(tempDataset,monthNum,norm,name):
```

```python
#Write a dastaset with future objective class to a CSV file
def writeCSVFuture(tempDataset,monthNum,norm,name,futureTimeWindow):
```

```python
#Read dataset into memory
def readFromFile():
```

#### File configuration methodologies

```python
#Use configuration to create sets of training and test sets
def dsConfigFile(objectiveID,addMonthBool):
```

```python
#Use configuration to create sets of training and test sets with objective class of a specific hour
def dsConfigFileFutureExactly(objectiveID,addMon,non_hour):
```

```python
##Use configuration to create sets of training and test sets with objective class consisting of a range of specific hours
def dsConfigFileFutureCombinations(objectiveID,addMon,non_hour):
```





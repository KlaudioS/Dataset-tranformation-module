# Dataset transformation API

The Dataset tranformation module API is a simple and efficient tool to add extra temporal information to time-series datasets, altough it still can be used in any numeric only datasets. The API allows an easy integration in researchers python projects.

##### Disclosure
API stil under development


# Requirements
- python 3.5.2

# API functions

The API comes with a different set of functions that lets the user models its dataset to its needs.

#### Grid search functions
```python
#Create multiple datasets with all possible configurations until max granularity and history
def ds_config(maxGranularity,maxHourHistory,objectiveID):
```

```python
#Create multiple datasets with all possible configurations until max granularity and history with a range of specific future hours for objective class
def ds_creator_future(granularity,hourHistory,usableAttributes,norm,originalDataset,monthNum,objectiveID,name,futureTimeWindow,non_hour):
```

#### File configuration functions

```python
#Use configuration to create sets of training and test sets
def ds_config_file(objectiveID,addMonthBool):
```

```python
#Use configuration to create sets of training and test sets with objective class of a specific hour
def ds_config_file_future_exactly(objectiveID,addMon,non_hour):
```

```python
##Use configuration to create sets of training and test sets with objective class consisting of a range of specific hours
def ds_config_file_futureCombinations(objectiveID,addMon,non_hour):
```

#### Create single dataset
```python
#Create a single dataset with specific configuration
def ds_creator(granularity,hourHistory,usableAttributes,norm,originalDataset,monthNum,objectiveID,name):
```

```python
#Create a single dataset composed by N months
def add_months(allDS,monthNumber):
```

```python
#Create a single dataset composed by N months and a future hour for objective class
def future_ds(allDS,futureTimeWindow,objectiveID,history):
```

```python
#Tranform dataset into N granularity
def granularity_indexer(tmpDS,granu):
```

```python
#Normalize dataset using min max
def normalization(allDS):
```

```python
#Delete specific attirbutes
def delete_metrics(metrics,tempDS):
```

```python
#Create history for records
def history(hourHistory,allDS):
```

#### Configuration functions
```python
#Set usable attributes in the dataset
def create_usable_att_list(file,objectiveID):
```

```python
#Create header for when using history
def create_history_header(hourHistory,allDS):
```

```python
#Create array with all files of the main directory
def get_all_files():
```

```python
#Get all CSV file locations in the main directory
def get_only_names():
```

```python
#Get only names of all the CSV files in the main directory
def get_file_names():
```

```python
#Create a header for future objective class
def create_history_header_future(hourHistory,allDS,futureTimeWindow,objectiveID):
```

```python
#Create a record with specific history containing the future objective class
def history_future(hourHistory,allDS,futureTimeWindow,objectiveID):
```

#### Specific tasks

```python
#Write a dastaset to a CSV file
def write_CSV4(tempDataset,monthNum,norm,name):
```

```python
#Write a dastaset with future objective class to a CSV file
def write_CSV_future(tempDataset,monthNum,norm,name,futureTimeWindow):
```

```python
#Read configuration parameters from file
def read_from_file():
```

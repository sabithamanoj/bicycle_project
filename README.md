# Bicycle Project


This repo consist of files which helps to collect information regarding the annotations done by a group of annotators and helps to evaluate the performance by comparing to the reference data. 

Inputs required are:
1. Annotator responses in .json format
2. Reference dataset (with correct response for each task) in json format

## Folder Structure
_____________________

Here is a quick overview of the different folders:

### src
This folder consists of python source code

* tasks.py : This file contains implementations of different evaluation routines (tasks).

* functions.py : This file has a function that calculates the performance of annotators.
_______________________
### classes
* annotation.py contains a class to handle annotation data.
* reference.py contains a class to handle reference data.

_______________________
### results
This folder contains log file and plots.

------------------------------
### tests
This folder contains sample test code.

## requirements.txt
This file contains information about python pakages used in this project.

## How to run:
tasks.py needs 2 input arguments : anonymized.json file and a reference.json file

### Usage:

    $ python3 ./src/tasks.py -h

      usage: tasks.py [-h] -a ANONYMIZED_JSON -r REFERENCE_JSON

      options:
      -h, --help            show this help message and exit
      -a ANONYMIZED_JSON, --anonymized_json ANONYMIZED_JSON
                            The json file with anonymized data
      -r REFERENCE_JSON, --reference_json REFERENCE_JSON
                            The json file with reference data

Example
    
       $ python3 ./src/tasks.py -a '/path/to/annonymized.json' -r '/path/to/reference.json'
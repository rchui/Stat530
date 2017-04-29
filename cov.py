import csv
import sys

csv.field_size_limit(sys.maxsize)

"""Reads in data passed by the user from a CSV file."""
count = 0
fileName = sys.argv[1]
csvArray = {}
with open(fileName) as csvFile:
    reader = csv.reader(csvFile)
    for row in reader:
	row.pop()
	if count != 0:
    	    readRow = [i for i in row]
	    csvArray[readRow[2]] = readRow
	count += 1
    csvFile.close()

"""Find rows to remove."""
rmArray = []
for i in csvArray.keys():
    if csvArray[i][12] == '':
	csvArray[i][12] = -9

"""Read in ped file"""
pedArray = []
for line in open(sys.argv[2]):
    pedArray.append(line.split())

for row in pedArray:
    print(row[0:2])

"""Write to covariate file"""

import csv
import sys

csv.field_size_limit(sys.maxsize)

"""Reads in data passed by the user from a CSV file."""
print("[0%] ... Reading in csv data")
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
print("[25%] ... Marking empty PTSD outcome as missing...")
rmArray = []
count = 0
for i in csvArray.keys():
    if csvArray[i][12] == '':
        count += 1
	csvArray[i][12] = -9
    if csvArray[i][9] == "":
        count += 1
        csvArray[i][9] = -9
print("    Marked " + count + " rows")

"""Read in ped file"""
print("[50%] ... Reading in ped file...")
pedArray = []
count = 0
for line in open(sys.argv[2]):
    print("    Reading in row " + count)
    pedArray.append(line.split())

for row in pedArray:
    print(row[0:2])

"""Write to covariate file"""
print("[75%] ... Writing to covariate file...")

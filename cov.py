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
print("[25%] ... Marking empty outcome rows as missing...")

rmArray = []
count = 0
for i in csvArray.keys():
    if csvArray[i][12] == '':
        count += 1
	csvArray[i][12] = -9
    if csvArray[i][9] == "":
        count += 1
        csvArray[i][9] = -9
    if csvArray[i][15]:
        count += 1
        csvArray[i][15] = -9
    if csvArray[i][51]:
        count += 1
        csvArray[i][51] = -9

print("    Marked " + str(count) + " rows")

"""Read in ped file"""
print("[50%] ... Reading in ped file...")

pedArray = []
count = 0
for line in open(sys.argv[2]):
    count += 1
    print("    Reading in row " + str(count))
    pedArray.append(line.split())

covArray = []
for row in pedArray:
    print("covArray <-- " + str(row[0:2]))
    covArray.append(row[0:2])

"""Build covariate array"""
print("[75%] ... Writing to covariate file...")

def symptoms(start, offset, columns):
    print("    Starting at [" + str(start) + "] with offset [" + str(offset) + "] for [" + str(columns) + "]")
    for i in range(len(covArray)):
        temp = 0
        for j in range(columns):
            temp += int(max(csvArray[covArray[i][1]][start + j], csvArray[covArray[i][1]][start + offset + j]))
        covArray[i].append(temp)
        print("covArray <-- " + str(covArray[i]))

def sumSymptoms():
    for i in range(len(covArray)):
        temp = 0
        for j in range(3):
            temp += covArray[i][2 + j]
        covArray[i].append(temp)
        print("covArray <-- " + str(covArray[i]))

def ptsdOutcome():
    for i in range(len(covArray)):
        if csvArray[covArray[i][1]][4]:
            temp = int(csvArray[covArray[i][1]][9])
        else:
            temp = int(csvArray[covArray[i][1]][12])
        covArray[i].append(temp)
        print("covArray <-- " + str(covArray[i]))

def exposure():
    temp = int(max(csvArray[covArray[i][1]][15], csvArray[covArray[i][1]][51]))
    if temp >= 1 and temp <= 12:
        exposure = 1
    elif temp >= 13 and temp <= 14:
        exposure = 2
    elif temp >= 15 and temp <= 19:
        exposure = 3
    elif temp >= 20:
        exposure = 4
    else:
        exposure = -9
    covArray[i].append(exposure)
    print("covArray <-- " + str(covArray[i]))

symptoms(16, 36, 5)
symptoms(21, 36, 7)
symptoms(28, 36, 5)
sumSymptoms()
ptsdOutcome()

print("[100%] ... Cleaning up")

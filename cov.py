import csv
import sys

csv.field_size_limit(sys.maxsize)

"""Reads in data passed by the user from a CSV file."""
print("[00%] ... Reading in csv data")

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
print("    Read in " + str(count) + " lines")

"""Find rows to remove."""
print("[20%] ... Marking empty outcome rows as missing")

rmArray = []
count = 0
for i in csvArray.keys():
    if csvArray[i][12] == '':
        count += 1
	csvArray[i][12] = -9
    if csvArray[i][9] == '':
        count += 1
        csvArray[i][9] = -9
    if csvArray[i][15] == '':
        count += 1
        csvArray[i][15] = -9
    if csvArray[i][51] == '':
        count += 1
        csvArray[i][51] = -9
    if csvArray[i][7] == '':
        count += 1
        csvArray[i][7] = -9
    if csvArray[i][8] == '':
        count += 1
        csvArray[i][8] = -9
    if csvArray[i][6] == '':
        count += 1
        csvArray[i][6] = -9

print("    Marked " + str(count) + " values as missing")

"""Read in ped file"""
print("[40%] ... Reading in ped file")

pedArray = []
count = 0
for line in open(sys.argv[2]):
    count += 1
    # print("    Reading in row " + str(count))
    pedArray.append(line.split())
print("    Read in " + str(count) + " lines")
covArray = []
for row in pedArray:
    # print("covArray <-- " + str(row[0:2]))
    covArray.append(row[0:2])
print("    Constructed " + str(count) + " line covariate array")

"""Build covariate array"""
print("[60%] ... Adding values to covariate array")

def symptoms(start, offset, columns):
    print("        Starting at [" + str(start) + "] with offset [" + str(offset) + "] for [" + str(columns) + "] values")
    for i in range(len(covArray)):
        temp = 0
        for j in range(columns):
            temp += int(max(csvArray[covArray[i][1]][start + j], csvArray[covArray[i][1]][start + offset + j]))
        covArray[i].append(temp)
        # print("covArray <-- " + str(covArray[i]))

def sumSymptoms():
    for i in range(len(covArray)):
        temp = 0
        for j in range(3):
            temp += covArray[i][2 + j]
        covArray[i].append(temp)
        # print("covArray <-- " + str(covArray[i]))

def ptsdOutcome():
    for i in range(len(covArray)):
        if csvArray[covArray[i][1]][4]:
            temp = int(csvArray[covArray[i][1]][9])
        else:
            temp = int(csvArray[covArray[i][1]][12])
        if temp == 1:
            temp = 2
        elif temp == 0:
            temp = 1
        covArray[i].append(temp)
        # print("covArray <-- " + str(covArray[i]))

def exposure():
    for i in range(len(covArray)):
        temp = int(max(csvArray[covArray[i][1]][15], csvArray[covArray[i][1]][51]))
        if temp >= 1 and temp <= 12:
            exposure = 1
        elif temp >= 13 and temp <= 14:
            exposure = 2
        elif temp >= 15 and temp <= 19:
            exposure = 3
        elif temp == 31:
            exposure = 4
        else:
            exposure = -9
        covArray[i].append(exposure)
        # print("covArray <-- " + str(covArray[i]))

def eventType():
    for i in range(len(covArray)):
        temp = int(max(csvArray[covArray[i][1]][15], csvArray[covArray[i][1]][51]))
        if temp >= 1 and temp <= 7:
            event = 1
        elif temp >= 8 and temp <= 14:
            event = 2
        elif temp >= 15 and temp <= 18:
            event = 3
        elif temp == 19:
            event = 4
        elif temp == 31:
            event = 5
        else:
            event = -9
        covArray[i].append(event)
        # print("covArray <-- " + str(covArray[i]))

def race():
    for i in range(len(covArray)):
        covArray[i].append(int(csvArray[covArray[i][1]][6]))
        # print("covArray <-- " + str(covArray[i]))

def age():
    for i in range(len(covArray)):
        temp = int(max(csvArray[covArray[i][1]][7], csvArray[covArray[i][1]][8]))
        covArray[i].append(temp)
        # print("covArray <-- " + str(covArray[i]))

def sex():
    for i in range(len(covArray)):
        temp = int(csvArray[covArray[i][1]][5])
        if temp == 1:
            temp = 2
        elif temp == 2:
            temp = 1
        covArray[i].append(temp)
        # print("covArray <-- " + str(covArray[i]))

print("    Adding symptom 1 scores")
symptoms(16, 36, 5)
print("    Adding symptom 2 scores")
symptoms(21, 36, 7)
print("    Adding symptom 3 scores")
symptoms(28, 36, 5)
print("    Adding summed symptom score")
sumSymptoms()
print("    Adding PTSD outcome")
ptsdOutcome()
print("    Adding exposure type")
exposure()
print("    Adding event type")
eventType()
print("    Adding coded race values")
race()
print("    Adding ages")
age()
print("    Adding coded sex values")
sex()

""" Write to covariate file """
print("[80%] ... Writing to covariate file")

print("    Opening covariate file")
covFile = open(sys.argv[3], 'w')
covFile.write("FID IID REE AVO ARO SEV OUT EXP EVE RAC AGE SEX\n")
for i in range(len(covArray)):
    covFile.write(covArray[i][0])
    for j in range(len(covArray[i]) - 1):
        j += 1
        covFile.write(" " + str(covArray[i][j]))
    covFile.write("\n")
covFile.close()
print("    Closing covariate file")

print("[100%] ... Cleaning up")

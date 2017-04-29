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
	if csvArray[row[1]][5] == 1:
		row[4] = 2
	else:
		row[4] = 1

	if csvArray[row[1]][12] == 0:
		row[5] = 1
	else:
		row[5] = 2

file = open(sys.argv[3], 'a')
output = ""
for row in pedArray:
	output = str(row[0])
	for i in range(len(row)):
		if i != 0:
			output += " " + str(row[i])
	output += "\n"
	file.write(output)

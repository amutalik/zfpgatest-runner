import argparse
from operator import contains
from bitarray import bitarray
from bitarray.util import int2ba
import csv

FILE = 0
EXPECTED = 1
RECEIVED = 2
R_W = 3
BIT_NO = 4
ERROR_TYPE = 5

TestSummaryHeader = ['FILE', 'EXPECTED', 'RECEIVED', 'R/W', 'BIT NO.', 'ERROR TYPE']

#parser = argparse.ArgumentParser()
#parser.add_argument("inputFiles", type=str)
#args = parser.parse_args()

#filesList = open(args.inputFiles, "r")

filesList = open("tests/inputFiles.txt", "r")
files = filesList.read().splitlines()

testSummaryRows = []


for fileName in files:
    testFile = open(fileName, "r")
    lines = testFile.readlines()

    errorFound = False

    for index, line in enumerate(lines):

        if "CheckLastResponseWithFile" in line:

            if errorFound:
                r_w_Error = "W" if "ERROR" in line else "R"
                errorFound = False

                for x, wrongbit in enumerate(wrongBits):
                    row = [testFile.name.split("/")[1], expectedHexFormatted, receivedHexFormatted, r_w_Error, wrongbit, wrongBitsInfo[x]]
                    testSummaryRows.append(row)
                    del row

            else:
                if "ERROR" in line:
                    errorFound = True

                    expectedHexOrig = lines[index+1].split("'")[3]
                    receivedHexOrig = lines[index+1].split("'")[5]
                    expectedHexFormatted = expectedHexOrig[2:4] + expectedHexOrig[0:2]
                    receivedHexFormatted = receivedHexOrig[2:4] + receivedHexOrig[0:2]
                    expectedInt = int(expectedHexFormatted, 16)
                    receivedInt = int(receivedHexFormatted, 16)
                    
                    diff = expectedInt ^ receivedInt
                    diffBitList = list(int2ba(diff))[::-1]
                    
                    expectedBitList = list(int2ba(expectedInt, 16))[::-1]

                    wrongBits = []
                    wrongBitsInfo = []
                    for idx,bit in enumerate(diffBitList):
                        if bit:
                            wrongBits.append(idx)
                            wrongBitsInfo.append("1 to 0") if expectedBitList[idx] else wrongBitsInfo.append("0 to 1")
                

filesList.close()


testSummaryFile = open("TestSummary.csv", "w")
testSummaryFileWriter = csv.writer(testSummaryFile)
testSummaryFileWriter.writerow(TestSummaryHeader)
testSummaryFileWriter.writerows(testSummaryRows)
testSummaryFile.close()



bitFailSummaryHeader = ["TOTAL FAILS", "READ FAILS", "WRITE FAILS", "H to L FAILS", "L TO H FAILS"]

TOTAL_FAILS = 0
READ_FAILS = 1
WRITE_FAILS = 2
H_TO_L_FAILS = 3
L_TO_H_FAILS = 4

bitFailInfo = [0]*5
bitFailSummary = []
for x in range(16):
    bitFailSummary.append(bitFailInfo.copy())

for row in testSummaryRows:
    bit = row[BIT_NO]
    bitFailSummary[bit][TOTAL_FAILS] += 1
    if "R" in row[R_W]:
        bitFailSummary[row[BIT_NO]][READ_FAILS] += 1
    else:
        bitFailSummary[row[BIT_NO]][WRITE_FAILS] += 1
    if "1 to 0" in row[ERROR_TYPE]:
        bitFailSummary[row[BIT_NO]][H_TO_L_FAILS] += 1
    else:
        bitFailSummary[row[BIT_NO]][L_TO_H_FAILS] += 1

bitFailSummaryFile = open("BitFailSummary.csv", "w")
bitFailSummaryFileWriter = csv.writer(bitFailSummaryFile)
bitFailSummaryFileWriter.writerow(bitFailSummaryHeader)
bitFailSummaryFileWriter.writerows(bitFailSummary)
bitFailSummaryFile.close()
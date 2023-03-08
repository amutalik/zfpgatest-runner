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

    for lineNumber, thisLine in enumerate(lines):

        if "CheckLastResponseWithFile" in thisLine:

            if errorFound:
                rwErrorType = "W" if "ERROR" in thisLine else "R"
                errorFound = False

                for y, erroInfo in enumerate(totalWrongBits):
                
                    for x, wrongbit in enumerate(erroInfo):
                        row = [testFile.name.split("/")[1], totalExpectedHexFormatted[y], totalReceivedHexFormatted[y], rwErrorType, wrongbit, totalWrongBitsInfo[y][x]]
                        testSummaryRows.append(row)
                        del row

            else:
                if "ERROR" in thisLine:
                    errorFound = True

                    totalWrongBits = []
                    totalWrongBitsInfo = []
                    totalExpectedHexFormatted = []
                    totalReceivedHexFormatted = []
                    nextline = lineNumber+1
                    while "Expected" in lines[nextline]:
                        expectedHexOrig = lines[nextline].split("'")[3]
                        receivedHexOrig = lines[nextline].split("'")[5]
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

                        totalWrongBits.append(wrongBits)
                        totalWrongBitsInfo.append(wrongBitsInfo)
                        totalExpectedHexFormatted.append(expectedHexFormatted)
                        totalReceivedHexFormatted.append(receivedHexFormatted)

                        nextline += 1

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
import argparse
from operator import contains
from bitarray import bitarray
from bitarray.util import int2ba
import csv

summaryHeader = ['File Name', 'Expected', 'Received', 'R/W', 'Bit No.', 'Error Type']

parser = argparse.ArgumentParser()
parser.add_argument("inputFile", type=str)
args = parser.parse_args()

resultsFile = open(args.inputFile, "r")
summaryFile = open("TestSummary.txt", "w")
summaryFileWriter = csv.writer(summaryFile)
summaryFileWriter.writerow(summaryHeader)

#resultsFile = open("TestFile.txt", "r")
lines = resultsFile.readlines()

row = []


errorFound = False
totalReadErrors = 0
totalWriteErrors = 0

for index, line in enumerate(lines):
    if "CheckLastResponseWithFile" in line:
        if errorFound:
            if "OK" in line:
                totalReadErrors += 1  
                errorType = "R"
            if "ERROR" in line:
                totalWriteErrors += 1
                errorType = "W"
            errorFound = False


            for x, wrongbit in enumerate(wrongBits):
                row.clear()
                row.append(args.inputFile)
                row.append(expectedHexFormatted)
                row.append(receivedHexFormatted)
                row.append(errorType)
                row.append(wrongbit)
                row.append(wrongBitsInfo[x])
                summaryFileWriter.writerow(row)

        else:
            if "ERROR" in line:
                errorFound = True

                expectedHexOrig = lines[index+1].split("'")[3]
                receivedHexOrig = lines[index+1].split("'")[5]
                expectedHexFormatted = expectedHexOrig[2:4] + expectedHexOrig[0:2]
                receivedHexFormatted = receivedHexOrig[2:4] + receivedHexOrig[0:2]
                expectedInt = int(expectedHexFormatted, 16)
                receivedInt = int(receivedHexFormatted, 16)
                print("expectedHex", "\t", expectedHexFormatted, "\t", "receivedHex", "\t", receivedHexFormatted)
                
                diff = expectedInt ^ receivedInt
                diffBitList = list(int2ba(diff))[::-1]
                
                expectedBitList = list(int2ba(expectedInt))[::-1]

                print("Wrong bits are: ", "\t")
                wrongBits = []
                wrongBitsInfo = []
                for idx,bit in enumerate(diffBitList):
                    if bit:
                        wrongBits.append(idx)
                        if expectedBitList[idx]:
                            wrongBitsInfo.append("1 to 0")
                            print("bit No.-", idx, "\t", "Expected '1' received '0'")
                        else:
                            wrongBitsInfo.append("0 to 1")
                            print("bit No.-", idx, "\t", "Expected '0' received '1'")
                

print("totalReadErrors:", "\t", totalReadErrors, "\t", "totalWriteErrors:", "\t", totalWriteErrors)


resultsFile.close()
summaryFile.close()

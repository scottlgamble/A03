#!/usr/bin/env python

import csv
import subprocess

def saveDict(dictList,name):
    with open(name+ ".csv", "w") as outfile:
        for row in dictList:
            fp = csv.DictWriter(outfile, dictList[0].keys())
            fp.writeheader()
            fp.writerows(dictList)
        
def readDict(name):

    with open(name+ ".csv") as f:
        f_csv = csv.DictReader(f)
        dictList = []
        for row in f_csv:
            row = [row]
            dictList.extend(row)
    return dictList

def getClipboardData():
    p = subprocess.Popen(['pbpaste'], stdout=subprocess.PIPE)
    retcode = p.wait()
    data = p.stdout.read()
    return data

def setClipboardData(data):
    p = subprocess.Popen(['pbcopy'], stdin=subprocess.PIPE)
    p.stdin.write(data)
    p.stdin.close()
    retcode = p.wait()
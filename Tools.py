import csv
import glob
import os
# def mergeCSVremoveDupes(folder)
os.chdir('/Users/scottgamble/Downloads/New Folder With Items/')
files = glob.glob("*.csv")

merged_rows = set()
for f in files:
    with open(f, 'rb') as csv_in:
        csvreader = csv.reader(csv_in, delimiter=',')
        for row in csvreader:
            merged_rows.add(tuple(row))
with open('output.csv', 'wb') as csv_out:
    csvwriter = csv.writer(csv_out, delimiter=',')
    csvwriter.writerows(merged_rows)
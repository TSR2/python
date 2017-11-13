


import csv
with open('C:/Users/TSR/Desktop/project data\ptt_tag_V1.csv', newline='') as csvfile:
    spamreader = csv.reader(csvfile)
    for row in spamreader:
        print(', '.join(row))
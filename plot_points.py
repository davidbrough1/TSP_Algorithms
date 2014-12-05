from __future__ import division
import numpy as np
import matplotlib.pyplot as plt


import csv
from os import listdir
from os.path import isfile, join
import sys

	

mypath = "/home/davinciwin/Algos/Amish_data"
output_path = "/home/davinciwin/Algos"
onlyfiles = [ f for f in listdir(mypath) if isfile(join(mypath,f)) ]

error = []
time = dict()
quality = sys.argv[1]
name = sys.argv[2]
optimum = int(sys.argv[3])
for i in range(len(onlyfiles)):
	
	input_file_reader = csv.reader(open(mypath+"/"+onlyfiles[i]),delimiter = ',')
	counter = 0
	row_error=[]
	row_time=[]
	for row in input_file_reader:
		temp_error = (int(row[1])-optimum)/optimum
		row_error.append((int(row[1])-optimum)/optimum)
		time[temp_error] = float(row[0])
		#print row[1]
		counter +=1
	error.append(row_error)
	#time.append(row_time)
	#print error
	#print row_error
storage_time = []
print len(error),len(row_error)


for row in error:
	print row
	for j in range(len(row)):
		if(row[j] < float(quality)):
			print row[j]
			storage_time.append(time[row[j]])
			
			
			break
storage_time.sort()
#print storage_time

output_file = open(output_path+"/"+"results"+"_"+name+quality+str(optimum)+".txt",'w')

test = int(storage_time[0])
test_array = []
count_array = []
while(test<int(max(storage_time)+2)):
	count = 0
	for m in range(len(storage_time)):
		if(storage_time[m]<test):
			count+=1
	output_file.write(str(test)+","+str(count/10)+"\n")
	test_array.append(test)
	count_array.append(count/10)
	test+=1

plt.plot(test_array,count_array)
plt.show()


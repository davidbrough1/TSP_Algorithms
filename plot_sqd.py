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

error = dict()
only_error = []
quality = float(sys.argv[1])
name = sys.argv[2]
optimum = int(sys.argv[3])
for i in range(len(onlyfiles)):
	
	input_file_reader = csv.reader(open(mypath+"/"+onlyfiles[i]),delimiter = ',')
	counter = 0
	row_error=[]
	row_time=[]
	for row in input_file_reader:
		if(float(row[0]) > quality):
			print row[0],quality
			error[row[0]] = (int(row[1])-optimum)/optimum
			only_error.append((int(row[1])-optimum)/optimum)
			break
		#print row[1]
		
storage_time = []
print only_error



only_error.sort()
#print storage_time

output_file = open(output_path+"/"+"results"+"_"+name+str(quality)+str(optimum)+"sqd.txt",'w')

counter = -1
test = only_error[0]
test_array = []
count_array = []
while(test<float(max(only_error))):
	counter+=1
	test = only_error[counter]
	count = 0
	for m in range(len(only_error)):
		if(only_error[m]<=test):
			count+=1
	output_file.write(str(test)+","+str(count/10)+"\n")
	test_array.append(test)
	count_array.append(count/10)

	

#plt.plot(test_array,count_array)
#plt.show()


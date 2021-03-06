import fileinput
import yaml
import subprocess
import os
import numpy as np

source = 'data/tutorials/shapes/'

f = "data/tutorials/shapes/CutScan.yaml"

with open(f, 'r') as f_in:
        dataMap = yaml.load(f_in)
        #dataMap = yaml.safe_load(f)

variables = dataMap['variables2D']

AllOutFile = open("Significance_Output_inclusive.txt","w")

for i in range(0,len(variables)):
        # Printing the variable name
        Varlen = len(variables[i]['name'])
        pline1 = "====        "+variables[i]['name']+"        ===="
        pline2 = "="*len(pline1)
        print pline2,"\n",pline1,"\n",pline2


	var = variables[i]['name']
	SigOutFile = open("Significance_Output_"+var+".txt","w")
	
	print(var+"\tWV(EWK)\taQGC")
        SigOutFile.write(pline2+"\n"+pline1+"\n"+pline2+"\n")
	SigOutFile.write(var+"\tSignificance\taQGC\n")
        AllOutFile.write(pline2+"\n"+pline1+"\n"+pline2+"\n")
	AllOutFile.write(var+"\tSignificance\taQGC\n")

	for cut1 in np.arange(variables[i]['iRange'], variables[i]['fRange'], variables[i]['step1']):
	   for cut2 in np.arange(variables[i]['fRange'], variables[i]['uRange'], variables[i]['step2']):
		os.system('cp data/tutorials/shapes/limits_vvjj_wv_13TeV2016.txt data/tutorials/shapes/limits_temp.txt')
		os.system('cp data/tutorials/shapes/limits_vvjj_wv_13TeV2016_aQGC.txt data/tutorials/shapes/limits_aQGC_temp.txt')
		#OutRootFileName = 'histo_El_'+str(variables[i]['name'])+'_'+(str(cut).replace(".","_")).replace("-","_")+'.root'
		OutRootFileName = 'histo_El_'+str(variables[i]['tag'])+'_'+(str(cut1).replace(".","_")).replace("-","_")+'_'+(str(cut2).replace(".","_")).replace("-","_")+'.root'
		os.system("sed -i 's/histo_El_SCut.root/"+OutRootFileName+"/' data/tutorials/shapes/limits_temp.txt")
		os.system("sed -i 's/histo_El_SCut.root/"+OutRootFileName+"/' data/tutorials/shapes/limits_aQGC_temp.txt")
		output = subprocess.check_output("combine -d data/tutorials/shapes/limits_temp.txt -M ProfileLikelihood --significance -t -1 --expectSignal=1 | grep Significance: | awk '{print $2}'", shell=True)
		output_aQGC = subprocess.check_output("combine -d data/tutorials/shapes/limits_aQGC_temp.txt -M ProfileLikelihood --significance -t -1 --expectSignal=1 | grep Significance: | awk '{print $2}'", shell=True)
		#print("combine -d data/tutorials/shapes/limits_temp.txt -M ProfileLikelihood --significance -t -1 --expectSignal=1 -S 0")
		#output_aQGC = "1.0"
		SigOutFile.write(str(cut1)+"-"+str(cut2)+"\t"+output.strip()+"\t"+output_aQGC.strip()+"\n")
		AllOutFile.write(str(cut1)+"-"+str(cut2)+"\t"+output.strip()+"\t"+output_aQGC.strip()+"\n")
		print cut1,"-",cut2,"\t",output.strip(),"\t",output_aQGC.strip()
	SigOutFile.close()			
	AllOutFile.write("\n\n")
	os.system('sort Significance_Output_'+var+'.txt'+' -n > temp.txt')
	os.system('mv temp.txt  Significance_Output_'+var+'.txt')
AllOutFile.close()	

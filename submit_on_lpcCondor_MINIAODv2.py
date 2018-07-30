#! /usr/bin/env python
import os
import glob
import math
from array import array
import sys
import time
import subprocess
import tarfile
import datetime
import commands

currentDir = os.getcwd();
CMSSWDir =  currentDir+"/../";

TestRun = 0

lumi = 35900.0

changes = raw_input("\n\nWrite change summary: ")

print "==> ",changes

# Get date and time for output directory
## ADD "test" IN OUTPUT FOLDER IF YOU ARE TESTING SO THAT LATER YOU REMEMBER TO WHICH DIRECTORY YOU HAVE TO REMOVE FROM EOS
if TestRun:
	# /eos/uscms/store/user/rasharma/Limit_Logs
	outputFolder = "/store/user/rasharma/Limit_Logs/LepCut_50GeV_WVZVCombined_"+datetime.datetime.now().strftime('%Y_%m_%d_%Hh%M')+"_TEST/";
	OutputLogPath = "OutPut_Logs/LepCut_50GeV_WVZVCombined_" + datetime.datetime.now().strftime('%Y_%m_%d_%Hh%M') + "_TEST";
else:
	outputFolder = "/store/user/rasharma/Limit_Logs/LepCut_50GeV_WVZVCombined_"+datetime.datetime.now().strftime('%Y_%m_%d_%Hh%M')+"/";
	OutputLogPath = "OutPut_Logs/LepCut_50GeV_WVZVCombined_" + datetime.datetime.now().strftime('%Y_%m_%d_%Hh%M')+"/";

print "Name of output dir: ",outputFolder
# create a directory on eos
os.system('xrdfs root://cmseos.fnal.gov/ mkdir ' + outputFolder)
# create directory in pwd for log files
os.system('mkdir -p ' + OutputLogPath + "/Logs")

def exclude_function(filename):
   if filename.endswith('.stdout' or '.log'):
   	return True
   else:
   	return False

# Function to create a tar file
def make_tarfile(output_filename, source_dir):
    with tarfile.open(output_filename, "w:gz") as tar:
            tar.add(source_dir, arcname=os.path.basename(source_dir), exclude=exclude_function)

# Get CMSSW directory path and name
cmsswDirPath = commands.getstatusoutput('echo ${CMSSW_BASE}')
CMSSWRel = os.path.basename(cmsswDirPath[1])

print "CMSSW release used : ",CMSSWRel

# create tarball of present working CMSSW base directory
os.system('rm CMSSW*.tgz')
make_tarfile(CMSSWRel+".tgz", cmsswDirPath[1])

# send the created tarball to eos
os.system('xrdcp -f ' + CMSSWRel+".tgz" + ' root://cmseos.fnal.gov/'+outputFolder+'/' + CMSSWRel+".tgz")

os.system('echo "Add git diff to file logs." > mypatch.patch')
os.system('git diff >> mypatch.patch')
os.system("sed -i '1s/^/Changes Summary : "+changes+"\\n/' mypatch.patch")
os.system('echo -e "\n\n============\n== Latest commit number \n\n" >> mypatch.patch ')
os.system('git log -1 --format="%H" >> mypatch.patch ')
os.system('xrdcp -f mypatch.patch root://cmseos.fnal.gov/'+outputFolder+'/mypatch.patch')


inputlist = "runstep2condor.sh, submit_condor.py"


command = "python submit_condor.py $*";

outScript = open("runstep2condor.sh","w");
outScript.write('#!/bin/bash');
outScript.write("\n"+'echo "Starting job on " `date`');
outScript.write("\n"+'echo "Running on: `uname -a`"');
outScript.write("\n"+'echo "System software: `cat /etc/redhat-release`"');
outScript.write("\n"+'source /cvmfs/cms.cern.ch/cmsset_default.sh');
outScript.write("\n"+'### copy the input root files if they are needed only if you require local reading');
outScript.write("\n"+'xrdcp -s root://cmseos.fnal.gov/'+outputFolder + '/'+CMSSWRel +'.tgz  .');
outScript.write("\n"+'tar -xf '+ CMSSWRel +'.tgz' );
outScript.write("\n"+'rm '+ CMSSWRel +'.tgz' );
outScript.write("\n"+'cd ' + CMSSWRel + '/src/CombinedEWKAnalysis/CommonTools/test' );
outScript.write("\n"+'echo "====> List files : " ');
outScript.write("\n"+'ls -alh');
outScript.write("\n"+'scramv1 b ProjectRename');
outScript.write("\n"+'eval `scram runtime -sh`');
outScript.write("\n"+'echo "====> List files : " ');
outScript.write("\n"+'ls -alh');
outScript.write("\n"+command);
outScript.write("\n"+'echo "====> List files : " ');
outScript.write("\n"+'ls -alh');
outScript.write("\n"+'echo "====> List root files : " ');
#outScript.write("\n"+'xrdcp -f *.log root://cmseos.fnal.gov/' + outputFolder);
outScript.write("\n"+'cd ${_CONDOR_SCRATCH_DIR}');
outScript.write("\n"+'rm -rf ' + CMSSWRel);
outScript.write("\n");
outScript.close();
os.system("chmod 777 runstep2condor.sh");

outJDL = open("runstep2condor.jdl","w");
outJDL.write("Executable = runstep2condor.sh\n");
outJDL.write("Universe = vanilla\n");
#outJDL.write("Requirements =FileSystemDomain==\"fnal.gov\" && Arch==\"X86_64\"");
outJDL.write("Notification = ERROR\n");
outJDL.write("Should_Transfer_Files = YES\n");
outJDL.write("WhenToTransferOutput = ON_EXIT\n");
#outJDL.write("include : list-infiles.sh |\n");
outJDL.write("Transfer_Input_Files = "+inputlist+"\n");
outJDL.write("x509userproxy = $ENV(X509_USER_PROXY)\n");

    #MC
import os

aQGCpars = {	'fs0':[5.5, 5.8, 6.0, 6.2, 6.4, 6.6, 7.0, 7.5, 8.0, 8.5, 9.0, 9.5, 10.0, 10.5, 11.0], 
		'fs1':[4.87, 4.89, 4.9, 5.0, 5.05, 5.1, 5.15, 5.2, 5.3, 5.4, 5.5, 5.6, 5.7, 5.8, 5.9, 6.0, 6.1, 6.2, 6.3, 6.4, 6.5, 6.6, 7.0, 7.5, 8.0, 8.5, 9.0, 9.5, 10.0, 11.0, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31], 
		#'fs1':[4.8, 4.825, 4.85, 4.875, 4.9, 4.925, 4.95, 4.975, 5, 5.025, 5.05, 5.075, 5.1, 5.125, 5.15, 5.175, 5.2, 5.225, 5.25, 5.275, 5.3, 5.325, 5.35, 5.375, 5.4, 5.425, 5.45, 5.475, 5.5, 5.525, 5.55, 5.575, 5.6, 5.625, 5.65, 5.675, 5.7, 5.725, 5.75, 5.775, 5.8, 5.825, 5.85, 5.875, 5.9, 5.925, 5.95, 5.975, 6, 6.025, 6.05, 6.075, 6.1, 6.125, 6.15, 6.175, 6.2, 6.225, 6.25, 6.275, 6.3, 6.325, 6.35, 6.375, 6.4, 6.425, 6.45, 6.475, 6.5, 6.525, 6.55, 6.575, 6.6, 6.625, 6.65, 6.675, 6.7, 6.725, 6.75, 6.775, 6.8, 6.825, 6.85, 6.875, 6.9, 6.925, 6.95, 6.975, 7, 7.025, 7.05, 7.075, 7.1, 7.125, 7.15, 7.175, 7.2, 7.225, 7.25, 7.275, 7.3, 7.325, 7.35, 7.375, 7.4, 7.425, 7.45, 7.475, 7.5, 7.525, 7.55, 7.575, 7.6, 7.625, 7.65, 7.675, 7.7, 7.725, 7.75, 7.775, 7.8, 7.825, 7.85, 7.875, 7.9, 7.925, 7.95, 7.975, 8, 8.025, 8.05, 8.075, 8.1, 8.125, 8.15, 8.175, 8.2, 8.225, 8.25, 8.275, 8.3, 8.325, 8.35, 8.375, 8.4, 8.425, 8.45, 8.475, 8.5, 8.525, 8.55, 8.575, 8.6, 8.625, 8.65, 8.675, 8.7, 8.725, 8.75, 8.775, 8.8, 8.825, 8.85, 8.875, 8.9, 8.925, 8.95, 8.975, 9, 9.025, 9.05, 9.075, 9.1, 9.125, 9.15, 9.175, 9.2, 9.225, 9.25, 9.275, 9.3, 9.325, 9.35, 9.375, 9.4, 9.425, 9.45, 9.475, 9.5, 9.525, 9.55, 9.575, 9.6, 9.625, 9.65, 9.675, 9.7, 9.725, 9.75, 9.775, 9.8, 9.825, 9.85, 9.875, 9.9, 9.925, 9.95, 9.975, 10, 10.025, 10.05, 10.075, 10.1, 10.125, 10.15, 10.175, 10.2, 10.225, 10.25, 10.275, 10.3, 10.325, 10.35, 10.375, 10.4, 10.425, 10.45, 10.475, 10.5, 10.525, 10.55, 10.575, 10.6, 10.625, 10.65, 10.675, 10.7, 10.725, 10.75, 10.775, 10.8, 10.825, 10.85, 10.875, 10.9, 10.925, 10.95, 10.975, 11, 11.025, 11.05, 11.075, 11.1, 11.125, 11.15, 11.175, 11.2, 11.225, 11.25, 11.275, 11.3, 11.325, 11.35, 11.375, 11.4, 11.425, 11.45, 11.475, 11.5, 11.525, 11.55, 11.575, 11.6, 11.625, 11.65, 11.675, 11.7, 11.725, 11.75, 11.775, 11.8, 11.825, 11.85, 11.875, 11.9, 11.925, 11.95, 11.975],
		'ft0':[0.17, 0.18, 0.19, 0.20, 0.22, 0.26, 0.3, 0.32, 0.34, 0.36,0.40, 0.41, 0.42, 0.44, 0.46, 0.48, 0.50, 0.52, 0.54, 0.56, 0.58, 0.60, 0.62, 0.68, 0.70, 0.72, 0.74, 0.76, 0.78, 0.8, 0.82, 0.84, 0.86, 0.88, 0.90, 0.92, 0.94, 0.96, 0.98, 1.0, 1.02, 1.04, 1.06, 1.08, 1.10, 1.12, 1.14, 1.16, 1.18, 1.20, 1.22, 1.24, 1.26, 1.28, 1.30, 1.32, 1.34, 1.36, 1.38, 1.40, 1.42, 1.44, 1.46, 1.48, 1.50, 1.52, 1.54, 1.56, 1.58, 1.60, 1.62, 1.64, 1.66, 1.68, 1.70, 1.72, 1.74, 1.76, 1.78, 1.80, 1.82, 1.84, 1.86, 1.88, 1.90, 1.92, 1.94, 1.96, 1.98, 2.00], 
		'ft1':[0.17, 0.18, 0.19, 0.20, 0.22, 0.24, 0.28, 0.30, 0.33, 0.36, 0.38, 0.40, 0.45, 0.50,0.6,0.7], 
		'ft2':[0.4, 0.6, 0.8, 0.9, 1.0, 1.2, 1.5],
		'fm0':[1.1, 1.4, 1.8, 2.2, 2.7, 3.2, 3.7, 4.2, 4.7, 5.2, 6.0, 7.0, 8.0,9.0], 
		'fm1':[3.0, 3.5, 4.0, 4.5, 5.0, 5.5, 6.0, 6.5, 7.0, 7.5, 8.0,9.0,10.0, 12.0], 
		'fm6':[2.0, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0, 5.5, 6.0, 6.5, 7.0, 8.0, 9.0, 10.0, 12.0], 
		'fm7':[5.0, 5.5, 5.7, 5.9, 6.0, 6.1, 6.2, 6.3, 6.4, 6.5, 6.7, 7.0, 7.5, 8.0, 8.5, 9.0, 9.5, 10.0, 11.0, 12.0, 13.0, 14.0, 15.0]
		}

dataPath = "$CMSSW_BASE/src/CombinedEWKAnalysis/CommonTools/data/anomalousCoupling/"
#configFile = "config_TF1_wv_plain_my"
configFile = ["config_TF1_wv_plain_my","config_TF1_wv_plain_my_ZV"]

LimitFile = "Limits_mass"

os.system("rm Limits.log")

#for mass in ['', '_M1000', '_1500', '_2000', '_2500', '_3000', '_3500', '_4000', '_4500', '_5000']:
#for mass in ['_2500', '_3000', '_3500', '_4000', '_4500', '_5000']:
#for mass in ['_2500', '_3000', '_3500', '_4000',]:
#for mass in ['', '_2500', '_3000', '_3500', '_4000', '_4500', '_5000']:
#for mass in ['',  '_4500']:
#for mass in ['', '_3000', '_3500', '_4000']:
#for mass in ['','_5000','_4500']:
for mass in ['_4000','_3500','_3000','_2500']:
	for pars, value in aQGCpars.iteritems():
	  if pars != 'fs0':
	    if mass == '_4000': continue;
	  for val in value:
	    outJDL.write("Output = "+OutputLogPath+"/"+   str(pars)+"_"+str(val)+"_"+str(val)+"_"+mass+".stdout\n");
	    outJDL.write("Error  = "+OutputLogPath+"/"+   str(pars)+"_"+str(val)+"_"+str(val)+"_"+mass+".stdout\n");
	    outJDL.write("Log  = "+OutputLogPath+"/Logs/"+str(pars)+"_"+str(val)+"_"+str(val)+"_"+mass+".log\n");
	    if mass == '':
	    	outJDL.write('Arguments =  -r -'+str(val)+' '+ str(val) + '  -l ' + LimitFile+mass+'_'+str(pars)+'_'+str(val)+"_"+str(val)+'.log' + ' -a ' + pars + '  -p ' + dataPath + '  -c ' + configFile[0] + ' ' + configFile[1] + '  \n')
	    else:
	    	outJDL.write('Arguments =  -r -'+str(val)+' '+ str(val) + '  -l ' + LimitFile+mass+'_'+str(pars)+'_'+str(val)+"_"+str(val)+'.log' + ' -a ' + pars + '  -p ' + dataPath + '  -c ' + configFile[0] + ' ' + configFile[1]  + '  -m '+ mass + ' \n')
	    outJDL.write("Queue\n");

outJDL.close();
print "===> Set Proxy Using:";
print "\tvoms-proxy-init --voms cms --valid 168:00";
print "\"condor_submit runstep2condor.jdl\" to submit";


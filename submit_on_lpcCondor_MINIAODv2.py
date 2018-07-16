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
	outputFolder = "/store/user/rasharma/Limit_Logs/M5000_"+datetime.datetime.now().strftime('%Y_%m_%d_%Hh%M')+"_TEST/";
	OutputLogPath = "OutPut_Logs/M5000_" + datetime.datetime.now().strftime('%Y_%m_%d_%Hh%M') + "_TEST";
else:
	outputFolder = "/store/user/rasharma/Limit_Logs/M5000_"+datetime.datetime.now().strftime('%Y_%m_%d_%Hh%M')+"/";
	OutputLogPath = "OutPut_Logs/M5000_" + datetime.datetime.now().strftime('%Y_%m_%d_%Hh%M')+"/";

print "Name of output dir: ",outputFolder
# create a directory on eos
os.system('xrdfs root://cmseos.fnal.gov/ mkdir ' + outputFolder)
# create directory in pwd for log files
os.system('mkdir -p ' + OutputLogPath + "/Logs")


# Function to create a tar file
def make_tarfile(output_filename, source_dir):
    with tarfile.open(output_filename, "w:gz") as tar:
            tar.add(source_dir, arcname=os.path.basename(source_dir))

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

aQGCpars = {	'fs0':[4.0, 4.2, 4.4, 4.6, 4.8, 5.0, 5.4, 5.8, 6.0, 6.5, 7.0], 
		'fs1':[5.0, 5.5, 6.0, 6.5, 7.0, 7.5, 8.0, 8.5, 9.0, 9.5, 10.0], 
		'ft0':[0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0, 1.1, 1.2], 
		'ft1':[2.0, 2.2, 2.4, 2.6, 2.8, 3.0, 3.5, 4.0, 4.5, 5.0, 5.5], 
		'ft2':[1.0, 1.5, 2.0, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0, 5.5, 6.0],
		'fm0':[1.1, 1.4, 1.8, 2.2, 2.7, 3.2, 3.7, 4.2, 4.7, 5.2, 6.0], 
		'fm1':[3.0, 3.5, 4.0, 4.5, 5.0, 5.5, 6.0, 6.5, 7.0, 7.5, 8.0], 
		'fm6':[2.0, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0, 5.5, 6.0, 6.5, 7.0], 
		'fm7':[5.0, 5.5, 6.0, 6.5, 7.0, 7.5, 8.0, 8.5, 9.0, 9.5, 10.0]
		}

dataPath = "$CMSSW_BASE/src/CombinedEWKAnalysis/CommonTools/data/anomalousCoupling/"
configFile = "config_TF1_wv_plain_my"

LimitFile = "Limits_mass"

os.system("rm Limits.log")

for mass in ['', '_M1000', '_1500', '_2000', '_2500', '_3000', '_3500', '_4000', '_4500', '_5000']:
	for pars, value in aQGCpars.iteritems():
	  for val in value:
	    outJDL.write("Output = "+OutputLogPath+"/"+   str(pars)+"_"+str(val)+"_"+str(val)+"_"+mass+".stdout\n");
	    outJDL.write("Error  = "+OutputLogPath+"/"+   str(pars)+"_"+str(val)+"_"+str(val)+"_"+mass+".stdout\n");
	    outJDL.write("Log  = "+OutputLogPath+"/Logs/"+str(pars)+"_"+str(val)+"_"+str(val)+"_"+mass+".log\n");
	    if mass == '':
	    	outJDL.write('Arguments =  -r -'+str(val)+' '+ str(val) + '  -l ' + LimitFile+mass+'_'+str(pars)+'_'+str(val)+"_"+str(val)+'.log' + ' -a ' + pars + '  -p ' + dataPath + '  -c ' + configFile + '  \n')
	    else:
	    	outJDL.write('Arguments =  -r -'+str(val)+' '+ str(val) + '  -l ' + LimitFile+mass+'_'+str(pars)+'_'+str(val)+"_"+str(val)+'.log' + ' -a ' + pars + '  -p ' + dataPath + '  -c ' + configFile + '  -m '+ mass + ' \n')
	    outJDL.write("Queue\n");

outJDL.close();
print "===> Set Proxy Using:";
print "\tvoms-proxy-init --voms cms --valid 168:00";
print "\"condor_submit runstep2condor.jdl\" to submit";


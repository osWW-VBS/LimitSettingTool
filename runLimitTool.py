import os

#aQGCpars = {'fs0':[-4,4], 'fs1':[-5,5], 'ft0':[-0.3,0.3], 'ft1':[-0.3,0.3], 'ft2':[-0.5,0.5], 'fm0':[-1.5,1.5], 'fm1':[-4,4], 'fm6':[-3,3], 'fm7':[-5.5,5.5]}
#M1000
#aQGCpars = {'fs0':[-8,8], 'fs1':[-8,8], 'ft0':[-1.3,1.3], 'ft1':[-1.3,1.3], 'ft2':[-1.5,1.5], 'fm0':[-3.5,3.5], 'fm1':[-9,9], 'fm6':[-9,9], 'fm7':[-9.5,9.5]}
#M5000
#aQGCpars = {'fs0':[-5.5,5.5], 'fs1':[-5.5,5.5], 'ft0':[-0.8,0.8], 'ft1':[-2.3,2.3], 'ft2':[-1.0,1.0], 'fm0':[-5.5,5.5], 'fm1':[-15,15], 'fm6':[-5,5], 'fm7':[-6.0,6.0]}
#aQGCpars = {'fs0':[-6.0,6.0], 'fs1':[-6.0,6.0], 'ft0':[-0.5,0.5], 'ft1':[-4.3,4.3], 'fm0':[-8.5,8.5], 'fm1':[-20,20]}
#aQGCpars = {'ft1':[-6.3,6.3], 'ft0':[-0.4,0.4], 'fm1':[-18,18], 'fm0':[-10.5,10.5], 'fs1':[-7.0,7.0]}
#aQGCpars = {'fm0':[-12.5,12.5], 'ft1':[-8.3,8.3], 'fm1':[-19,19]}
#aQGCpars = {'ft1':[-7.3,7.3], 'fm0':[-11.5,11.5], 'fm1':[-21,21]}
#aQGCpars = {'ft1':[-9.0,9.0], 'fm0':[-12.0,12.0], 'fm1':[-25,25]}
#aQGCpars = {'fm0':[-1.1,1.1]}
aQGCpars = {'fs1':[-5.50,5.50]}
mass = ""
#aQGCpars = {'fs0':[-4.0,3.9]}
#aQGCpars = {'fs0':[-4.5,4.5], 'ft0':[-0.2,0.2], 'ft1':[-0.3,0.3], 'ft2':[-0.5,0.5], 'fm0':[-1.5,1.5], 'fm1':[-4,4], 'fm6':[-3,3], 'fm7':[-5.5,5.5]}
#for mT
#aQGCpars = {'fs0':[-5,5], 'ft0':[-0.2,0.2], 'ft1':[-0.3,0.3], 'ft2':[-0.5,0.5], 'fm0':[-1.5,1.5], 'fm1':[-4,4], 'fm6':[-3,3], 'fm7':[-5.5,5.5]}
#aQGCpars = {'fs0':[-5,5], 'ft0':[-3.7,3.7], 'ft1':[-3.7,3.7], 'ft2':[-3.7,3.7], 'fm0':[-3.5,3.5], 'fm1':[-4,4], 'fm6':[-3,3], 'fm7':[-3.5,3.5]}

dataPath = "$CMSSW_BASE/src/CombinedEWKAnalysis/CommonTools/data/anomalousCoupling/"
#configFile = "config_TF1_wv_plain_my"
configFile = ["config_TF1_wv_plain_my","config_TF1_wv_plain_my_ZV"]
os.system("date")

LimitFile = "Limits_mass_5000.log"

os.system("rm Limits.log")

for pars, value in aQGCpars.iteritems():
	print "\n\n","="*20,"\n\n"
	#print('python submit_condor.py -r '+str(value[0])+' '+ str(value[1]) + '  -l ' + LimitFile + ' -a ' + pars + '  -p ' + dataPath + '  -c ' + configFile)
	if mass == "":
		os.system('python submit_condor.py -r '+str(value[0])+' '+ str(value[1]) + '  -l ' + LimitFile + ' -a ' + pars + '  -p ' + dataPath + '  -c ' + configFile[0] + ' ' + configFile[1])
	else:
		os.system('python submit_condor.py -r '+str(value[0])+' '+ str(value[1]) + '  -l ' + LimitFile + ' -a ' + pars + '  -p ' + dataPath + '  -c ' + configFile[0] + ' ' + configFile[1] + '  -m ' + mass)
os.system("date")

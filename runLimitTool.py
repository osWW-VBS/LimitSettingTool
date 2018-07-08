import os

#aQGCpars = {'fs0':[-5,5], 'fs1':[-6,6], 'ft0':[-0.3,0.3], 'ft1':[-0.3,0.3], 'ft2':[-0.5,0.5], 'fm0':[-1.5,1.5], 'fm1':[-4,4], 'fm6':[-3,3], 'fm7':[-5.5,5.5]}
aQGCpars = {'fs0':[-4.0,3.9]}
#aQGCpars = {'fs0':[-4.5,4.5], 'ft0':[-0.2,0.2], 'ft1':[-0.3,0.3], 'ft2':[-0.5,0.5], 'fm0':[-1.5,1.5], 'fm1':[-4,4], 'fm6':[-3,3], 'fm7':[-5.5,5.5]}
#for mT
#aQGCpars = {'fs0':[-5,5], 'ft0':[-0.2,0.2], 'ft1':[-0.3,0.3], 'ft2':[-0.5,0.5], 'fm0':[-1.5,1.5], 'fm1':[-4,4], 'fm6':[-3,3], 'fm7':[-5.5,5.5]}
#aQGCpars = {'fs0':[-5,5], 'ft0':[-3.7,3.7], 'ft1':[-3.7,3.7], 'ft2':[-3.7,3.7], 'fm0':[-3.5,3.5], 'fm1':[-4,4], 'fm6':[-3,3], 'fm7':[-3.5,3.5]}

dataPath = "$CMSSW_BASE/src/CombinedEWKAnalysis/CommonTools/data/anomalousCoupling/"
configFile = "config_TF1_wv_plain_my"
os.system("date")

LimitFile = "Limits_mass.log"

os.system("rm Limits.log")

for pars, value in aQGCpars.iteritems():
   print "\n\n","="*20,"\n\n"
   print pars,"\t",value[0],"\t",value[1]
   os.system('echo "" >> '+LimitFile)
   os.system('echo "=====	'+pars+'      =====" >> '+LimitFile)
   os.system('echo "" >> '+LimitFile)


   # copy root file
   print "="*20,"\n\n\t COMMAND : 1 : COPY ROOT FILE \n\n","="*20
   print('cp '+dataPath+'signal_proc_ch1_splitted_TF1_h'+pars+'.root '+dataPath+'signal_proc_ch1_splitted_TF1.root ')
   print ""
   os.system('cp '+dataPath+'signal_proc_ch1_splitted_TF1_h'+pars+'.root '+dataPath+'signal_proc_ch1_splitted_TF1.root')


   print "="*20,"\n\n\t COMMAND : 2 : COPY ROOT FILE \n\n","="*20
   os.system("python buildWorkspace_AC.py --config="+configFile+"  | tee Limit_"+pars+"_mass.log")
   print ""

   print "="*20,"\n\n\t COMMAND : 3 : COPY ROOT FILE \n\n","="*20
   os.system("text2workspace.py -m 126 aC_ch1_splitted_TF1.txt -o Example_test.root -P CombinedEWKAnalysis.CommonTools.ACModel:par1_TF1_Model --PO channels=ch1_splitted_TF1 --PO poi=hfs0 --PO range_hfs0="+str(value[0])+","+str(value[1]))
   print ""

   print "="*20,"\n\n\t COMMAND : 4 : COPY ROOT FILE \n\n","="*20
   os.system("combine Example_test.root -M MultiDimFit -P hfs0 --floatOtherPOIs=0 --algo=grid --points=10000 --minimizerStrategy=2 -t -1 --expectSignal=1")
   print ""

   print "="*20,"\n\n\t COMMAND : 5 : Get Limits ",pars," \n\n","="*20
   os.system("date")
   print ""
   print("python build1DInterval.py "+ str(value[0]) + "  " + str(value[1])  +" higgsCombineTest.MultiDimFit.mH120.root hfs0  >> "+LimitFile)
   os.system("python build1DInterval.py "+ str(value[0]) + "  " + str(value[1])  +" higgsCombineTest.MultiDimFit.mH120.root hfs0  >> "+LimitFile)
   print ""
   os.system("date")

   os.system("cp aC_ch1_splitted_TF1.txt aC_ch1_splitted_TF1_"+pars+"_mass.txt")
os.system("date")

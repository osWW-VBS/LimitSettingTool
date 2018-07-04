aQGCpars = {'fs0':[-5,5], 'fs1':[-5,5], 'ft0':[-5,5], 'ft1':[-5,5], 'ft2':[-5,5], 'fm0':[-5,5], 'fm1':[-5,5], 'fm6':[-5,5], 'fm7':[-5,5]}


for pars, value in aQGCpars.iteritems():
   print "\n\n","="*20,"\n\n"
   print key,"\t",value[0],"\t",value[1]

   command = 'cp ch1_splitted_TF1.root ch1_splitted_TF1_'+pars+'.root'
   os.sys(command)
   command = 'cp config_TF1_wv_plain config_TF1_wv_plain_'+pars
   os.sys(command)
   command = "sed 's/ft0/"+pars+"/g config_TF1_wv_plain_"+pars
   os.sys(command)
   
   os.sys("python buildWorkspace_AC.py --config=config_TF1_wv_plain_"+pars)

   os.sys("text2workspace.py -m 126 aC_ch1_splitted_TF1.txt -o Example_test.root -P CombinedEWKAnalysis.CommonTools.ACModel:par1_TF1_Model --PO channels=ch1_splitted_TF1 --PO poi=h"+pars+" --PO range_h"+pars+"=-5,5")

   os.sys("combine Example_test.root -M MultiDimFit -P "+ pars +" --floatOtherPOIs=0 --algo=grid --points=10000 --minimizerStrategy=2 -t -1 --expectSignal=1")

   os.sys("python build1DInterval.py -5.0 5.0 higgsCombineTest.MultiDimFit.mH120.root h"+pars+"  > Log_"+pars+".log")

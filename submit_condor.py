import os
import argparse

parser = argparse.ArgumentParser(description='Process limit combine tool commands...')
parser.add_argument('-r', '--range', type=float, nargs=2, help='Range of aQGC parameter to scan', default=[-5.0, 5.0])
parser.add_argument('-l', '--log', type=str,   help='name of log file', default='test')
parser.add_argument('-a', '--pars', type=str,  help='name of aQGC parameter', default='fs0')
parser.add_argument('-p', '--path', type=str,  help='Path of input root files', default='/eos/uscms/')
parser.add_argument('-c', '--config', type=str,help='Name of config file', default='my_config_file')
parser.add_argument('-m', '--mass', type=str, help='Mww cut for cut-off scan', default='')
parser.add_argument('-ch', '--channel', type=str, help='channel WV or ZV', default='ZV')
args = parser.parse_args()

print args.range
print args.log
print args.pars
print args.path
print args.config

#print "\n\n","="*20,"\n\n"
print args.pars,"\t",args.range[0],"\t",args.range[1]
os.system('echo "" >> '+args.log)
os.system('echo "=====	'+args.pars+'      =====" >> '+args.log)
os.system('echo "" >> '+args.log)


# copy root file
print "="*20,"\n\n\t COMMAND : 1 : COPY ROOT FILE \n\n","="*20
print('cp '+args.path+'signal_proc_ch1_splitted_TF1_'+args.channel+'_h'+args.pars+args.mass+'.root '+args.path+'signal_proc_ch1_splitted_TF1_'+args.channel+'.root ')
print ""
os.system('cp '+args.path+'signal_proc_ch1_splitted_TF1_'+args.channel+'_h'+args.pars+args.mass+'.root '+args.path+'signal_proc_ch1_splitted_TF1_'+args.channel+'.root')


print "="*20,"\n\n\t COMMAND : 2 : COPY ROOT FILE \n\n","="*20
print("python buildWorkspace_AC.py --config="+args.config)
os.system("python buildWorkspace_AC.py --config="+args.config)
print ""

print "="*20,"\n\n\t COMMAND : 3 : COPY ROOT FILE \n\n","="*20
print("text2workspace.py -m 126 aC_ch1_splitted_TF1_"+args.channel+".txt -o Example_test.root -P CombinedEWKAnalysis.CommonTools.ACModel:par1_TF1_Model --PO channels=ch1_splitted_TF1_"+args.channel+" --PO poi=hfs0 --PO range_hfs0="+str(args.range[0])+","+str(args.range[1]))
#os.system("text2workspace.py -m 126 aC_ch1_splitted_TF1_"+args.channel+".txt -o Example_test.root -P CombinedEWKAnalysis.CommonTools.ACModel:par1_TF1_Model --PO channels=ch1_splitted_TF1_"+args.channel+" --PO poi=hfs0 --PO range_hfs0="+str(args.range[0])+","+str(args.range[1])+" ")
os.system("text2workspace.py -m 126 aC_ch1_splitted_TF1_"+args.channel+".txt -o Example_test.root -P CombinedEWKAnalysis.CommonTools.ACModel:par1_TF1_Model --PO channels=ch1_splitted_TF1_"+args.channel+" --PO poi=hfs0 --PO range_hfs0="+str(args.range[0])+","+str(args.range[1])+" >& temp.txt")
print ""

print "="*20,"\n\n\t COMMAND : 4 : COPY ROOT FILE \n\n","="*20
print("combine Example_test.root -M MultiDimFit -P hfs0 --floatOtherPOIs=0 --algo=grid --points=10000 --minimizerStrategy=2 -t -1 --expectSignal=1")
#os.system("combine Example_test.root -M MultiDimFit -P hfs0 --floatOtherPOIs=0 --algo=grid --points=10000 --minimizerStrategy=2 -t -1 --expectSignal=1 ")
os.system("combine Example_test.root -M MultiDimFit -P hfs0 --floatOtherPOIs=0 --algo=grid --points=10000 --minimizerStrategy=2 -t -1 --expectSignal=1 > tmp.txt")
print ""

print "="*20,"\n\n\t COMMAND : 5 : Get Limits ",args.pars," \n\n","="*20
os.system("date")
print ""
print("python build1DInterval.py "+ str(args.range[0]) + "  " + str(args.range[1])  +" higgsCombineTest.MultiDimFit.mH120.root hfs0  >> "+args.log)
os.system("python build1DInterval.py "+ str(args.range[0]) + "  " + str(args.range[1])  +" higgsCombineTest.MultiDimFit.mH120.root hfs0 ")
print ""
os.system("date")

os.system("mv aC_ch1_splitted_TF1_"+args.channel+".txt aC_ch1_splitted_TF1_"+args.channel+"_"+args.pars+"_mass_"+args.mass+".txt")
os.system("mv Example_test.root Example_test_"+args.channel+"_"+args.pars+"_mass_"+args.mass+".root")
os.system("mv higgsCombineTest.MultiDimFit.mH120.root higgsCombineTest.MultiDimFit.mH120_"+args.channel+"_"+args.pars+"_mass_"+args.mass+".root")

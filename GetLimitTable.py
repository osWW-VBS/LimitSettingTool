import os

rrange = 1

os.system('find . | xargs grep -l "Traceback (most recent call last)" *.stdout | awk \'{print "mv "$1" OutOfRange"}\' > remove.sh')
os.system('find . | xargs grep -l "IndexError: list index out of range" *.stdout | awk \'{print "mv "$1"  OutOfRange"}\' >> remove.sh')
os.system('mkdir OutOfRange')
os.system("sed -i '/GetLimitTable.py/d' remove.sh")
os.system('bash remove.sh')
os.system("sed -i '/rasharma/d' *.stdout")
os.system("sed -i '/inversion of matrix fails/d' *.stdout")
os.system("sed -i '/Minimization did NOT converge/d' *.stdout")
os.system("sed -E -i '/rasharma|inversion of matrix fails|Minimization did NOT converge/d' *.stdout")
os.system('mkdir union')
os.system('grep "95% CL Limit" *.stdout | grep "U" | awk -F ":" \'{print "mv "$1" union/"}\' > MoveFileToUniDir.sh')
os.system('bash MoveFileToUniDir.sh')

for mass in ['_', 'M1000', '1500', '2000', '2500', '3000', '3500', '4000', '4500', '5000']:
   #print('grep "95% CL Limit:" *'+mass+'.stdout > tmp.dat') 
   os.system('grep "95% CL Limit:" *'+mass+'.stdout > tmp.dat') 

   #print "===="
   #os.system('cat tmp.dat')
   #print "===="
   print "\n\n","-"*30,"\n"
   if mass == '_': print "\t Cut-off = [600, inf]"
   else: print "\t Cut-off = [600,",mass,"]"
   print ""
   oldPar = "Test"
   inFile = open("tmp.dat",'read')

   for lines in inFile:
      splitTxt = lines.split()
      par = splitTxt[0][0:3]
      if par == oldPar: continue;
      if rrange: print par,splitTxt[0][4:8],splitTxt[-1]
      else: print par,splitTxt[-1]
      oldPar= par

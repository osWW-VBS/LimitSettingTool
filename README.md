# SMP-VV Limit Setting Tool Setup

Reference: [https://twiki.cern.ch/twiki/bin/viewauth/CMS/ATGCRooStats](https://twiki.cern.ch/twiki/bin/viewauth/CMS/ATGCRooStats)

# Setup-1

```sh
setenv SCRAM_ARCH slc6_amd64_gcc481
cmsrel CMSSW_7_1_5
cd CMSSW_7_1_5/src
cmsenv
git clone --branch v5.0.2 git@github.com:cms-analysis/HiggsAnalysis-CombinedLimit.git HiggsAnalysis/CombinedLimit
scramv1 b clean
# always first clean then compile
scramv1 b -j 8 
mkdir CombinedEWKAnalysis
git clone git@github.com:senka/CombinedEWKAnalysis_1D2D3D.git CombinedEWKAnalysis
source CombinedEWKAnalysis/CommonTools/setup/patchToSource.sh
scramv1 b -j 8
git clone git@github.com:osWW-VBS/LimitSettingTool.git
```

Now go the path `CombinedEWKAnalysis/CommonTools/data/anomalousCoupling` and remove all root files.

```sh
cd $CMSSW_BASE/src/CombinedEWKAnalysis/CommonTools/data/anomalousCoupling
rm *.root
cd $CMSSW_BASE/src
```

Next, move the fit.C, config file and resubmit file to respective places... to the above path 

```sh
bash LimitSettingTool/SetupFile.sh
```

# Setup-2

- Before run put the input root files to path `$CMSSW_BASE/src/CombinedEWKAnalysis/CommonTools/data/anomalousCoupling/`.  

- The lastest version of root file can be grabbed from `/afs/cern.ch/user/r/rasharma/work/public/aQGC_Ntuples/PLB_1st_comment/limit_rootfiles`.

- Copy  the root file from the path given above into path `$CMSSW_BASE/src/CombinedEWKAnalysis/CommonTools/data/anomalousCoupling/`

- Then to fit the signal root file run

   ```sh
   cd $CMSSW_BASE/src/CombinedEWKAnalysis/CommonTools/data/anomalousCoupling/
   root -l -b -q fit.C
   ```

To run the `fit.C` check if the input root file name is appropriate. We are fitting signal here because fitting is dependent on the CMSSW version. And our signal extraction part is in CMSSW_8X while this limit tool we are running on CMSSW_7_1_5.

# Run the Limit

## Manual

- After fit in the previous steps the root file that we have now looks like:

   ```
   ch1_splitted_TF1_WV.root
   ch1_splitted_TF1_WV_NoBinbyBin.root
   ch1_splitted_TF1_hfm0.root
   ch1_splitted_TF1_hfm1.root
   ch1_splitted_TF1_hfm6.root
   ch1_splitted_TF1_hfm7.root
   ch1_splitted_TF1_hfs0.root
   ch1_splitted_TF1_hfs1.root
   ch1_splitted_TF1_hft0.root
   ch1_splitted_TF1_hft1.root
   ch1_splitted_TF1_hft2.root
   signal_proc_ch1_splitted_TF1_hfm0.root
   signal_proc_ch1_splitted_TF1_hfm1.root
   signal_proc_ch1_splitted_TF1_hfm6.root
   signal_proc_ch1_splitted_TF1_hfm7.root
   signal_proc_ch1_splitted_TF1_hft0.root
   signal_proc_ch1_splitted_TF1_hft1.root
   signal_proc_ch1_splitted_TF1_hft2.root
   signal_proc_ch1_splitted_TF1_hfs0.root
   signal_proc_ch1_splitted_TF1_hfs1.root
   ```
- The next steps need two files. They are `ch1_splitted_TF1.root` and `signal_proc_ch1_splitted_TF1.root`.
- There are total of nine parameters. They are fm0, fm1, fm6, fm7, ft0, ft1, ft2, fs0 and fs1. We need to run next steps nine times for each parameters.
- If we are calculating limits for `fs0` then we need to do:

   ```sh
   cp ch1_splitted_TF1_hfs0.root ch1_splitted_TF1.root
   cp signal_proc_ch1_splitted_TF1_hfs0.root signal_proc_ch1_splitted_TF1.root
   ```

- We need to do the same for all others.

   ```sh
   cd $CMSSW_BASE/src/CombinedEWKAnalysis/CommonTools/test
   # prepare config file config_TF1_wv_plain
   python buildWorkspace_AC.py --config=config_TF1_wv_plain
   text2workspace.py -m 126 aC_ch1_splitted_TF1.txt -o Example_test.root -P CombinedEWKAnalysis.CommonTools.ACModel:par1_TF1_Model --PO channels=ch1_splitted_TF1 --PO poi=hfs0 --PO range_hfs0=-5,5
   combine Example_test.root -M MultiDimFit -P hfs0 --floatOtherPOIs=0 --algo=grid --points=10000 --minimizerStrategy=2 -t -1 --expectSignal=1
   python build1DInterval.py -5.0 5.0 higgsCombineTest.MultiDimFit.mH120.root hfs0
   ```

## Script for above commands

```sh
bash resubmit.sh
```

## Run for all limits at once

```sh
python runLimitTool.py
```

# Some useful command to filter out condor log files

	```sh
	find . | xargs grep -l "Traceback (most recent call last)" | awk '{print "rm "$1}' > remove.sh
	
	sed -i '/rasharma/d' *.stdout
	
	sed -i '/inversion of matrix fails/d' *.stdout

	sed -i '/Minimization did NOT converge/d' *.stdout
	```
or,
	```sh
	sed -E -i '/rasharma|inversion of matrix fails|Minimization did NOT converge/d' *.stdout

	grep "95% CL Limit" *.stdout | grep "U" | awk -F ":" '{print "mv "$1" union/"}' > MoveFileToUniDir.sh
	```

# List of important points

1. There are two input root files.
	1. First one corresponds to the aQGC parameter.
	2. Second one corresponds to the all the shape systematics for all backgrounds
2. There is a naming convention for the two input root file:
	1. File name convention for aQGC signal: `signal_proc_*channel_name*.root`
	2. For another file naming convention should be just `channel_name.root`.
3. Note the **channel_name** from naming convention of the root file. It should be same in the two input root files.
4. Selected range for the parameters under calculation should not be too large.

# List of important commands

```bash
find . | xargs grep -l "Traceback (most recent call last)" | awk '{print "rm "$1}' > remove.sh

sed -i '/rasharma/d' *.stdout

sed -i '/ list index out of range/d' *.stdout

sed -i '/inversion of matrix fails/d' *.stdout
```


# print number from 4.80 to 12.0 in steps of 0.025

```bash
awk 'BEGIN { for (i=4.80; i<12.0; i+=0.025) print i}' | xargs | sed -e 's/ /, /g'
```

# SMP-VV Limit Setting Tool Setup

Reference: [https://twiki.cern.ch/twiki/bin/viewauth/CMS/ATGCRooStats](https://twiki.cern.ch/twiki/bin/viewauth/CMS/ATGCRooStats)

```sh
setenv SCRAM_ARCH slc6_amd64_gcc481
cmsrel CMSSW_7_1_5
cd CMSSW_7_1_5/src
cmsenv
git clone --branch v5.0.2 git@github.com:cms-analysis/HiggsAnalysis-CombinedLimit.git HiggsAnalysis/CombinedLimit
mkdir CombinedEWKAnalysis
git clone git@github.com:senka/CombinedEWKAnalysis_1D2D3D.git CombinedEWKAnalysis
source CombinedEWKAnalysis/CommonTools/setup/patchToSource.sh
scramv1 b
git clone git@github.com:osWW-VBS/LimitSettingTool.git
```

Now go the path `CombinedEWKAnalysis/CommonTools/data/anomalousCoupling` and remove all root files.

```sh
cd $CMSSW_BASE/CombinedEWKAnalysis/CommonTools/data/anomalousCoupling
rm *.root
```

Next, move the fit.C to the above path 
```sh
mv LimitSettingTool/fit.C $CMSSW_BASE/CombinedEWKAnalysis/CommonTools/data/anomalousCoupling/
mv LimitSettingTool/config_TF1_wv_plain $CMSSW_BASE/CombinedEWKAnalysis/CommonTools/data/anomalousCoupling/
mv LimitSettingTool/resubmit.sh	$CMSSW_BASE/CombinedEWKAnalysis/CommonTools/data/anomalousCoupling/

# Here put the signal and backgound root files having up/dn shapes

root -l -b -q fit.C
```

To run the `fit.C` check if the input root file name is appropriate. We are fitting signal here because fitting is dependent on the CMSSW version. And our signal extraction part is in CMSSW_8X while this limit tool we are running on CMSSW_7_1_5.


```sh
cd $CMSSW_BASE/src/CombinedEWKAnalysis/CommonTools/test
# prepare config file config_TF1_wv_plain
python buildWorkspace_AC.py --config=config_TF1_wv_plain
text2workspace.py -m 126 aC_ch1_splitted_TF1.txt -o Example_test.root -P CombinedEWKAnalysis.CommonTools.ACModel:par1_TF1_Model --PO channels=ch1_splitted_TF1 --PO poi=hfs0 --PO range_hfs0=-5,5
combine Example_test.root -M MultiDimFit -P hfs0 --floatOtherPOIs=0 --algo=grid --points=10000 --minimizerStrategy=2 -t -1 --expectSignal=1
python build1DInterval.py -5.0 5.0 higgsCombineTest.MultiDimFit.mH120.root hfs0
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

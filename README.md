# LimitSettingTool
Scripts for calculating Limits

# Setting tool

	cmsrel CMSSW_7_4_7
	cd CMSSW_7_4_7/src 
	cmsenv
	git clone https://github.com/cms-analysis/HiggsAnalysis-CombinedLimit.git HiggsAnalysis/CombinedLimit
	cd HiggsAnalysis/CombinedLimit
	git fetch origin;
	git checkout v6.3.0;
	scramv1 b clean; scramv1 b 
	cd ../../
	git clone git@github.com:osWW-VBS/LimitSettingTool.git
	cd LimitSettingTool

To get the significance run the command:

	combine -d limits_vvjj_wv_13TeV2016 -M ProfileLikelihood --significance -t -1 --expectSignal=1

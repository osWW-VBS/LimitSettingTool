range=0.8
par="hft0"
python buildWorkspace_AC.py --config=config_TF1_wv_plain
echo ""
echo ""
echo "========================================================= 1"
echo ""
echo ""
text2workspace.py -m 126 aC_ch1_splitted_TF1.txt -o Example_test.root -P CombinedEWKAnalysis.CommonTools.ACModel:par1_TF1_Model --PO channels=ch1_splitted_TF1 --PO poi=${par} --PO range_${par}=-${range},${range}
echo ""
echo ""
echo "========================================================= 2"
echo ""
echo ""
combine Example_test.root -M MultiDimFit -P ${par} --floatOtherPOIs=0 --algo=grid --points=10000 --minimizerStrategy=2 -t -1 --expectSignal=1
echo ""
echo ""
echo "========================================================= 3"
echo ""
echo ""
python build1DInterval.py -${range} ${range} higgsCombineTest.MultiDimFit.mH120.root ${par}

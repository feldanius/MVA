# New_FCC
**_The first step to use the FCC Framework is run the following instruction:_**
 ´source /cvmfs/sw.hsf.org/key4hep/setup.sh -r 2024-03-10´
 ´source ./setup.sh´
´fccanalysis build -j 8´

 (/afs/cern.ch/user/f/fdmartin/FCCAnalyses/examples/FCCee/higgs/mva)
 ___
_In order to run the preselection.py I have to run the following lines:_
`fccanalysis run preselection1.py`
___
_In order to run the plots I have to run the following lines:_
`fccanalysis plots plots.py`


scp /eos/user/f/fdmartin/FCC365_jets_b_tagging_cut_missing_p-15 fdmartin@lxplus.cern.ch:/afs/cern.ch/user/f/fdmartin/FCCAnalyses/signal_strenght


scp fdmartin@lxplus.cern.ch:/afs/cern.ch/user/f/fdmartin/FCCAnalyses/examples/FCCee/higgs/mva/outputs/FCCee/higgs/mva/bdt_model_example.root /eos/user/f/fdmartin/FCC365_MVA_BDT_preselection/

python evaluate_bdt.py -i outputs/FCCee/higgs/mva/bdt_model_example.pkl -o outputs/FCCee/higgs/mva/plots_training


# BDT PROCESS

## STEP 1
preselection2.py

## STEP 2
train_bdt_2.py

## STEP 3
evaluate_bdt.py

## STEP 4
preselection_mva.py

## STEP 5
final_selection_2.py

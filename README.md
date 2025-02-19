
# FCC_MVA



## Running Tests

The first step to use the FCC Framework is run the following instruction:

```bash
  source /cvmfs/sw.hsf.org/key4hep/setup.sh -r 2024-03-10
```
Second step

```bash
  source ./setup.sh
```
And third
```bash
 fccanalysis build -j 8
```

## Notes for me

```bash
cd examples/FCCee/higgs/mva
```
```bash
cd outputs/FCCee/higgs/mva
```

In order to run the preselection.py I have to run the following lines:
```bash
fccanalysis run preselection2.py
```
In order to run the plots I have to run the following lines:
```bash
fccanalysis plots plots.py
``` 
In order to run the evaluate_bdt.py I have to run the following lines:
```bash
python evaluate_bdt.py -i outputs/FCCee/higgs/mva/bdt_model_example.pkl -o outputs/FCCee/higgs/mva/plots_training
``` 

## SCP

Example SCP CERNBOX ---> LXPLUS
```bash
scp /eos/user/f/fdmartin/FCC365_jets_b_tagging_cut_missing_p-15 fdmartin@lxplus.cern.ch:/afs/cern.ch/user/f/fdmartin/FCCAnalyses/signal_strenght
``` 

Example SCP  LXPLUS ---> CERNBOX 
```bash
scp fdmartin@lxplus.cern.ch:/afs/cern.ch/user/f/fdmartin/FCCAnalyses/examples/FCCee/higgs/mva/outputs/FCCee/higgs/mva/bdt_model_example.root /eos/user/f/fdmartin/FCC365_MVA_BDT_preselection/
``` 



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

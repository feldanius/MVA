import uproot
import pandas as pd
import xgboost as xgb
import numpy as np
from sklearn.model_selection import train_test_split
import ROOT
import pickle
import os

ROOT.gROOT.SetBatch(True)

# Función para cargar los datos
def load_process(fIn, variables, target=0, weight_sf=1.0):
    f = uproot.open(fIn)
    tree = f["events"]
    weight = 1.0 / tree.num_entries * weight_sf  # Ajuste de peso
    print("Load {} with {} events and weight {}".format(fIn.replace(".root", ""), tree.num_entries, weight))
    
    df = tree.arrays(variables, library="pd")  # Convertir a DataFrame de pandas
    df['target'] = target  # Etiqueta de señal (1) y fondo (0)
    df['weight'] = weight
    return df

# Cargar múltiples procesos
def load_multiple_processes(files, variables, weight_sf=1.0, target=0):
    df_list = [load_process(fIn, variables, target=target, weight_sf=weight_sf) for fIn in files]
    return pd.concat(df_list, ignore_index=True)

# Configuración de variables
variables = ["jj_m", "cosTheta_miss", "missingEnergy_energy_fixed", "missing_p_fixed", "higgs_recoil_m", "hbb_p", "hbb_m"]
weight_sf = 1e9

# Archivos de señal y fondo
signal_files = [
    "/eos/user/f/fdmartin/FCC365_MVA_train_realsim_recoil/preselection/wzp6_ee_nuenueH_Hbb_ecm365.root",
    "/eos/user/f/fdmartin/FCC365_MVA_train_realsim_recoil/preselection/wzp6_ee_numunumuH_Hbb_ecm365.root"
]

background_files = [
    "/eos/user/f/fdmartin/FCC365_MVA_train_realsim_recoil/preselection/p8_ee_ZZ_ecm365.root",
    "/eos/user/f/fdmartin/FCC365_MVA_train_realsim_recoil/preselection/p8_ee_WW_ecm365.root", 
    "/eos/user/f/fdmartin/FCC365_MVA_train_realsim_recoil/preselection/p8_ee_tt_ecm365.root",
    "/eos/user/f/fdmartin/FCC365_MVA_train_realsim_recoil/preselection/wzp6_ee_numunumuH_Hbb_ecm365.root"
]

print("Parse inputs")
sig_df = load_multiple_processes(signal_files, variables, weight_sf=weight_sf, target=1)
bkg_df = load_multiple_processes(background_files, variables, weight_sf=weight_sf, target=0)

# Concatenar los datos de señal y fondo
data = pd.concat([sig_df, bkg_df], ignore_index=True)

# Dividir los datos en entrenamiento y prueba
train_data, test_data, train_labels, test_labels, train_weights, test_weights = train_test_split(
    data[variables], data['target'], data['weight'], test_size=0.2, random_state=42, stratify=data['target']
)

train_data = train_data.to_numpy()
test_data = test_data.to_numpy()
train_labels = train_labels.to_numpy()
test_labels = test_labels.to_numpy()
train_weights = train_weights.to_numpy()
test_weights = test_weights.to_numpy()

params = {
    'objective': 'binary:logistic',
    'eval_metric': 'auc',
    #'eta': 0.1,
    'max_depth': 5,
    'subsample': 0.7,#before 0.5 giving more information to the trees
    'colsample_bytree': 0.7,#before 0.5 giving more information to the trees
    'seed': 42,
    'n_estimators': 350,
    'early_stopping_rounds': 25,
    'learning_rate': 0.10, #before 0.2 decreasing is better for a finest learning
    'gamma': 3,
    'min_child_weight': 10,
    'max_delta_step': 0,
}

print("Start training")
eval_set = [(train_data, train_labels), (test_data, test_labels)]
bdt = xgb.XGBClassifier(**params)
bdt.fit(train_data, train_labels, verbose=True, eval_set=eval_set, sample_weight=train_weights)

print("Export model")
fOutName = "/eos/user/f/fdmartin/FCC365_MVA_train_realsim_recoil/train/bdt_model_example.root"
ROOT.TMVA.Experimental.SaveXGBoost(bdt, "bdt_model", fOutName, num_inputs=len(variables))

# Guardar las variables
variables_ = ROOT.TList()
for var in variables:
     variables_.Add(ROOT.TObjString(var))
fOut = ROOT.TFile(fOutName, "UPDATE")
fOut.WriteObject(variables_, "variables")

# Guardar MVA Score en un TTree
test_mva_scores = bdt.predict_proba(test_data)[:, 1]  # Probabilidad de la clase señal

# Crear el TTree
tree = ROOT.TTree("mva_tree", "Tree with MVA scores")

# Definir variables para las ramas
test_mva_score = np.zeros(1, dtype=np.float32)
var_branches = {var: np.zeros(1, dtype=np.float32) for var in variables}

# Crear ramas
tree.Branch("mva_score", test_mva_score, "mva_score/F")
for var in variables:
    tree.Branch(var, var_branches[var], f"{var}/F")

# Llenar el TTree
for i in range(len(test_mva_scores)):
    test_mva_score[0] = test_mva_scores[i]
    for var in variables:
        var_branches[var][0] = test_data[i][variables.index(var)]
    tree.Fill()

# Escribir el TTree en el archivo ROOT
tree.Write()
fOut.Close()

print("MVA scores saved successfully in the ROOT file!")

# Guardar el modelo y datos con pickle
save = {
    'model': bdt,
    'train_data': train_data,
    'test_data': test_data,
    'train_labels': train_labels,
    'test_labels': test_labels,
    'variables': variables
}

pickle.dump(save, open("/eos/user/f/fdmartin/FCC365_MVA_train_realsim_recoil/train/bdt_model_example.pkl", "wb"))
print("Model saved as pickle file.")

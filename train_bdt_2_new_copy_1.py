import uproot
import pandas as pd
import xgboost as xgb
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, roc_auc_score
import ROOT
import pickle

ROOT.gROOT.SetBatch(True)

# Función para cargar los datos
def load_process(fIn, variables, target=0, weight_sf=1.):
    f = uproot.open(fIn)
    tree = f["events"]
    weight = 1.0 / tree.num_entries * weight_sf  # Ajuste de peso
    print("Load {} with {} events and weight {}".format(fIn.replace(".root", ""), tree.num_entries, weight))

    df = tree.arrays(variables, library="pd")  # Convertir a DataFrame de pandas
    df['target'] = target  # Etiqueta de señal (1) y fondo (0)
    df['weight'] = weight
    return df

# Cargar múltiples procesos
def load_multiple_processes(files, variables, weight_sf=1., target=0):
    df_list = []
    for fIn in files:
        df = load_process(fIn, variables, target=target, weight_sf=weight_sf)
        df_list.append(df)
    return pd.concat(df_list, ignore_index=True)

# Configuración de variables
variables = ["jj_m", "cosTheta_miss", "missingEnergy_energy", "missing_p"]
weight_sf = 1e9

# Archivos de señal y fondo
signal_files = [
    "outputs/FCCee/higgs/mva/preselection_new/wzp6_ee_nuenueH_Hbb_ecm240.root",
    "outputs/FCCee/higgs/mva/preselection_new/wzp6_ee_numunumuH_Hbb_ecm240.root"
]

background_files = [
    "outputs/FCCee/higgs/mva/preselection_new/p8_ee_ZZ_ecm240.root",
    "outputs/FCCee/higgs/mva/preselection_new/p8_ee_WW_ecm355.root", 
    "outputs/FCCee/higgs/mva/preselection_new/p8_ee_tt_ecm365.root",
    "outputs/FCCee/higgs/mva/preselection_new/wzp6_ee_numunumuH_Hbb_ecm240.root"
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
    'eval_metric': 'auc',  # Cambiar a 'auc' para early_stopping_rounds
    'eta': 0.1,
    'max_depth': 5,
    'subsample': 0.5,
    'colsample_bytree': 0.5,
    'seed': 42,
    'n_estimators': 350,  # Número de estimadores
    'early_stopping_rounds': 25,
    'learning_rate': 0.20,
    'gamma': 3,
    'min_child_weight': 10,
    'max_delta_step': 0,
}

print("Start training")
eval_set = [(train_data, train_labels), (test_data, test_labels)]
bdt = xgb.XGBClassifier(**params)
bdt.fit(train_data, train_labels, verbose=True, eval_set=eval_set, sample_weight=train_weights)


print("Export model")
fOutName = "outputs/FCCee/higgs/mva/test_3_pkl/bdt_model_example.root"

# Asegurar que el directorio existe (aunque creas que ya existe, es clave para evitar errores)
import os
os.makedirs(os.path.dirname(fOutName), exist_ok=True)  # <--- Esto crea la carpeta test_3_pkl si no existe

# 1. Exportar el modelo XGBoost a ROOT usando el Booster directamente
ROOT.TMVA.Experimental.SaveXGBoost(
    bdt.get_booster(),  # Pasar el modelo XGBoost en memoria, NO la ruta del JSON
    "bdt_model", 
    fOutName, 
    num_inputs=len(variables)
)

# 2. Guardar las variables en el archivo ROOT
fOut = ROOT.TFile(fOutName, "UPDATE")
variables_list = ROOT.TList()
for var in variables:
    variables_list.Add(ROOT.TObjString(var))
fOut.WriteObject(variables_list, "variables")
fOut.Close()

# 3. Guardar el modelo en .pkl
save = {
    'model': bdt,
    'train_data': train_data,
    'test_data': test_data,
    'variables': variables
}
pickle.dump(save, open(os.path.join(os.path.dirname(fOutName), "bdt_model_example.pkl"), "wb"))

print("Modelo exportado exitosamente")

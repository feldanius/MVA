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
variables = ["jj_m", "cosTheta_miss", "missingEnergy.energy", "missing_p"]
weight_sf = 1e9

# Archivos de señal y fondo
signal_files = [
    "outputs/FCCee/higgs/mva/preselection/wzp6_ee_nuenueH_Hbb_ecm240",
    "outputs/FCCee/higgs/mva/preselection/wzp6_ee_numunumuH_Hbb_ecm240_vbf"
]

background_files = [
    "outputs/FCCee/higgs/mva/preselection/p8_ee_ZZ_ecm240",
    "outputs/FCCee/higgs/mva/preselection/p8_ee_WW_ecm355",  # Fondo relevante
    "outputs/FCCee/higgs/mva/preselection/p8_ee_tt_ecm365",
    "outputs/FCCee/higgs/mva/preselection/wzp6_ee_numunumuH_Hbb_ecm240"
]

# Cargar los datos
print("Parse inputs")
sig_df = load_multiple_processes(signal_files, variables, weight_sf=weight_sf, target=1)
bkg_df = load_multiple_processes(background_files, variables, weight_sf=weight_sf, target=0)

# Concatenar los datos de señal y fondo
data = pd.concat([sig_df, bkg_df], ignore_index=True)

# Dividir los datos en entrenamiento y prueba
train_data, test_data, train_labels, test_labels, train_weights, test_weights = train_test_split(
    data[variables], data['target'], data['weight'], test_size=0.2, random_state=42, stratify=data['target']
)

# Convertir a numpy arrays
train_data = train_data.to_numpy()
test_data = test_data.to_numpy()
train_labels = train_labels.to_numpy()
test_labels = test_labels.to_numpy()
train_weights = train_weights.to_numpy()
test_weights = test_weights.to_numpy()

# Parámetros del modelo XGBoost
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

# Entrenar el modelo XGBoost
print("Start training")
eval_set = [(train_data, train_labels), (test_data, test_labels)]
bdt = xgb.XGBClassifier(**params)
bdt.fit(train_data, train_labels, verbose=True, eval_set=eval_set, sample_weight=train_weights)

# Verificación del archivo .root antes de exportar el modelo
fOutName = "outputs/FCCee/higgs/mva/bdt_model_example.root"
root_file = ROOT.TFile.Open(fOutName, "UPDATE")
if not root_file:
    print(f"Error al abrir el archivo ROOT: {fOutName}")
else:
    print(f"Archivo ROOT abierto correctamente: {fOutName}")

# Exportar el modelo a ROOT (con JSON primero)
print("Export model")
bdt.get_booster().save_model("outputs/FCCee/higgs/mva/bdt_model_example.json")  # Guardar como .json

# Luego puedes intentar cargar el modelo desde JSON si fuera necesario
# ROOT.TMVA.Experimental.SaveXGBoost("outputs/FCCee/higgs/mva/bdt_model_example.json", "bdt_model", fOutName, num_inputs=len(variables))

# Guardar las variables en ROOT
variables_ = ROOT.TList()
for var in variables:
    variables_.Add(ROOT.TObjString(var))
fOut = ROOT.TFile(fOutName, "UPDATE")
fOut.WriteObject(variables_, "variables")

# Guardar el modelo con pickle
save = {}
save['model'] = bdt
save['train_data'] = train_data
save['test_data'] = test_data
save['train_labels'] = train_labels
save['test_labels'] = test_labels
save['variables'] = variables
pickle.dump(save, open("outputs/FCCee/higgs/mva/bdt_model_example.pkl", "wb"))

print("Modelo exportado exitosamente")

import ROOT
import pandas as pd
import numpy as np
import pickle

# Cargar el modelo entrenado
res = pickle.load(open("outputs/FCCee/higgs/mva/bdt_model_example.pkl", "rb"))
bdt = res['model']
variables = res['variables']

# Lista de archivos ROOT originales
root_files = [
    "p8_ee_WW_ecm355.root",
    "wzp6_ee_nuenueH_Hbb_ecm240.root",
    "wzp6_ee_numunumuH_Hbb_ecm240.root",
    "p8_ee_ZZ_ecm240.root",
    "p8_ee_tt_ecm365.root",
    "wzp6_ee_numunumuH_Hbb_ecm240_vbf.root"
]

# Procesar cada archivo ROOT
for root_file in root_files:
    input_path = f"outputs/FCCee/higgs/mva/preselection/{root_file}"
    output_path = input_path.replace(".root", "_mva.root")  # Crear copia con "_mva"

    # Abrir archivo ROOT original
    file = ROOT.TFile.Open(input_path, "READ")
    tree = file.Get("events")
    
    # Convertir el TTree en un DataFrame con RDataFrame
    rdf = ROOT.RDataFrame(tree)
    df = pd.DataFrame(rdf.AsNumpy(variables)).astype(np.float32)  # Convertir a float32

    # Aplicar el modelo BDT y agregar la columna mva_score
    df["mva_score"] = bdt.predict_proba(df[variables])[:, 1]

    # Crear un nuevo archivo ROOT con la variable `mva_score`
    new_file = ROOT.TFile(output_path, "RECREATE")
    new_tree = ROOT.TTree("events", "events")

    # Crear ramas para las variables originales y `mva_score`
    branches = {}
    for var in variables:
        branches[var] = np.zeros(1, dtype=np.float32)
        new_tree.Branch(var, branches[var], f"{var}/F")

    mva_score = np.zeros(1, dtype=np.float32)
    new_tree.Branch("mva_score", mva_score, "mva_score/F")

    # Llenar el nuevo TTree con los valores del DataFrame
    for i in range(len(df)):
        for var in variables:
            branches[var][0] = df[var].iloc[i]
        mva_score[0] = df["mva_score"].iloc[i]
        new_tree.Fill()

    # Guardar el nuevo archivo ROOT
    new_file.Write()
    new_file.Close()
    file.Close()

    print(f"Procesado: {output_path}")

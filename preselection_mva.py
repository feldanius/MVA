import ROOT
import pandas as pd
import numpy as np
import pickle

# Cargar el modelo entrenado
res = pickle.load(open("outputs/FCCee/higgs/mva/bdt_model_example.pkl", "rb"))
bdt = res['model']
variables = res['variables']

# Lista de archivos ROOT originales
input_files = [
    "p8_ee_WW_ecm355.root",
    "wzp6_ee_nuenueH_Hbb_ecm240.root",
    "wzp6_ee_numunumuH_Hbb_ecm240.root",
    "p8_ee_ZZ_ecm240.root",
    "p8_ee_tt_ecm365.root",
    "wzp6_ee_numunumuH_Hbb_ecm240_vbf.root"
]

# Directorios de entrada y salida
input_dir = "outputs/FCCee/higgs/mva/preselection/"
output_dir = "outputs/FCCee/higgs/mva/preselection/"

for file_name in input_files:
    input_path = input_dir + file_name
    output_path = output_dir + file_name.replace(".root", "_mva.root")

    # Cargar archivo ROOT
    input_file = ROOT.TFile(input_path, "READ")
    tree = input_file.Get("events")

    # Convertir el árbol ROOT en un DataFrame
    df = pd.DataFrame({var: np.array(tree.AsMatrix([var]))[:, 0] for var in variables})

    # Aplicar el modelo BDT
    df["mva_score"] = bdt.predict_proba(df[variables])[:, 1]

    # Crear un nuevo archivo ROOT
    output_file = ROOT.TFile(output_path, "RECREATE")
    new_tree = tree.CloneTree(0)  # Clonar estructura del árbol original

    # Crear una nueva rama para mva_score
    mva_score = np.zeros(1, dtype=np.float32)
    branch = new_tree.Branch("mva_score", mva_score, "mva_score/F")

    # Llenar el nuevo árbol con datos originales y mva_score
    for i in range(len(df)):
        mva_score[0] = df["mva_score"].iloc[i]
        new_tree.Fill()

    # Guardar el nuevo archivo ROOT
    output_file.cd()
    new_tree.Write()
    output_file.Close()
    input_file.Close()

    print(f"Archivo procesado: {output_path}")

import uproot
import pandas as pd
import numpy as np
import pickle

# Definir variables a extraer
variables = ["missingEnergy.energy", "cosTheta_miss", "missing_p", "event_weight"]

# Definir rutas de los archivos de señal y background
signal_files = ["outputs/FCCee/higgs/mva/preselection/wzp6_ee_nuenueH_Hbb_ecm240.root"]
background_files = ["outputs/FCCee/higgs/mva/preselection/p8_ee_ZZ_ecm240.root"]

# Ruta donde guardaremos los datos procesados
file_path = "outputs/FCCee/higgs/mva/preselection/training_data.pkl"

# Función para cargar datos desde archivos ROOT
def load_root_files(file_list, variables, target):
    dataframes = []
    
    for file in file_list:
        print(f"Cargando archivo: {file}")
        with uproot.open(file) as root_file:
            tree = root_file["events"]  # Asegurar que el TTree se llama 'events'
            df = tree.arrays(variables, library="pd")  # Convertir a DataFrame
            df["target"] = target  # Agregar columna de etiqueta (1 = señal, 0 = fondo)
            dataframes.append(df)

    return pd.concat(dataframes, ignore_index=True)

# Cargar datos de señal y background
print("Cargando datos de señal...")
sig_df = load_root_files(signal_files, variables, target=1)

print("Cargando datos de background...")
bkg_df = load_root_files(background_files, variables, target=0)

# Combinar datos
df = pd.concat([sig_df, bkg_df], ignore_index=True)

# Verificaciones
print("Verificando datos...")

# 1. Revisar valores NaN
if df.isnull().values.any():
    print("⚠️ Advertencia: Hay valores NaN en el DataFrame.")
    print(df.isnull().sum())

# 2. Revisar valores infinitos
if np.isinf(df.values).any():
    print("⚠️ Advertencia: Hay valores infinitos en el DataFrame.")

# 3. Revisar si todas las variables están presentes
missing_cols = [var for var in variables if var not in df.columns]
if missing_cols:
    print(f"⚠️ Advertencia: Faltan las siguientes columnas: {missing_cols}")

# Guardar el DataFrame en un archivo .pkl
print(f"Guardando datos en {file_path}...")
with open(file_path, "wb") as f:
    pickle.dump(df, f)

print("✅ Proceso finalizado con éxito.")

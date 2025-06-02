import ROOT
import os
import shutil # Usaremos esta librería para copiar archivos de forma segura

# --- Variables de Configuración ---

# Directorio donde están los archivos ROOT originales
inputDir = "/eos/user/f/fdmartin/FCC365_MVA_train_realsim_recoil/higgs_combine/final_selection/MVA_0"

# Directorio donde se guardarán los nuevos archivos con el peso aplicado
outputDir = "/eos/user/f/fdmartin/FCC365_MVA_train_realsim_recoil/higgs_combine/final_selection/MVA_0"

# El peso que quieres aplicar. 
SCALE_FACTOR = 3.0 

# Lista de los nombres base de los procesos a escalar
processes_to_scale = [
    "wzp6_ee_numunumuH_Hbb_ecm365"
]

# Identificadores de tus archivos para construir el nombre completo
selection_tag = "sel3"
output_tag = "_ZH" # Etiqueta para añadir al nombre del archivo de salida
hist_name = "higgs_recoil_m_final"


# --- Lógica del Programa ---

# 1. Asegurarse de que el directorio de salida exista
if not os.path.exists(outputDir):
    os.makedirs(outputDir)
    print(f"Directorio de salida creado: {outputDir}")

for process in processes_to_scale:
    # 2. Construir los nombres de archivo de entrada y salida
    input_filename = f"{process}_{selection_tag}_histo.root"
    output_filename = f"{process}{output_tag}_{selection_tag}_histo.root"
    
    input_path = os.path.join(inputDir, input_filename)
    output_path = os.path.join(outputDir, output_filename)
    
    print(f"--- Procesando: {process} ---")
    
    # Verificar si el archivo de entrada existe
    if not os.path.exists(input_path):
        print(f"  ERROR: El archivo de entrada no se encontró en {input_path}")
        continue
        
    # 3. Copiar el archivo original al directorio de salida.
    #    Esto asegura que todos los demás objetos y metadatos en el archivo se preserven.
    try:
        shutil.copy2(input_path, output_path)
        print(f"  Archivo copiado a: {output_path}")
    except Exception as e:
        print(f"  ERROR: No se pudo copiar el archivo. {e}")
        continue

    # 4. Abrir la COPIA del archivo en modo "UPDATE" para modificarlo
    f = ROOT.TFile(output_path, "UPDATE")
    if not f or f.IsZombie():
        print(f"  ERROR: No se pudo abrir la copia del archivo en {output_path}")
        continue

    h = f.Get(hist_name)
    if not h:
        print(f"  ERROR: Histograma '{hist_name}' no encontrado en el archivo.")
        f.Close()
        continue
    
    # 5. Aplicar el escalado y guardar el cambio
    print(f"  Integral original: {h.Integral()}")
    h.Scale(SCALE_FACTOR)
    print(f"  Nueva integral tras escalar por {SCALE_FACTOR:.3f}: {h.Integral()}")

    h.Write("", ROOT.TObject.kOverwrite) # Sobrescribe el histograma en el archivo
    f.Close()

print("\nProceso completado.")

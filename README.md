
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
```bash
python evaluate_bdt_mva_real_sim_0_5_recoil_w3.py -i /eos/user/f/fdmartin/FCC365_MVA_train_realsim_recoil/train_w3/bdt_model_example.pkl -o /eos/user/f/fdmartin/FCC365_MVA_train_realsim_recoil/evaluate_plots_0_5_w3
```

In order to run the plot.py I have to run the following lines:
```bash
python final_selection.py 
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

## COMBINE  (I can't mix fccanalyses enviorement, if I used fisrt FCC I should to close the terminal session and start a new one with the following lines and viceverse)


```bash
cmssw-el7
``` 
```bash
cd CMSSW_10_2_13/src
```
```bash
cmsenv
```
# SIGNIFICANCE
```bash
combine -M Significance /eos/user/f/fdmartin/FCC365_MVA_train_realsim_recoil/higgs_combine/combine_recoil/mva_0_ZH_w3/datacard.txt -t -1 --expectSignal=1
```
# AsymptoticLimits
```bash
combine -M AsymptoticLimits /eos/user/f/fdmartin/FCC365_MVA_train_realsim_recoil/higgs_combine/combine_recoil/mva_0_ZH_w3/datacard.txt -t -1 --expectSignal=0
```
# FitDiagnostics
```bash
combine -M FitDiagnostics /eos/user/f/fdmartin/FCC365_MVA_train_realsim_recoil/higgs_combine/combine_recoil/mva_0_ZH_w3/datacard.txt -t -1 --expectSignal=1
```
# FitDiagnostics_V2
```bash
combine -M FitDiagnostics /eos/user/f/fdmartin/FCC365_MVA_train_realsim_recoil/higgs_combine/combine_recoil/VBF_analysis/datacard.txt -t -1 --expectSignal=1 --saveShapes --saveNormalizations
```
# Nuisances
```bash
python -b HiggsAnalysis/CombinedLimit/test/diffNuisances.py fitDiagnosticsTest.root -g nuisances.pdf
```
```bash
ls -lh nuisances.pdf
```
```bash
cat > nuisances_data_mva_0.txt
```
```bash
cat > impact_histogram_mva_0.py
```
```bash
# -*- coding: utf-8 -*-
import matplotlib
matplotlib.use('Agg')

import matplotlib.pyplot as plt
import numpy as np
import os # <--- IMPORTANTE: Módulo para operaciones del sistema operativo, como rutas

# --- Configuración ---
input_file = 'nuisances_data_mva_0_5_cut_3.txt' # Asume que está en el mismo directorio que el script

# Directorio donde quieres guardar el gráfico
output_directory = "/eos/user/f/fdmartin/FCC365_MVA_train_realsim_recoil/higgs_combine/combine_recoil/mva_0_5_cut_3_ZH_w3"
# Nombre del archivo PDF
output_filename = 'mi_grafico_de_impacto.png'

# Construir la ruta completa para el archivo de salida
output_file = os.path.join(output_directory, output_filename)

# --- Asegurarse de que el directorio de salida exista ---
# Si el directorio no existe, lo creamos.
try:
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)
        print u"Directorio de salida creado: {}".format(output_directory)
except OSError as e:
    print u"Error al crear el directorio de salida '{}': {}. Por favor, verifica la ruta y los permisos.".format(output_directory, e)
    # Podrías decidir salir del script si el directorio no se puede crear
    # import sys
    # sys.exit(1)


# --- Listas para almacenar los datos ---
param_names = []
postfit_values = []
postfit_errors = []

# --- Leer y procesar el archivo de datos ---
# (El resto del código para leer y procesar el archivo de datos permanece igual)
with open(input_file, 'r') as f:
    for line in f:
        if not line.strip():
            continue
        parts = line.split()
        param_names.append(parts[0])
        s_plus_b_fit_str = ''
        for part in parts:
            if ',' in part and part.startswith(('+', '-')):
                s_plus_b_fit_str = part.replace('!', '')
                s_plus_b_error_str = parts[parts.index(part) + 1].replace('!', '')
                break
        value_str, error_str = s_plus_b_fit_str, s_plus_b_error_str
        postfit_values.append(float(value_str.replace(',', '')))
        postfit_errors.append(float(error_str))

param_names.reverse()
postfit_values.reverse()
postfit_errors.reverse()

# --- Crear el Gráfico ---
# (El código para crear y formatear el gráfico permanece igual)
fig, ax = plt.subplots(figsize=(10, 8))
y_pos = np.arange(len(param_names))
ax.errorbar(postfit_values, y_pos, xerr=postfit_errors, fmt='o', color='black', ecolor='black', elinewidth=1, capsize=3)

ax.axvline(0, color='black', linestyle='--', linewidth=0.8)
ax.axvspan(-1, 1, alpha=0.2, color='green', label=u'Incertidumbre de 1σ')
ax.axvspan(-2, 2, alpha=0.2, color='yellow', zorder=0)
ax.set_yticks(y_pos)
ax.set_yticklabels(param_names)
ax.set_xlabel(u'Post-adjustment value of the parameter (\theta)', fontsize=12)
ax.set_ylabel(u' Nuisance Parameter', fontsize=12)
ax.set_title(u'Impact and Restriction of Nuisance Parameters', fontsize=14, weight='bold')
ax.set_xlim(-15, 15)
ax.grid(axis='x', linestyle='--', alpha=0.6)
plt.tight_layout()

# --- Guardar el Gráfico ---
# plt.savefig() ahora usará la ruta completa
try:
    plt.savefig(output_file)
    print u"¡Gráfico guardado exitosamente como '{}'!".format(output_file)
except Exception as e:
    print u"Error al guardar el gráfico en '{}': {}".format(output_file, e)
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

#!/bin/bash

# =================================================================
# Script de ejecución para trabajo de FCCAnalyses en el CERN Batch
# =================================================================

# --- Mensajes de inicio para seguimiento ---
echo "========================================================"
echo "Trabajo iniciado en el nodo: $(hostname)"
echo "Fecha de inicio: $(date)"
echo "========================================================"

# --- Configuración del Entorno (en el orden correcto) ---
echo "Configurando el entorno..."

# Paso 1: Cargar el entorno base de Key4hep (¡CRÍTICO!)
echo "Cargando Key4hep..."
source /cvmfs/sw.hsf.org/key4hep/setup.sh -r 2024-03-10

# Paso 2: Cargar la configuración local de FCCAnalyses
# ¡REEMPLAZA con la ruta absoluta a tu carpeta FCCanalyses!
echo "Cargando FCCAnalyses..."
source /afs/cern.ch/user/f/fdmartin/FCCAnalyses/setup.sh

echo "Entorno configurado correctamente."

# --- Ejecución del Análisis ---
# Paso 3: Ir a la carpeta EXACTA donde está tu script de análisis.
# ¡REEMPLAZA con la ruta absoluta a la carpeta de tu script!
cd /afs/cern.ch/user/f/fdmartin/FCCAnalyses/examples/FCCee/higgs/mva

echo "Directorio de trabajo cambiado a: $(pwd)"
echo "Ejecutando el análisis con el comando 'fccanalysis run'..."

# Paso 4: Ejecutar el análisis con el comando específico del framework.
fccanalysis run preselection_real_sim_infer_no_recoil_train.py

# --- Mensajes de finalización ---
echo "========================================================"
echo "El comando 'fccanalysis run' ha finalizado."
echo "Fecha de finalización: $(date)"
echo "========================================================"

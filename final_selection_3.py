#!/usr/bin/env python3
import os
import ROOT

# Directorios de entrada y salida
inputDir   = "/eos/user/f/fdmartin/FCC365_MVA_train_realsim/preselection_total_with_inference_previous"
outputDir  = "/eos/user/f/fdmartin/FCC365_MVA_train_realsim/final_selection"

# Lista de procesos (para filtrar ficheros, por ejemplo)
processList = {
    'p8_ee_WW_ecm365': {'fraction': 1},
    'wzp6_ee_numunumuH_Hbb_ecm365': {'fraction': 1},
    'wzp6_ee_nuenueH_Hbb_ecm365':  {'fraction': 1},
    'p8_ee_ZZ_ecm365': {'fraction': 1},
    'p8_ee_tt_ecm365': {'fraction': 1},
}

# Diccionario de cortes (aquí se definen las selecciones)
cutList = {
    "sel0": "1==1",  # selección trivial
    "sel1": "mva_score[0] > 0.5",
}

# Diccionario para histogramas
histoList = {
    "mva_score": {"cols": ["mva_score"], "title": "MVA score", "bins": [(100, 0, 1)]},
    "jj_m": {"cols": ["jj_m"], "title": "Dijet Mass (GeV)", "bins": [(200, 0, 365)]},
    "cosTheta_miss": {"cols": ["cosTheta_miss"], "title": "cos(θ_{miss})", "bins": [(100, -1, 1)]},
    "missingEnergy_energy_fixed": {"cols": ["missingEnergy_energy_fixed"], "title": "Missing Energy (GeV)", "bins": [(200, 0, 365)]},
    "missing_p_fixed": {"cols": ["missing_p_fixed"], "title": "Missing Momentum (GeV)", "bins": [(200, 0, 365)]},
}

# Parámetros de escalado
doScale = True
intLumi = 3000000.0  # 3 /ab

# Si se desea generar TTrees (no en este ejemplo)
doTree = False

def create_histograms():
    """
    Crea y devuelve un diccionario con histogramas de acuerdo a histoList.
    """
    hists = {}
    for hname, hparams in histoList.items():
        nb, xmin, xmax = hparams["bins"][0]
        hists[hname] = ROOT.TH1F(hname, hparams["title"], nb, xmin, xmax)
    return hists

def passes_cuts(event):
    """
    Aplica los cortes definidos en cutList.
    Aquí, únicamente usamos 'sel1' como ejemplo.
    """
    try:
        return getattr(event, "mva_score")[0] > 0.5
    except Exception as e:
        print("Error al evaluar corte en el evento:", e)
        return False

def process_file(file_path, hists):
    """
    Abre un fichero ROOT, obtiene el árbol (se asume que se llama 'events') y recorre
    los eventos, llenando los histogramas cuando se cumple el corte.
    """
    fIn = ROOT.TFile.Open(file_path)
    if not fIn or fIn.IsZombie():
        print("Error abriendo:", file_path)
        return
    tree = fIn.Get("events")  # Ajusta el nombre del árbol si es necesario
    if not tree:
        print("No se encontró el árbol 'events' en:", file_path)
        fIn.Close()
        return
    
    for event in tree:
        if passes_cuts(event):
            try:
                hists["mva_score"].Fill(getattr(event, "mva_score")[0])
            except Exception as e:
                print("Error llenando mva_score:", e)
            if hasattr(event, "jj_m"):
                hists["jj_m"].Fill(event.jj_m)
            if hasattr(event, "cosTheta_miss"):
                hists["cosTheta_miss"].Fill(event.cosTheta_miss)
            if hasattr(event, "missingEnergy_energy_fixed"):
                hists["missingEnergy_energy_fixed"].Fill(event.missingEnergy_energy_fixed)
            if hasattr(event, "missing_p_fixed"):
                hists["missing_p_fixed"].Fill(event.missing_p_fixed)
    fIn.Close()

def main():
    # Crear el directorio de salida si no existe
    if not os.path.exists(outputDir):
        os.makedirs(outputDir)
    
    # Obtener lista de ficheros ROOT en inputDir que coincidan con algún proceso en processList
    files = []
    for f in os.listdir(inputDir):
        if f.endswith(".root") and any(proc in f for proc in processList.keys()):
            files.append(os.path.join(inputDir, f))
    if not files:
        print("No se encontraron ficheros ROOT en el directorio de entrada.")
        return

    # Procesar cada fichero de forma individual
    for file_path in files:
        print("Procesando:", file_path)
        # Crear histogramas para este fichero
        histograms = create_histograms()
        # Procesar el fichero y llenar los histogramas
        process_file(file_path, histograms)
        
        # Aplicar escalado si es necesario
        if doScale:
            scaling_factor = 1.0  # Sustituir por el cálculo real si es necesario
            for hist in histograms.values():
                hist.Scale(scaling_factor)
        
        # Guardar los histogramas en un fichero de salida con el mismo nombre que el original
        base_name = os.path.basename(file_path)
        output_file_path = os.path.join(outputDir, base_name)
        outFile = ROOT.TFile(output_file_path, "RECREATE")
        for hist in histograms.values():
            hist.Write()
        outFile.Close()
        print("Histograma(s) guardado(s) en:", output_file_path)

if __name__ == '__main__':
    main()


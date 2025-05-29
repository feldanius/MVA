#!/usr/bin/env python3
import os
import ROOT

# Directorios de entrada y salida
inputDir   = "/eos/user/f/fdmartin/FCC365_MVA_train_realsim_recoil/preselection_total_with_inference"
outputDir  = "/eos/user/f/fdmartin/FCC365_MVA_train_realsim_recoil/final_selection_cuts/mva_5_sigma"
#outputDir  = "/eos/user/f/fdmartin/FCC365_MVA_train_realsim_recoil/final_selection_cuts/mva_cut1_5_sigma"
#outputDir  = "/eos/user/f/fdmartin/FCC365_MVA_train_realsim_recoil/final_selection_cuts/mva_cut2_5_sigma"
#outputDir  = "/eos/user/f/fdmartin/FCC365_MVA_train_realsim_recoil/final_selection_cuts/mva_cut3_5_sigma"
#outputDir  = "/eos/user/f/fdmartin/FCC365_MVA_train_realsim_recoil/final_selection_cuts/mva_0_2_5_sigma"
#outputDir  = "/eos/user/f/fdmartin/FCC365_MVA_train_realsim_recoil/final_selection_cuts/mva_0_2_cut_1_5_sigma"
#outputDir  = "/eos/user/f/fdmartin/FCC365_MVA_train_realsim_recoil/final_selection_cuts/mva_0_2_cut_2_5_sigma"
#outputDir  = "/eos/user/f/fdmartin/FCC365_MVA_train_realsim_recoil/final_selection_cuts/mva_0_2_cut_3_5_sigma"
#outputDir  = "/eos/user/f/fdmartin/FCC365_MVA_train_realsim_recoil/final_selection_cuts/mva_0_5_5_sigma"
#outputDir  = "/eos/user/f/fdmartin/FCC365_MVA_train_realsim_recoil/final_selection_cuts/mva_0_5_cut_1_5_sigma"
#outputDir  = "/eos/user/f/fdmartin/FCC365_MVA_train_realsim_recoil/final_selection_cuts/mva_0_5_cut_2_5_sigma"
#outputDir  = "/eos/user/f/fdmartin/FCC365_MVA_train_realsim_recoil/final_selection_cuts/mva_0_5_cut_3_5_sigma"

# Lista de procesos (para filtrar ficheros, por ejemplo)
processList = {
    'p8_ee_WW_ecm365': {'fraction': 1, 'crossSection': 10.7165 },
    'wzp6_ee_numunumuH_Hbb_ecm365': {'fraction': 1, 'crossSection': 0.004814},
    'wzp6_ee_nuenueH_Hbb_ecm365':  {'fraction': 1, 'crossSection': 0.02181},
    'p8_ee_ZZ_ecm365': {'fraction': 1, 'crossSection': 0.6428},
    'p8_ee_tt_ecm365': {'fraction': 1, 'crossSection': 0.8},
}

# Diccionario de cortes (aquí se definen las selecciones)
cutList = {
    "sel_mva":                  "mva_score[0] > 0",
   # "sel_hbb_p":                "hbb_p < 90",
   # "sel_higgs_recoil_m":       "higgs_recoil_m > 200",
   # "sel_missingEnergy":        "missingEnergy_energy_fixed > 190",
}


# Diccionario para histogramas
histoList = {
    "mva_score": {"cols": ["mva_score"], "title": "MVA score", "bins": [(100, 0, 1)]},
    "jj_m": {"cols": ["jj_m"], "title": "Dijet Mass (GeV)", "bins": [(200, 0, 365)]},
    "cosTheta_miss": {"cols": ["cosTheta_miss"], "title": "cos(θ_{miss})", "bins": [(100, -1, 1)]},
    "missingEnergy_energy_fixed": {"cols": ["missingEnergy_energy_fixed"], "title": "Missing Energy (GeV)", "bins": [(200, 0, 365)]},
    "missing_p_fixed": {"cols": ["missing_p_fixed"], "title": "Missing Momentum (GeV)", "bins": [(200, 0, 365)]},
    "hbb_m": {"cols": ["hbb_m"], "title": "Resonance Builder Mass", "bins": [(200, 0, 365)]},
    "hbb_p": {"cols": ["hbb_p"], "title": "Resonance Builder Momentum", "bins": [(200, 0, 365)]},
    "higgs_recoil_m": {"cols": ["higgs_recoil_m"], "title": "Higgs Recoil Mass", "bins": [(200, 0, 365)]},
}

# Parámetros de escalado
doScale = True
intLumi = 144.0  # 0.000144/ab
#intLumi = 320.0  # 0.00032/ab
#intLumi = 310.0  # 0.00031/ab
#intLumi = 290.0  # 0.00029/ab
#intLumi = 137.0  # 0.000137/ab
#intLumi = 283.0  # 0.000283/ab
#intLumi = 284.0  # 0.000284/ab
#intLumi = 287.0  # 0.000287/ab
#intLumi = 156.0  # 0.000156/ab
#intLumi = 288.0  # 0.000288/ab
#intLumi = 290.0  # 0.000290/ab
#intLumi = 291.0  # 0.000291/ab
#intLumi = 3000000.0  # 3 /ab

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
    Aplica secuencialmente todos los cortes en `cutList`.
    """
    # crea un diccionario con todas las variables que uses en los cortes
    vars = {
        "mva_score":                  event.mva_score,                # arreglo
        #"hbb_p":                      getattr(event, "hbb_p", None),
        #"higgs_recoil_m":             getattr(event, "higgs_recoil_m", None),
        #"missingEnergy_energy_fixed": getattr(event, "missingEnergy_energy_fixed", None),
    }
    # evalúa cada corte; si falla alguno, rechaza el evento
    for name, expr in cutList.items():
        try:
            if not eval(expr, {}, vars):
                return False
        except Exception as e:
            print(f"Error al evaluar corte {name} ('{expr}'): {e}")
            return False
    return True


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
            if hasattr(event, "hbb_m"):
                hists["hbb_m"].Fill(event.hbb_m)
            if hasattr(event, "hbb_p"):
                hists["hbb_p"].Fill(event.hbb_p)
            if hasattr(event, "higgs_recoil_m"):
                hists["higgs_recoil_m"].Fill(event.higgs_recoil_m)
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
            crossSection = processList[proc_found]['crossSection']
            #fraction = processList[proc_found]['fraction']
            total_events = total_events_per_process[proc_found]
            scaling_factor = (intLumi * crossSection) / total_events
            print(f"  Factor de escala para {proc_found}: {scaling_factor:.6e}")
            #scaling_factor = intLumi*crossSection 
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

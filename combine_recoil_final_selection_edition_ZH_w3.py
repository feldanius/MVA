import ROOT

#flavor = "mumu" # mumu, ee

intLumi         = 1.0
outputDir       = "/eos/user/f/fdmartin/FCC365_MVA_train_realsim_recoil/higgs_combine/combine_recoil/mva_0_cut_3_ZH_w3"
mc_stats        = True
rebin           = 10
inputDir        = "/eos/user/f/fdmartin/FCC365_MVA_train_realsim_recoil/higgs_combine/final_selection/MVA_0"
selection       = "sel3"

# --- CAMBIO PRINCIPAL AQUÍ ---
# Define cada proceso físico como una categoría separada.
# La clave del diccionario será el nombre del proceso en el datacard.

sig_procs = {
    # Este es tu proceso de señal ZH
    'VBF_sig': ["wzp6_ee_nuenueH_Hbb_ecm365", "wzp6_ee_numunumuH_Hbb_ecm365"]
}

bkg_procs = {
    # Este es el MISMO proceso, pero ahora lo llamas 'ZH_bkg' y apuntas a los archivos pre-escalados
    'ZH': ["wzp6_ee_numunumuH_Hbb_ecm365_ZH"],
    
    # El resto de los fondos, cada uno como su propio proceso
    'ZZ': ["p8_ee_ZZ_ecm365"],
    'WW': ["p8_ee_WW_ecm365"],
    'tt': ["p8_ee_tt_ecm365"]
}

# El resto del script no necesita cambios
categories = ["recoil"]
hist_names = ["higgs_recoil_m_final"]

systs = {}

systs['lumi'] = {
    'type': 'lnN',
    'value': 1.01, # Ejemplo
    'procs': '.*', 
}

# Incertidumbres de normalización para cada fondo
systs['bkg_norm_ZH'] = {
    'type': 'lnN',
    'value': 1.02, # Ejemplo
    'procs': ['ZH'], 
}

systs['bkg_norm_ZZ'] = {
    'type': 'lnN',
    'value': 1.005, # Ejemplo
    'procs': ['ZZ'],
}

systs['bkg_norm_WW'] = {
    'type': 'lnN',
    'value': 1.005, # Ejemplo
    'procs': ['WW'],
}

systs['bkg_norm_tt'] = {
    'type': 'lnN',
    'value': 1.05, # Ejemplo
    'procs': ['tt'],
}

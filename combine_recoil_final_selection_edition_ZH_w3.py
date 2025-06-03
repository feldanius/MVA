import ROOT

#flavor = "mumu" # mumu, ee

intLumi         = 1.0
outputDir       = "/eos/user/f/fdmartin/FCC365_MVA_train_realsim_recoil/higgs_combine/combine_recoil/mva_0_ZH_w3"
mc_stats        = True
rebin           = 10
inputDir        = "/eos/user/f/fdmartin/FCC365_MVA_train_realsim_recoil/higgs_combine/final_selection/MVA_0"
selection       = "sel0"

sig_procs = {
    'VBF_sig': ["wzp6_ee_nuenueH_Hbb_ecm365", "wzp6_ee_numunumuH_Hbb_ecm365"]
}

bkg_procs = {
    'ZH': ["wzp6_ee_numunumuH_Hbb_ecm365_ZH"],
    'ZZ': ["p8_ee_ZZ_ecm365"],
    'WW': ["p8_ee_WW_ecm365"],
    'tt': ["p8_ee_tt_ecm365"]
}

categories = ["recoil"]
hist_names = ["higgs_recoil_m_final"]

systs = {}

systs['lumi'] = {
    'type': 'lnN',
    'value': 1.01,
    'procs': '.*', 
}

systs['bkg_norm_ZH'] = {
    'type': 'lnN',
    'value': 1.02, 
    'procs': ['ZH'], 
}

systs['bkg_norm_ZZ'] = {
    'type': 'lnN',
    'value': 1.005, 
    'procs': ['ZZ'],
}

systs['bkg_norm_WW'] = {
    'type': 'lnN',
    'value': 1.005, 
    'procs': ['WW'],
}

systs['bkg_norm_tt'] = {
    'type': 'lnN',
    'value': 1.05, 
    'procs': ['tt'],
}

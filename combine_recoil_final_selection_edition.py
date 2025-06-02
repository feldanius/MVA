import ROOT

#flavor = "mumu" # mumu, ee

intLumi        = 1.0 # assume histograms are scaled in previous step
outputDir      = "/eos/user/f/fdmartin/FCC365_MVA_train_realsim_recoil/higgs_combine/combine_recoil/mva_0_cut_3"
mc_stats       = True
rebin          = 10

# get histograms from histmaker step
#inputDir       = f"outputs/FCCee/higgs/mass-xsec/histmaker/{flavor}/"

# get histograms from final step, selection to be defined
inputDir       = "/eos/user/f/fdmartin/FCC365_MVA_train_realsim_recoil/higgs_combine/final_selection/MVA_0"
selection      = "sel3"


sig_procs = {'sig':["wzp6_ee_nuenueH_Hbb_ecm365", "wzp6_ee_numunumuH_Hbb_ecm365"]}
bkg_procs = {'bkg':["p8_ee_ZZ_ecm365", "p8_ee_WW_ecm365", "p8_ee_tt_ecm365", "wzp6_ee_numunumuH_Hbb_ecm365"]}


categories = ["recoil"]
hist_names = ["higgs_recoil_m_final"]


systs = {}

systs['bkg_norm'] = {
    'type': 'lnN',
    'value': 1.10,
    'procs': ['bkg'],
}

systs['lumi'] = {
    'type': 'lnN',
    'value': 1.01,
    'procs': '.*',
}

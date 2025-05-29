import ROOT

flavor = "mumu" # mumu, ee

intLumi        = 1.0 # assume histograms are scaled in previous step
outputDir  = "/eos/user/f/fdmartin/FCC365_MVA_train_realsim_recoil/higgs_combine/mva"
#outputDir  = "/eos/user/f/fdmartin/FCC365_MVA_train_realsim_recoil/higgs_combine/mva_cut_1"
#outputDir  = "/eos/user/f/fdmartin/FCC365_MVA_train_realsim_recoil/higgs_combine/mva_cut_2"
#outputDir  = "/eos/user/f/fdmartin/FCC365_MVA_train_realsim_recoil/higgs_combine/mva_cut_3"
#outputDir  = "/eos/user/f/fdmartin/FCC365_MVA_train_realsim_recoil/higgs_combine/mva_0_2"
#outputDir  = "/eos/user/f/fdmartin/FCC365_MVA_train_realsim_recoil/higgs_combine/mva_0_2_cut_1"
#outputDir  = "/eos/user/f/fdmartin/FCC365_MVA_train_realsim_recoil/higgs_combine/mva_0_2_cut_2"
#outputDir  = "/eos/user/f/fdmartin/FCC365_MVA_train_realsim_recoil/higgs_combine/mva_0_2_cut_3"
#outputDir  = "/eos/user/f/fdmartin/FCC365_MVA_train_realsim_recoil/higgs_combine/mva_0_5"
#outputDir  = "/eos/user/f/fdmartin/FCC365_MVA_train_realsim_recoil/higgs_combine/mva_0_5_cut_1"
#outputDir  = "/eos/user/f/fdmartin/FCC365_MVA_train_realsim_recoil/higgs_combine/mva_0_5_cut_2"
#outputDir  = "/eos/user/f/fdmartin/FCC365_MVA_train_realsim_recoil/higgs_combine/mva_0_5_cut_3"
mc_stats       = True
rebin          = 10

# get histograms from histmaker step
inputDir  = "/eos/user/f/fdmartin/FCC365_MVA_train_realsim_recoil/final_selection_cuts/mva_5_sigma"
#inputDir  = "/eos/user/f/fdmartin/FCC365_MVA_train_realsim_recoil/final_selection_cuts/mva_cut1_5_sigma"
#inputDir  = "/eos/user/f/fdmartin/FCC365_MVA_train_realsim_recoil/final_selection_cuts/mva_cut2_5_sigma"
#inputDir  = "/eos/user/f/fdmartin/FCC365_MVA_train_realsim_recoil/final_selection_cuts/mva_cut3_5_sigma"
#inputDir  = "/eos/user/f/fdmartin/FCC365_MVA_train_realsim_recoil/final_selection_cuts/mva_0_2_5_sigma"
#inputDir  = "/eos/user/f/fdmartin/FCC365_MVA_train_realsim_recoil/final_selection_cuts/mva_0_2_cut_1_5_sigma"
#inputDir  = "/eos/user/f/fdmartin/FCC365_MVA_train_realsim_recoil/final_selection_cuts/mva_0_2_cut_2_5_sigma"
#inputDir  = "/eos/user/f/fdmartin/FCC365_MVA_train_realsim_recoil/final_selection_cuts/mva_0_2_cut_3_5_sigma"
#inputDir  = "/eos/user/f/fdmartin/FCC365_MVA_train_realsim_recoil/final_selection_cuts/mva_0_5_5_sigma"
#inputDir  = "/eos/user/f/fdmartin/FCC365_MVA_train_realsim_recoil/final_selection_cuts/mva_0_5_cut_1_5_sigma"
#inputDir  = "/eos/user/f/fdmartin/FCC365_MVA_train_realsim_recoil/final_selection_cuts/mva_0_5_cut_2_5_sigma"
#inputDir  = "/eos/user/f/fdmartin/FCC365_MVA_train_realsim_recoil/final_selection_cuts/mva_0_5_cut_3_5_sigma"


# get histograms from final step, selection to be defined
#inputDir       = f"outputs/FCCee/higgs/mass-xsec/final_selection/{flavor}/"
#selection      = "sel3"


sig_procs = {'sig':["wzp6_ee_nuenueH_Hbb_ecm365", "wzp6_ee_numunumuH_Hbb_ecm365"]}
bkg_procs = {'bkg':["p8_ee_ZZ_ecm365", "p8_ee_WW_ecm365", "p8_ee_tt_ecm365", "wzp6_ee_numunumuH_Hbb_ecm365"]}


categories = ["recoil"]
hist_names = ["hbb_m"]


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

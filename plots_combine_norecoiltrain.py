import ROOT


# global parameters
intLumi        = 1.
intLumiLabel   = "L = 3 ab^{-1}"
ana_tex        = '(VBF) e^{+}e^{-} #nu^{+}#nu^{-} H #rightarrow b^{+} b^{-}'
delphesVersion = '3.4.2'
energy         = 365.0
collider       = 'FCC-ee'
inputDir       = "/eos/user/f/fdmartin/FCC365_MVA_train_realsim/higgs_combine/final_selection/MVA_0/"
#inputDir       = "/eos/user/f/fdmartin/FCC365_MVA_train_realsim/higgs_combine/final_selection/MVA_0_2/"
#inputDir       = "/eos/user/f/fdmartin/FCC365_MVA_train_realsim/higgs_combine/final_selection/MVA_0_5/"
formats        = ['png','pdf']
outdir         = "/eos/user/f/fdmartin/FCC365_MVA_train_realsim/higgs_combine/plots_final_selection/MVA_0"
#outdir         = "/eos/user/f/fdmartin/FCC365_MVA_train_realsim/higgs_combine/plots_final_selection/MVA_0_2"
#outdir         = "/eos/user/f/fdmartin/FCC365_MVA_train_realsim/higgs_combine/plots_final_selection/MVA_0_5"
yaxis          = ['lin','log']
stacksig       = ['nostack']
plotStatUnc    = True

variables = ['mva_score', 'hbb_p', 'higgs_recoil', 'missingEnergy_energy_fixed', 'higgs_recoil_final']
rebin = [1, 1] # uniform rebin per variable (optional)


selections = {}
selections['VBF']   = ["sel0"]
#selections['VBF']   = ["sel0", "sel1", "sel2", "sel3" ]

extralabel = {}
extralabel['sel0'] = "MVA > 0.2"
#extralabel['sel1'] = "hbb_p < 90 GeV"
#extralabel['sel0'] = "higgs_recoil_m > 120 GeV"
#extralabel['sel1'] = "MET > 190 GeV"


colors = {}
colors["VBF"] = ROOT.kRed
colors["ZZ"] = ROOT.kGreen + 2
colors["WW"] = ROOT.kCyan - 2
colors["tt"] = ROOT.kBlue - 2
colors["ZH"] = ROOT.kMagenta - 8


plots = {}
plots['VBF'] = {'signal':{'VBF':["wzp6_ee_nuenueH_Hbb_ecm365", "wzp6_ee_numunumuH_Hbb_ecm365"]},
               'backgrounds':{ 'ZZ': ["p8_ee_ZZ_ecm365"], 'WW': ["p8_ee_WW_ecm365"], 'tt': ["p8_ee_tt_ecm365"], 'ZH': ["wzp6_ee_numunumuH_Hbb_ecm365_ZH"] }
           }

legend = {}
legend["VBF"] = "VBF"
legend["ZZ"] = "ZZ"
legend["WW"] = "WW"
legend["tt"] = "tt"
legend["ZH"] = "ZH"


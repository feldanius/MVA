import ROOT


# global parameters
intLumi        = 1.
intLumiLabel   = "L = 3 ab^{-1}"
ana_tex        = '(VBF) e^{+}e^{-} #nu^{+}#nu^{-} H #rightarrow #b^{+}#b^{-}'
delphesVersion = '3.4.2'
energy         = 365.0
collider       = 'FCC-ee'
inputDir       = "/eos/user/f/fdmartin/FCC365_MVA_train_realsim/final_selection"
formats        = ['png','pdf']
outdir         = "/eos/user/f/fdmartin/FCC365_MVA_train_realsim/final_selection/plots_0_5"
yaxis          = ['lin','log']
stacksig       = ['nostack']
plotStatUnc    = True




variables = ['mva_score', 'jj_m', 'cosTheta_miss', 'missingEnergy_energy_fixed', 'missing_p_fixed']
rebin = [1, 1] # uniform rebin per variable (optional)

###Dictonnary with the analysis name as a key, and the list of selections to be plotted for this analysis. The name of the selections should be the same than in the final selection
selections = {}
selections['VBF']   = ["sel0", "sel1"]

extralabel = {}
extralabel['sel0'] = "Basic selection"
extralabel['sel1'] = "MVA > 0.5"

colors = {}
colors["VBF"] = ROOT.kRed
colors["ZZ"] = ROOT.kGreen + 2
colors["WW"] = ROOT.kCyan - 2
colors["tt"] = ROOT.kBlue - 2
colors["ZH"] = ROOT.kMagenta - 8


plots = {}
plots['ZH'] = {'signal':{"VBF": ["wzp6_ee_nuenueH_Hbb_ecm365", "wzp6_ee_numunumuH_Hbb_ecm365"]},
               'backgrounds':{ "ZZ": ["p8_ee_ZZ_ecm365"], "WW": ["p8_ee_WW_ecm365"], "tt": ["p8_ee_tt_ecm365"], "ZH": ["wzp6_ee_numunumuH_Hbb_ecm365"] }
           }

legend = {}
legend["VBF"] = "VBF"
legend["ZZ"] = "ZZ"
legend["WW"] = "WW"
legend["tt"] = "tt"
legend["ZH"] = "ZH"

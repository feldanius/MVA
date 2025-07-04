import ROOT


# global parameters
intLumi        = 1.
intLumiLabel   = "L = 3 ab^{-1}"
ana_tex        = '(VBF) e^{+}e^{-} #nu^{+}#nu^{-} H #rightarrow #b^{+}#b^{-}'
delphesVersion = '3.4.2'
energy         = 365.0
collider       = 'FCC-ee'
inputDir       = "/eos/user/f/fdmartin/FCC365_MVA_train_realsim/final_selection/mva_0_5"
#inputDir       = "/eos/user/f/fdmartin/FCC365_MVA_train_realsim/final_selection/mva_0_2"
#inputDir       = "/eos/user/f/fdmartin/FCC365_MVA_train_realsim/final_selection/mva_total"
formats        = ['png','pdf']
outdir         = "/eos/user/f/fdmartin/FCC365_MVA_train_realsim/plots/plots_0_5_non_stack_signal"
#outdir         = "/eos/user/f/fdmartin/FCC365_MVA_train_realsim/plots/plots_0_2_non_stack_signal"
#outdir         = "/eos/user/f/fdmartin/FCC365_MVA_train_realsim/plots/plots_no_mva_cut_non_stack_signal"
yaxis          = ['lin','log']
#stacksig       = ['nostack']
plotStatUnc    = True

colors = {}
#colors["Signal VBF"] = ROOT.kRed
#colors["Backgrounds"] = ROOT.kGreen + 2
colors["VBF"] = ROOT.kRed
colors["ZZ"] = ROOT.kGreen + 2
colors["WW"] = ROOT.kCyan - 2
colors["tt"] = ROOT.kBlue - 2
colors["ZH"] = ROOT.kMagenta - 8


procs = {}
procs["signal"] = {"VBF": ["wzp6_ee_nuenueH_Hbb_ecm365", "wzp6_ee_numunumuH_Hbb_ecm365"]}
#procs["Signal VBF"] = {"Signal VBF": ["wzp6_ee_nuenueH_Hbb_ecm365", "wzp6_ee_numunumuH_Hbb_ecm365"]}
procs["backgrounds"] = { "ZZ": ["p8_ee_ZZ_ecm365"], "WW": ["p8_ee_WW_ecm365"], "tt": ["p8_ee_tt_ecm365"], "ZH": ["wzp6_ee_numunumuH_Hbb_ecm365"] }
#procs["Backgrounds"] = { "Backgrounds": ["p8_ee_ZZ_ecm365", "p8_ee_WW_ecm365", "p8_ee_tt_ecm365", "wzp6_ee_numunumuH_Hbb_ecm365"] }

legend = {}
#legend["Signal VBF"] = "Signal VBF"
#legend["Backgrounds"] = "Backgrounds"
legend["VBF"] = "VBF"
legend["ZZ"] = "ZZ"
legend["WW"] = "WW"
legend["tt"] = "tt"
legend["ZH"] = "ZH"

hists = {}

hists["missingEnergy_energy_fixed"] = {
    "output": "missingEnergy_energy_fixed",
    "logy": False,
    "stack": True,
    #"stack_signal": False,
    "rebin": 2,
    "xmin": 130,
    "xmax": 350,
    "ymin": 0,
    "ymax": 400000,
    "xtitle": "MET (GeV)",
    "ytitle": "Events / 2 GeV",
}

hists["missing_p_fixed"] = {
    "output": "missing_p_fixed",
    "logy": False,
    "stack": True,
    #"stack_signal": False,
    "rebin": 2,
    "xmin": 0,
    "xmax": 190,
    "ymin": 0,
    "ymax": 550000,
    "xtitle": "Missing_p (GeV)",
    "ytitle": "Events / 2 GeV",
}

hists["jj_m"] = {
    "output": "jj_m",
    "logy": False,
    "stack": True,
    #"stack_signal": False,
    "rebin": 2,
    "xmin": 0,
    "xmax": 250,
    "ymin": 0,
    "ymax": 500000,
    "xtitle": "m_{jj} (GeV)",
    "ytitle": "Events / 2 GeV",
}


hists["mva_score"] = {
    "output": "mva_score",
    "logy": True,
    "stack": True,
    #"stack_signal": False,
    "rebin": 1,
    "xmin": 0.5,
    "xmax": 1,
    "ymin": 1,
    "ymax": 600000,
    "xtitle": "mva_score",
    "ytitle": "Events",
}


hists["cosTheta_miss"] = {
    "output": "cosTheta_miss",
    "logy": False,
    "stack": True,
    #"stack_signal": False,
    "rebin": 1,
    "xmin": 0,
    "xmax": 1.0,
    "ymin": 0,
    "ymax": 250000,
    "xtitle": "cosTheta_miss",
    "ytitle": "Events",
}

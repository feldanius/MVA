import ROOT


# global parameters
intLumi        = 1.
intLumiLabel   = "L = 3 ab^{-1}"
ana_tex        = '(VBF) e^{+}e^{-} #nu^{+}#nu^{-} H #rightarrow b^{+} b^{-}'
delphesVersion = '3.4.2'
energy         = 365.0
collider       = 'FCC-ee'
#inputDir       = "/eos/user/f/fdmartin/FCC365_MVA_train_realsim_recoil/final_selection_cuts/mva_0_5_cut3"
inputDir       = "/eos/user/f/fdmartin/FCC365_MVA_train_realsim_recoil/final_selection_cuts/mva_0_2"
#inputDir       = "/eos/user/f/fdmartin/FCC365_MVA_train_realsim_recoil/final_selection_cuts/mva_total"
formats        = ['png','pdf']
#outdir         = "/eos/user/f/fdmartin/FCC365_MVA_train_realsim_recoil/plots_cut/plots_0_5"
outdir         = "/eos/user/f/fdmartin/FCC365_MVA_train_realsim_recoil/plots_cut/plots_0_2"
#outdir         = "/eos/user/f/fdmartin/FCC365_MVA_train_realsim_recoil/plots_cut/plots_no_mva_cut"
yaxis          = ['lin','log']
stacksig       = ['nostack']
plotStatUnc    = True




#variables = ['mva_score', 'jj_m', 'cosTheta_miss', 'missingEnergy_energy_fixed', 'missing_p_fixed']
#rebin = [1, 1] # uniform rebin per variable (optional)

###Dictonnary with the analysis name as a key, and the list of selections to be plotted for this analysis. The name of the selections should be the same than in the final selection
#selections = {}
#selections['VBF']   = ["mva_score"]


colors = {}
colors["VBF"] = ROOT.kRed
colors["ZZ"] = ROOT.kGreen + 2
colors["WW"] = ROOT.kCyan - 2
colors["tt"] = ROOT.kBlue - 2
colors["ZH"] = ROOT.kMagenta - 8


procs = {}
procs["signal"] = {"VBF": ["wzp6_ee_nuenueH_Hbb_ecm365", "wzp6_ee_numunumuH_Hbb_ecm365"]}
procs["backgrounds"] = { "ZZ": ["p8_ee_ZZ_ecm365"], "WW": ["p8_ee_WW_ecm365"], "tt": ["p8_ee_tt_ecm365"], "ZH": ["wzp6_ee_numunumuH_Hbb_ecm365"] }

legend = {}
legend["VBF"] = "VBF"
legend["ZZ"] = "ZZ"
legend["WW"] = "WW"
legend["tt"] = "tt"
legend["ZH"] = "ZH"

hists = {}

hists["missingEnergy_energy_fixed"] = {
    "output": "missingEnergy_energy_fixed",
    "logy": False,
    "stack": False,
    "rebin": 2,
    "xmin": 185,
    "xmax": 265,
    "ymin": 0,
    "ymax": 48000,
    "xtitle": "MET (GeV)",
    "ytitle": "Events",
}

hists["missing_p_fixed"] = {
    "output": "missing_p_fixed",
    "logy": False,
    "stack": False,
    "rebin": 2,
    "xmin": 0,
    "xmax": 150,
    "ymin": 0,
    "ymax": 25000,
    "xtitle": "Missing_p (GeV)",
    "ytitle": "Events",
}

hists["jj_m"] = {
    "output": "jj_m",
    "logy": False,
    "stack": False,
    "rebin": 2,
    "xmin": 90,
    "xmax": 130,
    "ymin": 0,
    "ymax": 90000,
    "xtitle": "m_{jj} (GeV)",
    "ytitle": "Events",
}

hists["hbb_m"] = {
    "output": "hbb_m",
    "logy": False,
    "stack": False,
    "rebin": 2,
    "xmin": 90,
    "xmax": 130,
    "ymin": 0,
    "ymax": 95000,
    "xtitle": "RecoBuilder_mass (GeV)",
    "ytitle": "Events ",
}

hists["hbb_p"] = {
    "output": "hbb_p",
    "logy": False,
    "stack": False,
    "rebin": 2,
    "xmin": 0,
    "xmax": 100,
    "ymin": 0,
    "ymax": 35000,
    "xtitle": "RecoBuilder_p (GeV)",
    "ytitle": "Events",
}

hists["higgs_recoil_m"] = {
    "output": "higgs_recoil_m",
    "logy": False,
    "stack": False,
    "rebin": 2,
    "xmin": 190,
    "xmax": 280,
    "ymin": 0,
    "ymax": 38000,
    "xtitle": "higgs_recoil_mass (GeV)",
    "ytitle": "Events",
}


hists["mva_score"] = {
    "output": "mva_score",
    "logy": False,
    "stack": False,
    "rebin": 2,
    "xmin": 0.2,
    "xmax": 1,
    "ymin": 1,
    "ymax": 900000,
    "xtitle": "mva_score",
    "ytitle": "Events",
}


hists["cosTheta_miss"] = {
    "output": "cosTheta_miss",
    "logy": False,
    "stack": False,
    "rebin": 2,
    "xmin": 0,
    "xmax": 1.0,
    "ymin": 0,
    "ymax": 12000,
    "xtitle": "cosTheta_miss",
    "ytitle": "Events",
}

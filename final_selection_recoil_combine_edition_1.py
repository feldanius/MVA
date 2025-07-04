
#flavor = "mumu" # mumu, ee

#Input directory where the files produced at the pre-selection level are
#inputDir   = f"outputs/FCCee/higgs/mass-xsec/preselection/{flavor}/"
inputDir   = "/eos/user/f/fdmartin/FCC365_MVA_train_realsim_recoil/preselection_total_with_inference"

#Input directory where the files produced at the pre-selection level are
#Optional: output directory, default is local running directory
#outputDir   = f"outputs/FCCee/higgs/mass-xsec/final_selection/{flavor}/"
outputDir   = "/eos/user/f/fdmartin/FCC365_MVA_train_realsim_recoil/higgs_combine/final_selection/MVA_0"

# if no processList or empty dictionary provided, run over all ROOT files in the input directory
processList = {}

#Link to the dictonary that contains all the cross section informations etc...
procDict = "FCCee_procDict_winter2023_IDEA.json"

#Number of CPUs to use
nCPUS = -1

#produces ROOT TTrees, default is False
doTree = False


# scale the histograms with the cross-section and integrated luminosity
doScale = True
intLumi = 3000000.0 # 3 /ab

saveTabular = True

###Dictionnay of the list of cuts. The key is the name of the selection that will be added to the output file
sel0 = "(mva_score[0] > 0)"
sel1 = "(hbb_p < 90)"
sel2 = "(higgs_recoil_m > 120)"
sel3 = "(missingEnergy_energy_fixed > 190)"
cutList = {
    "sel0": f"{sel0}",
    "sel1": f"{sel0} && {sel1}",
    "sel2": f"{sel0} && {sel1} && {sel2}",
    "sel3": f"{sel0} && {sel1} && {sel2} && {sel3}"
}


#Dictionary for the ouput variable/hitograms. The key is the name of the variable in the output files. "name" is the name of the variable in the input file, "title" is the x-axis label of the histogram, "bin" the number of bins of the histogram, "xmin" the minimum x-axis value and "xmax" the maximum x-axis value.
histoList = {
    "mva_score":{"cols": ["mva_score"], "title": " (GeV)", "bins": [(250,0,250)]},
    "recobuilder":{"cols": ["hbb_p"], "title": "recoil_m (GeV)", "bins": [(250,0,120)]},
    "MET":{"cols": ["missingEnergy_energy_fixed"], "title": "MET (GeV)", "bins": [(120,180,300)]},
    "higgs_recoil":{"cols": ["higgs_recoil_m"], "title": "Recoil (GeV)", "bins": [(250,0,250)]},
    "higgs_recoil_final":{"cols": ["higgs_recoil_m"], "title": "Recoil (GeV)", "bins": [(130,120,250)]},
}

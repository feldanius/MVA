# Configuración básica
inputDir   = "outputs/FCCee/higgs/mva/preselection/"
outputDir  = "outputs/FCCee/higgs/mva/final_selection/"
processList = {}
procDict = "FCCee_procDict_winter2023_IDEA.json"
nCPUS = -1
doTree = False
doScale = True
intLumi = 3000000.0  # 3 /ab
saveTabular = True

### Diccionario de cortes
cutList = {
    "sel0": "1==1",
    "sel1": "mva_score[0] > 0.5",
}

### Diccionario de histogramas
histoList = {
    "mva_score": {"cols": ["mva_score"], "title": "MVA score", "bins": [(100, 0, 1)]},
    "jj_m": {"cols": ["jj_m"], "title": "Dijet Mass (GeV)", "bins": [(200, 0, 365)]},
    "cosTheta_miss": {"cols": ["cosTheta_miss"], "title": "cos(θ_{miss})", "bins": [(100, -1, 1)]},
    "missingEnergy": {"cols": ["missingEnergy.energy"], "title": "Missing Energy (GeV)", "bins": [(200, 0, 365)]},
    "missing_p": {"cols": ["missing_p"], "title": "Missing Momentum (GeV)", "bins": [(200, 0, 365)]},
}

def build_graph(df, dataset):
    """
    Función que aplica los cortes y crea los histogramas.
    """
    # Aplicar corte: mva_score[0] > 0.5
    df_sel = df.Filter(cutList["sel1"], "MVA cut")
    
    # Crear histogramas usando las configuraciones definidas
    h_mva_score = df_sel.Histo1D(
        ("mva_score", histoList["mva_score"]["title"], *histoList["mva_score"]["bins"][0]),
        histoList["mva_score"]["cols"][0]
    )
    h_jj_m = df_sel.Histo1D(
        ("jj_m", histoList["jj_m"]["title"], *histoList["jj_m"]["bins"][0]),
        histoList["jj_m"]["cols"][0]
    )
    h_cosTheta_miss = df_sel.Histo1D(
        ("cosTheta_miss", histoList["cosTheta_miss"]["title"], *histoList["cosTheta_miss"]["bins"][0]),
        histoList["cosTheta_miss"]["cols"][0]
    )
    h_missingEnergy = df_sel.Histo1D(
        ("missingEnergy", histoList["missingEnergy"]["title"], *histoList["missingEnergy"]["bins"][0]),
        histoList["missingEnergy"]["cols"][0]
    )
    h_missing_p = df_sel.Histo1D(
        ("missing_p", histoList["missing_p"]["title"], *histoList["missing_p"]["bins"][0]),
        histoList["missing_p"]["cols"][0]
    )
    
    histos = {
        "mva_score": h_mva_score,
        "jj_m": h_jj_m,
        "cosTheta_miss": h_cosTheta_miss,
        "missingEnergy": h_missingEnergy,
        "missing_p": h_missing_p,
    }
    
    return histos

import ROOT

# Parámetros globales
intLumi        = 1.0
intLumiLabel   = "L = 3 ab^{-1}"
ana_tex        = '(VBF) e^{+}e^{-} #nu^{+}#nu^{-} H #rightarrow #b^{+}#b^{-}'
delphesVersion = '3.4.2'
energy         = 365.0
collider       = 'FCC-ee'
inputDir       = "outputs/FCCee/higgs/mva/plots_training/"
formats        = ['png', 'pdf']
outdir         = "outputs/FCCee/higgs/mva/plots/"
yaxis          = ['lin', 'log']
stacksig       = ['nostack']
plotStatUnc    = True

# Variables a plotear: se utilizan solo las versiones con corte (threshold)
variables = [
    'missing_p_threshold',
    'missingEnergy.energy_threshold',
    'jj_m_threshold',
    'cosTheta_miss_threshold',
    'score_threshold'
]
rebin = [1, 1]  # Rebinning uniforme por variable (opcional)

# Diccionario de selecciones: como ya aplicaste el corte final manualmente, 
# utilizamos una única selección representada por "score_threshold"
selections = {}
selections['Signal'] = ["score_threshold"]

# Etiquetas extra para la selección
extralabel = {}
extralabel['score_threshold'] = "MVA > 0.5"

# Definición de colores para cada análisis/muestra
colors = {}
colors['Signal'] = ROOT.kRed
colors['Background'] = ROOT.kBlue + 1

# Configuración de las muestras a plotear para cada análisis: 
# Aquí se definen las muestras señal y de fondo.
plots = {}
plots['ZH'] = {
    'signal': {'Signal': ['wzp6_ee_mumuH_ecm240']},
    'backgrounds': {'Background': ['p8_ee_WW_ecm240']}
}

# Leyendas para las muestras
legend = {}
legend['signal'] = 'Signal'
legend['background'] = 'Background'




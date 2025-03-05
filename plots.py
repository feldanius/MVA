import ROOT
import os

# Parámetros globales
intLumi        = 1.0
intLumiLabel   = "L = 3 ab^{-1}"
ana_tex        = '(VBF) e^{+}e^{-} #nu^{+}#nu^{-} H #rightarrow #b^{+}#b^{-}'
delphesVersion = '3.4.2'
energy         = 365.0
collider       = 'FCC-ee'
inputDir       = "outputs/FCCee/higgs/mva/plots_training/"
outdir         = "/eos/user/f/fdmartin/FCC365_MVA_BDT/Final_Plots/"
#outdir         = "outputs/FCCee/higgs/mva/plots/"

files_to_process = [
    "missing_p_threshold.png",
    "missingEnergy.energy_threshold.png",
    "jj_m_threshold.png",
    "cosTheta_miss_threshold.png",
    "score_threshold.png",
    "score.png"
]

if not os.path.exists(outdir):
    os.makedirs(outdir)

for file in files_to_process:
    file_path = os.path.join(inputDir, file)
    if not os.path.exists(file_path):
        print(f"Archivo {file_path} no existe, se salta.")
        continue

    c = ROOT.TCanvas("c", "c", 800, 600)

    img = ROOT.TImage.Open(file_path)
    if not img:
        print(f"No se pudo cargar la imagen {file_path}")
        continue

    img.Draw("X")  # "X" permite dibujar la imagen usando las coordenadas del canvas

    latex = ROOT.TLatex()
    latex.SetNDC()               
    latex.SetTextFont(42)
    latex.SetTextSize(0.04)
    latex.DrawLatex(0.15, 0.92, intLumiLabel)
    latex.DrawLatex(0.15, 0.87, ana_tex)

    c.Update()

    base, ext = os.path.splitext(file)
    out_file_name = os.path.join(outdir, f"{base}_final{ext}")
    c.SaveAs(out_file_name)
    c.Close()
    print(f"Guardado: {out_file_name}")

import xgboost as xgb
import ROOT

def convert_pkl_to_root(input_pkl, output_root):
    # Cargar el modelo XGBoost desde el archivo .pkl
    model = xgb.Booster()
    model.load_model(input_pkl)

    # Crear un archivo ROOT vacío
    root_file = ROOT.TFile(output_root, "RECREATE")

    # Crear un árbol (TTree) donde almacenaremos la información del modelo
    tree = ROOT.TTree("model_tree", "Modelo XGBoost")

    # Asegúrate de definir las ramas adecuadas según los datos que desees almacenar
    # Aquí solo te muestro cómo crear un ejemplo básico con el número de árboles
    num_trees = model.booster._Booster.attr('num_trees')  # Esto es solo un ejemplo
    tree.Branch("num_trees", ROOT.AddressOf(num_trees), "num_trees/I")

    # Aquí puedes agregar más ramas con más atributos del modelo si lo necesitas

    # Llenar el árbol con la información que quieras
    tree.Fill()

    # Escribir y cerrar el archivo ROOT
    root_file.Write()
    root_file.Close()

    print(f"Conversión completada: {output_root}")

# Llamar a la función
input_pkl = "outputs/FCCee/higgs/mva/test_2_pkl/bdt_model_example.pkl"
output_root = "outputs/FCCee/higgs/mva/test_2_pkl/bdt_model_example.root"
convert_pkl_to_root(input_pkl, output_root)





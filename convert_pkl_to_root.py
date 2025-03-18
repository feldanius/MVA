from addons.TMVAHelper.TMVAHelper import TMVAHelperXGB

input_pkl = "outputs/FCCee/higgs/mva/test_2_pkl/bdt_model_example.pkl"
output_root = "outputs/FCCee/higgs/mva/test_2_pkl/bdt_model_example.root"

# Instanciar la clase con los parámetros requeridos
model_name = "bdt_model_example"  # Este es el nombre que le asignas al modelo
helper = TMVAHelperXGB(model_input=input_pkl, model_name=model_name)

# Usar el método adecuado para realizar la conversión
helper.run_inference(input_pkl, output_root)

print(f"Conversión completada: {output_root}")



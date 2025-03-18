from addons.TMVAHelper.TMVAHelper import TMVAHelperXGB

input_pkl = "outputs/FCCee/higgs/mva/test_2_pkl/bdt_model_example.pkl"
output_root = "outputs/FCCee/higgs/mva/test_2_pkl/bdt_model_example.root"

TMVAHelperXGB.convert_model_to_ROOT(input_pkl, output_root)

print(f"Conversión completada: {output_root}")

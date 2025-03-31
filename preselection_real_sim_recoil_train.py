import os, copy
from addons.TMVAHelper.TMVAHelper import TMVAHelperXGB


# list of processes (mandatory)
processList = {
    'p8_ee_WW_ecm365': {'fraction': 0.3},
    'wzp6_ee_numunumuH_Hbb_ecm365': {'fraction': 0.3},
    'wzp6_ee_nuenueH_Hbb_ecm365':  {'fraction': 0.3},
    'p8_ee_ZZ_ecm365': {'fraction': 0.3},
    'p8_ee_tt_ecm365': {'fraction': 0.3},
}

# Production tag when running over EDM4Hep centrally produced events, this points to the yaml files for getting sample statistics (mandatory)
prodTag     = "FCCee/winter2023/IDEA/"

# Link to the dictonary that contains all the cross section informations etc... (mandatory)
procDict = "FCCee_procDict_winter2023_IDEA.json"

# Additional/custom C++ functions, defined in header files
includePaths = ["functions.h"]

# Output directory
#outputDir   = f"outputs/FCCee/higgs/mva/preselection_real/"
outputDir   = "/eos/user/f/fdmartin/FCC365_MVA_train_realsim_recoil/preselection"

# Multithreading: -1 means using all cores
nCPUS       = -1

# Batch settings
#runBatch    = False
#batchQueue  = "longlunch"
#compGroup = "group_u_FCC.local_gen"

doInference = False

## latest particle transformer model, trained on 9M jets in winter2023 samples
model_name = "fccee_flavtagging_edm4hep_wc_v1"

## model files needed for unit testing in CI
url_model_dir = "https://fccsw.web.cern.ch/fccsw/testsamples/jet_flavour_tagging/winter2023/wc_pt_13_01_2022/"
url_preproc = "{}/{}.json".format(url_model_dir, model_name)
url_model = "{}/{}.onnx".format(url_model_dir, model_name)

## model files locally stored on /eos
model_dir = (
    "/eos/experiment/fcc/ee/jet_flavour_tagging/winter2023/wc_pt_13_01_2022/"
)
local_preproc = "{}/{}.json".format(model_dir, model_name)
local_model = "{}/{}.onnx".format(model_dir, model_name)

## get local file, else download from url
def get_file_path(url, filename):
    if os.path.exists(filename):
        return os.path.abspath(filename)
    else:
        urllib.request.urlretrieve(url, os.path.basename(url))
        return os.path.basename(url)


weaver_preproc = get_file_path(url_preproc, local_preproc)
weaver_model = get_file_path(url_model, local_model)

from addons.ONNXRuntime.jetFlavourHelper import JetFlavourHelper
from addons.FastJet.jetClusteringHelper import (
    ExclusiveJetClusteringHelper,
)

jetFlavourHelper = None
jetClusteringHelper = None


class RDFanalysis:

    # encapsulate analysis logic, definitions and filters in the dataframe
    def analysers(df):

        df = df.Alias("Particle0", "Particle#0.index")
        df = df.Alias("Particle1", "Particle#1.index")
        df = df.Alias("MCRecoAssociations0", "MCRecoAssociations#0.index")
        df = df.Alias("MCRecoAssociations1", "MCRecoAssociations#1.index")
        df = df.Alias("Muon", "Muon#0.index")
        df = df.Alias("Electron", "Electron#0.index")

        # all leptons (bare)
        df = df.Define("muons_all", "FCCAnalyses::ReconstructedParticle::get(Muon, ReconstructedParticles)")
        df = df.Define("electrons_all", "FCCAnalyses::ReconstructedParticle::get(Electron, ReconstructedParticles)")

        # define good muons and electrons
        df = df.Define("muons", "FCCAnalyses::ReconstructedParticle::sel_p(20)(muons_all)")
        df = df.Define("electrons", "FCCAnalyses::ReconstructedParticle::sel_p(20)(electrons_all)")

        # electron veto
        df = df.Define("electrons_no", "FCCAnalyses::ReconstructedParticle::get_n(electrons)")
        df = df.Filter("electrons_no == 0")

        # muon veto
        df = df.Define("muons_no", "FCCAnalyses::ReconstructedParticle::get_n(muons)")
        df = df.Filter("muons_no == 0")

        # photon veto
        df = df.Alias("Photon0", "Photon#0.index")
        df = df.Define("photons_all", "FCCAnalyses::ReconstructedParticle::get(Photon0, ReconstructedParticles)")
        df = df.Define("photons", "FCCAnalyses::ReconstructedParticle::sel_p(40)(photons_all)")
        df = df.Define("photons_no", "FCCAnalyses::ReconstructedParticle::get_n(photons)")
        df = df.Filter("photons_no == 0")

      
###############################################################################################################################################
      # Eliminate particles that correspond to muons y electrons
        df = df.Define("ReconstructedParticlesNoMuons", "FCCAnalyses::ReconstructedParticle::remove(ReconstructedParticles, muons_all)")
        df = df.Define("ReconstructedParticlesNoLeptons", "FCCAnalyses::ReconstructedParticle::remove(ReconstructedParticlesNoMuons, electrons_all)")
        df = df.Define("ReconstructedParticlesNoLeptonsAndPhotons", "FCCAnalyses::ReconstructedParticle::remove(ReconstructedParticlesNoLeptons, photons_all)")

        
        # Clustering de jets usando partículas sin muones ni electrones
        global jetClusteringHelper
        global jetFlavourHelper
      
        collections = {
           "GenParticles": "Particle",
            "PFParticles": "ReconstructedParticles",
            "PFTracks": "EFlowTrack",
            "PFPhotons": "EFlowPhoton",
            "PFNeutralHadrons": "EFlowNeutralHadron",
            "TrackState": "EFlowTrack_1",
            "TrackerHits": "TrackerHits",
            "CalorimeterHits": "CalorimeterHits",
            "dNdx": "EFlowTrack_2",
            "PathLength": "EFlowTrack_L",
            "Bz": "magFieldBz",
        }

        collections_noleptons_and_photons = copy.deepcopy(collections)  
        collections_noleptons_and_photons["PFParticles"] = "ReconstructedParticlesNoLeptonsAndPhotons"

      
        jetClusteringHelper = ExclusiveJetClusteringHelper(collections_noleptons_and_photons["PFParticles"], 2)
        df = jetClusteringHelper.define(df)

        
        jetFlavourHelper = JetFlavourHelper(collections_noleptons_and_photons, jetClusteringHelper.jets, jetClusteringHelper.constituents)
        df = jetFlavourHelper.define(df)
        df = jetFlavourHelper.inference(weaver_preproc, weaver_model, df)

        df = df.Filter("event_njet == 2")    
        df = df.Define("jets_p4", "JetConstituentsUtils::compute_tlv_jets({})".format(jetClusteringHelper.jets))
        df = df.Define("jj_m", "JetConstituentsUtils::InvariantMass(jets_p4[0], jets_p4[1])")
      ###########################BTagging####################################
        df = df.Define("scoresum_B", "recojet_isB[0] + recojet_isB[1]")
        df = df.Filter("scoresum_B > 1.0")
        df = df.Define("bjets_mask", "scoresum_B > 1.0")
       # df = df.Define("bjets_mask", "recojet_isB > 0.7") 
        df = df.Define("bjets", "jets_p4[bjets_mask]")
        df = df.Filter("bjets.size() == 2", "two b-jets")

        
        df = df.Define("missingEnergy", "FCCAnalyses::missingEnergy(365., ReconstructedParticles)")
        df = df.Define("missingEnergy_energy", "FCCAnalyses::ReconstructedParticle::get_e({missingEnergy[0]})")
        df = df.Define("missingEnergy_energy_fixed", "(missingEnergy_energy.size() > 0) ? missingEnergy_energy[0] : 0.0")
        df = df.Define("cosTheta_miss", "FCCAnalyses::get_cosTheta_miss({missingEnergy[0]})")
        df = df.Define("missing_p", "FCCAnalyses::ReconstructedParticle::get_p({missingEnergy[0]})")
        df = df.Define("missing_p_fixed", "(missing_p.size() > 0) ? missing_p[0] : 0.0")
        df = df.Filter("cosTheta_miss < 0.98")
        df = df.Filter("jj_m > 95 && jj_m < 155")

      ###########################Recoil####################################
      
        df = df.Define("hbb", "ReconstructedParticle::resonanceBuilder(125)(bjets)")
        df = df.Define("hbb_m", "ReconstructedParticle::get_mass(hbb)[0]")
        df = df.Define("hbb_p", "ReconstructedParticle::get_p(hbb)[0]")
        df = df.Define("higgs_recoil", "ReconstructedParticle::recoilBuilder(365)(hbb)")
        df = df.Define("higgs_recoil_m", "ReconstructedParticle::get_mass(higgs_recoil)[0]")

        if doInference:
            tmva_helper = TMVAHelperXGB("/eos/user/f/fdmartin/FCC365_MVA_train_realsim/train/bdt_model_example.root", "bdt_model")

            #df = tmva_helper.run_inference(df, col_name="mva_score")
            df = df.Define("mva_score", "ROOT::VecOps::RVec<float>{0.5}")
            df = df.Define("mva_score_fixed", "(mva_score.size() > 0) ? mva_score[0] : 0.0")
            #df = df.Define("mva_score_fixed", "[](const ROOT::VecOps::RVec<float>& arr) { return arr.empty() ? 0.0f : arr[0]; }(mva_score)")

        return df

    def output():
        branchList = ["jj_m", "cosTheta_miss", "missingEnergy_energy_fixed", "missing_p_fixed"]
        if doInference:
            branchList.append("mva_score_fixed")
        return branchList

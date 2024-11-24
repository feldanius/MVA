#import sys
#sys.path.append("/afs/cern.ch/user/f/fdmartin/FCCAnalyses")
#from TMVAHelper import TMVAHelperXGB

from addons.TMVAHelper.TMVAHelper import TMVAHelperXGB


# list of processes (mandatory)
processList = {
    'p8_ee_WW_ecm355': {'fraction': 1},
    'wzp6_ee_nuenueH_Hbb_ecm240': {'fraction': 1},
    'wzp6_ee_numunumuH_Hbb_ecm240': {'fraction': 1},
    'p8_ee_ZZ_ecm240': {'fraction': 0.2},
    'p8_ee_tt_ecm365': {'fraction': 0.2},
}

# Production tag when running over EDM4Hep centrally produced events, this points to the yaml files for getting sample statistics (mandatory)
prodTag     = "FCCee/winter2023/IDEA/"

# Link to the dictonary that contains all the cross section informations etc... (mandatory)
procDict = "FCCee_procDict_winter2023_IDEA.json"

# Additional/custom C++ functions, defined in header files
includePaths = ["functions.h"]

# Output directory
outputDir   = f"outputs/FCCee/higgs/mva/preselection/"
#outputDir   = "/eos/user/f/fdmartin/FCC365_MVA_preselection"

# Multithreading: -1 means using all cores
nCPUS       = -1

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

# Batch settings
#runBatch    = False
#batchQueue  = "longlunch"
#compGroup = "group_u_FCC.local_gen"

doInference = False

class RDFanalysis():

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

        collections_noleptons = copy.deepcopy(collections)  
        collections_noleptons["PFParticles"] = "ReconstructedParticlesNoLeptons"

      
        jetClusteringHelper = ExclusiveJetClusteringHelper(collections_noleptons["PFParticles"], 2)
        df = jetClusteringHelper.define(df)

        
        jetFlavourHelper = JetFlavourHelper(collections_noleptons, jetClusteringHelper.jets, jetClusteringHelper.constituents)
        df = jetFlavourHelper.define(df)
        df = jetFlavourHelper.inference(weaver_preproc, weaver_model, df)

        df = df.Filter("event_njet >= 2")
       
        df = df.Define("jets_p4", "JetConstituentsUtils::compute_tlv_jets({})".format(jetClusteringHelper.jets))
        df = df.Define("jj_m", "JetConstituentsUtils::InvariantMass(jets_p4[0], jets_p4[1])")

#########################################################################################
        df = df.Define("scoresum_B", "recojet_isB[0] + recojet_isB[1]")  
        df = df.Filter("scoresum_B > 1.0") 
# Select two leading jets as b-jets candidates
        df = df.Define("bjets", "std::vector<ROOT::Math::PxPyPzEVector>{jets_p4[0], jets_p4[1]}")  
#########################################################################################
      
        # build Higgs resonance
        df = df.Define("higgs", "ReconstructedParticle::resonanceBuilder(125)(bjets)")
        df = df.Define("higgs_m", "ReconstructedParticle::get_mass(higgs)[0]")
        df = df.Define("higgs_p", "ReconstructedParticle::get_p(higgs)[0]")
        df = df.Define("higgs_recoil", "ReconstructedParticle::recoilBuilder(365)(higgs)")
        df = df.Define("higgs_recoil_m", "ReconstructedParticle::get_mass(higgs_recoil)[0]")

        # kinematic cuts
        df = df.Filter("higgs_m > 120 && higgs_m < 130")
        df = df.Filter("higgs_p > 10 && higgs_p < 100") 
        df = df.Filter("higgs_recoil_m < 10") 

        df = df.Define("missingEnergy", "FCCAnalyses::missingEnergy(365., ReconstructedParticles)")
        df = df.Define("cosTheta_miss", "FCCAnalyses::get_cosTheta_miss(missingEnergy)")
        df = df.Filter("cosTheta_miss < 0.98")

        #df = df.Define("acoplanarity", "FCCAnalyses::acoplanarity(muons)")
        #df = df.Define("acolinearity", "FCCAnalyses::acolinearity(muons)")


        if doInference:
            tmva_helper = TMVAHelperXGB("outputs/FCCee/higgs/mva/bdt_model_example.root", "bdt_model") # read the XGBoost training
            df = tmva_helper.run_inference(df, col_name="mva_score") # by default, makes a new column mva_score

        return df

    # define output branches to be saved
    def output():
        branchList = [ "higgs_p", "higgs_m", "higgs_recoil_m", "cosTheta_miss", "missingEnergy"]
        if doInference:
            branchList.append("mva_score")
        return branchList

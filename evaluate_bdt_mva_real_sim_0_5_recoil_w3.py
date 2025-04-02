import sys, os
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import sklearn
import pickle
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("-i", "--input", type=str, default="/eos/user/f/fdmartin/FCC365_MVA_train_realsim_recoil/train_w3/bdt_model_example.pkl", help="Input pkl file")
parser.add_argument("-o", "--outDir", type=str, default="/eos/user/f/fdmartin/FCC365_MVA_train_realsim_recoil/evaluate_plots_0_5_w3", help="Output directory")
args = parser.parse_args()


def plot_roc():
    train_probs = bdt.predict_proba(train_data)
    train_preds = train_probs[:, 1]
    train_fpr, train_tpr, _ = sklearn.metrics.roc_curve(train_labels, train_preds)
    train_roc_auc = sklearn.metrics.auc(train_fpr, train_tpr)

    test_probs = bdt.predict_proba(test_data)
    test_preds = test_probs[:, 1]
    test_fpr, test_tpr, _ = sklearn.metrics.roc_curve(test_labels, test_preds)
    test_roc_auc = sklearn.metrics.auc(test_fpr, test_tpr)

    plt.figure(figsize=(8, 6))
    plt.plot(train_fpr, train_tpr, color='blue', label=f"Training ROC (AUC = {train_roc_auc:.2f})")
    plt.plot(test_fpr, test_tpr, color='red', label=f"Testing ROC (AUC = {test_roc_auc:.2f})")
    plt.plot([0, 1], [0, 1], linestyle='--', color='gray', label='Random Guess')
    plt.xlabel('False Positive Rate')
    plt.ylabel('True Positive Rate')
    plt.title('Receiver Operating Characteristic (ROC) Curve')
    plt.legend()
    plt.grid()
    plt.savefig(f"{outDir}/roc.png")
    plt.savefig(f"{outDir}/roc.pdf")
    plt.close()


def plot_score():
    train_predictions = bdt.predict_proba(train_data)[:, 1]
    test_predictions = bdt.predict_proba(test_data)[:, 1]

    plt.figure(figsize=(8, 6))
    plt.hist(train_predictions[train_labels == 1], bins=50, range=(0, 1), histtype='step',
             label='Training Signal', color='blue', density=True)
    plt.hist(train_predictions[train_labels == 0], bins=50, range=(0, 1), histtype='step',
             label='Training Background', color='red', density=True)
    plt.hist(test_predictions[test_labels == 1], bins=50, range=(0, 1), histtype='step',
             label='Testing Signal', color='blue', linestyle='dashed', density=True)
    plt.hist(test_predictions[test_labels == 0], bins=50, range=(0, 1), histtype='step',
             label='Testing Background', color='red', linestyle='dashed', density=True)
    plt.xlabel('BDT Score')
    plt.ylabel('Number of Events (normalized)')
    plt.title('BDT Score Distribution')
    plt.legend()
    plt.grid()
    plt.savefig(f"{outDir}/score.png")
    plt.savefig(f"{outDir}/score.pdf")
    plt.close()


def plot_importance():
    fig, ax = plt.subplots(figsize=(12, 6))
    importance = bdt.get_booster().get_score(importance_type='weight')
    sorted_importance = sorted(importance.items(), key=lambda x: x[1], reverse=False)
    sorted_indices = [int(x[0][1:]) for x in sorted_importance]  # extrae los índices

    # Obtiene los nombres de las variables y sus importancias correspondientes
    sorted_vars = [variables[i] for i in sorted_indices]
    sorted_values = [x[1] for x in sorted_importance]

    importance_df = pd.DataFrame({'Variable': sorted_vars, 'Importance': sorted_values})
    importance_df.plot(kind='barh', x='Variable', y='Importance', legend=None, ax=ax)
    ax.set_xlabel('BDT score')
    ax.set_title("BDT variable scores", fontsize=16)
    plt.savefig(f"{outDir}/importance.png")
    plt.savefig(f"{outDir}/importance.pdf")
    plt.close()


def plot_score_threshold():
    train_predictions = bdt.predict_proba(train_data)[:, 1]
    test_predictions = bdt.predict_proba(test_data)[:, 1]

    plt.figure(figsize=(8, 6))
    plt.hist(train_predictions[(train_labels == 1) & (train_predictions > 0.5)], bins=50, range=(0.5, 1),
             histtype='step', label='Training Signal (>0.5)', color='blue', density=True)
    plt.hist(train_predictions[(train_labels == 0) & (train_predictions > 0.5)], bins=50, range=(0.5, 1),
             histtype='step', label='Training Background (>0.5)', color='red', density=True)
    plt.hist(test_predictions[(test_labels == 1) & (test_predictions > 0.5)], bins=50, range=(0.5, 1),
             histtype='step', label='Testing Signal (>0.5)', color='blue', linestyle='dashed', density=True)
    plt.hist(test_predictions[(test_labels == 0) & (test_predictions > 0.5)], bins=50, range=(0.5, 1),
             histtype='step', label='Testing Background (>0.5)', color='red', linestyle='dashed', density=True)
    plt.xlabel('BDT Score')
    plt.ylabel('Number of Events (normalized)')
    plt.title('BDT Score Distribution (Score > 0.5)')
    plt.legend()
    plt.grid()
    plt.savefig(f"{outDir}/score_threshold.png")
    plt.savefig(f"{outDir}/score_threshold.pdf")
    plt.close()


def plot_kinematics_threshold():
    # Lista de variables cinemáticas a graficar
    kinematics = ['jj_m', 'cosTheta_miss', 'missingEnergy_energy_fixed', 'missing_p_fixed', 'higgs_recoil_m', 'hbb_p', 'hbb_m']
    train_scores = bdt.predict_proba(train_data)[:, 1]
    test_scores = bdt.predict_proba(test_data)[:, 1]

    for var in kinematics:
        if var in variables:
            idx = variables.index(var)
            train_signal = train_data[(train_scores > 0.5) & (train_labels == 1), idx]
            train_background = train_data[(train_scores > 0.5) & (train_labels == 0), idx]
            test_signal = test_data[(test_scores > 0.5) & (test_labels == 1), idx]
            test_background = test_data[(test_scores > 0.5) & (test_labels == 0), idx]

            plt.figure(figsize=(8, 6))
            plt.hist(train_signal, bins=50, histtype='step', label='Training Signal (>0.5)', color='blue', density=True)
            plt.hist(train_background, bins=50, histtype='step', label='Training Background (>0.5)', color='red', density=True)
            plt.hist(test_signal, bins=50, histtype='step', label='Testing Signal (>0.5)', color='blue', linestyle='dashed', density=True)
            plt.hist(test_background, bins=50, histtype='step', label='Testing Background (>0.5)', color='red', linestyle='dashed', density=True)
            plt.xlabel(var)
            plt.ylabel('Number of Events (normalized)')
            plt.title(f'Histogram of {var} (BDT Score > 0.5)')
            plt.legend()
            plt.grid()
            plt.savefig(f"{outDir}/{var}_threshold.png")
            plt.savefig(f"{outDir}/{var}_threshold.pdf")
            plt.close()
        else:
            print(f"Warning: Variable '{var}' not found.")


if __name__ == "__main__":
    outDir = args.outDir

    res = pickle.load(open(args.input, "rb"))
    bdt = res['model']
    train_data = res['train_data']
    test_data = res['test_data']
    train_labels = res['train_labels']
    test_labels = res['test_labels']
    variables = res['variables']

    plot_importance()        
    plot_roc()               
    plot_score()             
    plot_score_threshold()   
    plot_kinematics_threshold()  

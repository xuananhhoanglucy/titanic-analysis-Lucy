import pandas as pd
import numpy as np
from scipy import stats
import matplotlib.pyplot as plt
import os
from datetime import datetime

#1.charger_donnees
chemin_fichier = r"C:\Users\Inspiron\Xuan Anh HOANG + Saad Larabi results projet\41_Titanic2.csv"
def charger_donnees(chemin_fichier):
    """Charge les données du Titanic depuis un fichier CSV"""
    if not chemin_fichier.lower().endswith('.csv'):
        raise ValueError("Le fichier doit être un CSV")
    if 'titanic' not in chemin_fichier.lower():
        raise ValueError("Le fichier doit contenir 'titanic' dans son nom")
    df = pd.read_csv(chemin_fichier, sep=';')
    colonnes_rename = {
        'survived': 'Survécu (1 = oui, 0 = non)',
        'pclass': 'Classe (1re, 2e, 3e)',
        'sex': 'Sexe',
        'age': 'Âge',
        'sibsp': 'Nombre de frères/sœurs ou conjoint(s) à bord',
        'parch': 'Nombre de parents ou enfants à bord',
        'fare': 'Tarif payé pour le billet',
        'embarked': 'Port d\'embarquement (C = Cherbourg, etc.)',
        'class': 'Classe (équivalent textuel de pclass)',
        'who': 'Catégorie (homme, femme, enfant)',
        'adult_male': 'Adulte masculin (booléen)',
        'deck': 'Pont de cabine (lettre)',
        'embark_town': 'Ville d\'embarquement',
        'alive': 'Statut de survie (vivant / décédé)',
        'alone': 'Était seul à bord (booléen)'
    }
    df = df.rename(columns=colonnes_rename)
    return df
    
#2.nettoyer_donnees
def nettoyer_donnees(df):
    """Nettoie les données en remplaçant les valeurs manquantes"""
    df_clean = df.copy()
    for col in df.select_dtypes(include=[np.number]):
        if df[col].isnull().sum() > 0:
            if col == 'Âge':
                df[col].fillna(df[col].mean(), inplace=True)
            elif col == 'Tarif payé pour le billet':
                df[col].fillna(df[col].max(), inplace=True)
            else:
                df[col].fillna(df[col].mode()[0], inplace=True)
    return df_clean

#3.statistiques_generales
def statistiques_generales(df):
    """Calcule et affiche les statistiques générales"""
    stats_dict = {}
    
    stats_desc = df.describe(include='all')
    stats_dict['Statistiques descriptives'] = stats_desc
    
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    for col in numeric_cols:
        stats_dict[f'Moyenne {col}'] = df[col].mean()
        stats_dict[f'Mode {col}'] = df[col].mode()[0]
        stats_dict[f'Max {col}'] = df[col].max()
        stats_dict[f'Min {col}'] = df[col].min()
        
    if 'Sexe' in df.columns:
        stats_dict['Nombre par sexe'] = df['Sexe'].value_counts()
        
    if 'Survécu (1 = oui, 0 = non)' in df.columns and 'Sexe' in df.columns:
        mortalite_sexe = df.groupby('Sexe')['Survécu (1 = oui, 0 = non)'].mean()
        stats_dict['Taux de mortalité par sexe'] = 1 - mortalite_sexe
    
    if all(col in df.columns for col in ['Survécu (1 = oui, 0 = non)', 'Classe (1re, 2e, 3e)', 'Sexe']):
        survie_classe_sexe = df.groupby(['Classe (1re, 2e, 3e)', 'Sexe'])['Survécu (1 = oui, 0 = non)'].mean()
        stats_dict['Taux de survie par classe et sexe'] = survie_classe_sexe
        
    if 'Âge' in df.columns:
        stats_dict['Nombre adultes'] = df[df['Âge'] >= 18].shape[0]
        stats_dict['Nombre enfants'] = df[df['Âge'] < 18].shape[0]
        
        if 'Survécu (1 = oui, 0 = non)' in df.columns:
            df_adultes = df[df['Âge'] >= 18]
            df_enfants = df[df['Âge'] < 18]
            stats_dict['Taux mortalité adultes'] = 1 - df_adultes['Survécu (1 = oui, 0 = non)'].mean()
            stats_dict['Taux mortalité enfants'] = 1 - df_enfants['Survécu (1 = oui, 0 = non)'].mean()
        
    for key, value in stats_dict.items():
        print(f"\n=== {key} ===")
        print(value)
    
    return stats_dict

#4.calculer corrélation(df, col1, col2)
def calculer_correlation(df, col1, col2):
    """Calcule la corrélation de Pearson entre deux colonnes"""
    if col1 not in df.columns or col2 not in df.columns:
        raise ValueError("Les colonnes spécifiées n'existent pas dans le DataFrame")
    if not (np.issubdtype(df[col1].dtype, np.number) and np.issubdtype(df[col2].dtype, np.number)):
        raise ValueError("Les colonnes doivent être numériques pour calculer la corrélation")
        
    correlation = df[[col1, col2]].corr().iloc[0, 1]
    print(f"Corrélation entre {col1} et {col2}: {correlation:.2f}")
    return correlation

#5.regression_lineaire(df, x_col, y_col)
def regression_lineaire(df, x_col, y_col):
    """Effectue une régression linéaire entre deux colonnes"""
    if x_col not in df.columns or y_col not in df.columns:
        raise ValueError("Les colonnes spécifiées n'existent pas dans le DataFrame")
        
    df_reg = df[[x_col, y_col]].dropna()
    if df_reg.empty:
        raise ValueError("Pas assez de données pour effectuer la régression")

    x = df_reg[x_col]
    y = df_reg[y_col]
    result = stats.linregress(x, y)
    print(f"Régression linéaire: y = {result.slope:.2f}x + {result.intercept:.2f}")
    print(f"Coefficient R: {result.rvalue:.2f}")
    print(f"Valeur p: {result.pvalue:.2e}")

    return result.slope, result.intercept, result.rvalue

#6.classes_age_tarif
def creer_classes_age_tarif(df):
    """Crée des classes d'âge et des tranches de tarif"""
    df_copy = df.copy()
    bins_age = [0, 12, 18, 60, 100]
    labels_age = ['Enfant(<12)', 'Adolescent(12-18)', 'Adulte(18-60)', 'Senior(>60)']
    if 'Âge' in df_copy.columns:
        df_copy = df_copy[df_copy['Âge'].notnull()]
        df_copy['Classe d\'âge'] = pd.cut(df_copy['Âge'], bins=bins_age, labels=labels_age, right=False)
    
    if 'Tarif payé pour le billet' in df_copy.columns:
        df_copy['Tranche tarif'] = pd.qcut(df_copy['Tarif payé pour le billet'], q=4, 
                                          labels=['Très bas', 'Bas', 'Élevé', 'Très élevé'])
    
    return df_copy

#7.survivants_par_ville_d'embarquement
def survivants_par_ville(df):
    """Calcule et affiche le nombre de survivants par ville d'embarquement"""
    if 'Ville d\'embarquement' not in df.columns or 'Survécu (1 = oui, 0 = non)' not in df.columns:
        raise ValueError("Colonnes nécessaires non trouvées")
        
    survivants_ville = df[df['Survécu (1 = oui, 0 = non)'] == 1]['Ville d\'embarquement'].value_counts()

    plt.figure(figsize=(8, 5))
    survivants_ville.plot(kind='bar', color='pink', edgecolor='black')
    plt.title("Nombre de survivants par ville d'embarquement")
    plt.xlabel("Ville")
    plt.ylabel("Nombre de survivants")
    plt.tight_layout()
    plt.show()
        
    os.makedirs("results", exist_ok=True)
    plt.savefig("results/survivants_par_ville.png")
    plt.close()

    result_df = pd.DataFrame({'Nombre de survivants': survivants_ville})
    print("\n=== Nombre de survivants par ville d'embarquement ===")
    print(result_df)
    return result_df

#8.generer_graphique
def generer_graphique(df, x_col, y_col, chemin_sortie):
    """Génère un nuage de points avec droite de régression"""
    if x_col not in df.columns or y_col not in df.columns:
        raise ValueError("Colonnes spécifiées non trouvées")
    
    df_plot = df[[x_col, y_col]].dropna()
    slope, intercept, rvalue = regression_lineaire(df, x_col, y_col)

    plt.figure(figsize=(8, 5))
    plt.scatter(df_plot[x_col], df_plot[y_col], alpha=0.5, label='Données')

    x_vals = np.array([df_plot[x_col].min(), df_plot[x_col].max()])
    y_vals = intercept + slope * x_vals
    plt.plot(x_vals, y_vals, color='red', label=f"Régression (R={rvalue:.2f})")
    
    plt.xlabel(x_col)
    plt.ylabel(y_col)
    plt.title(f"Nuages de points: {y_col} en fonction de {x_col}")
    plt.legend()
    plt.grid(True)

    results = r"C:\Users\Inspiron\Xuan Anh HOANG + Saad Larabi results projet\results"
    os.makedirs(results, exist_ok=True)
    chemin_sortie = os.path.join(results, "regression.png")
    
    plt.savefig(chemin_sortie)
    plt.close()
    print(f"Graphique sauvegardé à : {chemin_sortie}")
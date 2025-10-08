import pandas as pd
import os

print("="*60)
print("ETL PIPELINE - ASSOCIATIONS PARIS 12")
print("="*60)

# ====================
# 1. EXTRACT (Extraction)
# ====================
print("\n[EXTRACT] Chargement des données Paris (75)...")

fichier_paris = 'rna_import_20250901_dpt_75.csv'

if not os.path.exists(fichier_paris):
    print(f"ERREUR : {fichier_paris} introuvable !")
    input("Appuie sur Entrée...")
    exit()

# Charger le fichier Paris (ça peut prendre 1 minute)
print(f"Lecture de {fichier_paris} (50 MB)...")
print("Patience, ça peut prendre 1-2 minutes...")

df = pd.read_csv(
    fichier_paris,
    sep=';',
    encoding='utf-8',
    low_memory=False,
    on_bad_lines='skip'
)

print(f"✅ {len(df)} associations chargées (tout Paris)")
print(f"📊 {len(df.columns)} colonnes")

# ====================
# 2. TRANSFORM (Transformation)
# ====================
print("\n[TRANSFORM] Nettoyage et filtrage...")

# 2.1 - Filtrer Paris 12 (code postal 75012)
df['adrs_codepostal'] = df['adrs_codepostal'].astype(str)
df_paris12 = df[df['adrs_codepostal'] == '75012'].copy()

print(f"🎯 Associations Paris 12 : {len(df_paris12)}")

if len(df_paris12) == 0:
    print("Aucune association trouvée à Paris 12 !")
    input("Appuie sur Entrée...")
    exit()

# 2.2 - Supprimer les doublons
avant = len(df_paris12)
df_paris12 = df_paris12.drop_duplicates(subset=['id'])
apres = len(df_paris12)
print(f"🧹 Doublons supprimés : {avant - apres}")

# 2.3 - Supprimer les lignes avec ID vide
df_paris12 = df_paris12[df_paris12['id'].notna()]

# 2.4 - Nettoyer les espaces
colonnes_texte = ['titre', 'objet', 'libcom']
for col in colonnes_texte:
    if col in df_paris12.columns:
        df_paris12[col] = df_paris12[col].astype(str).str.strip()

# 2.5 - Sélectionner les colonnes importantes
colonnes_utiles = [
    'id',
    'titre',
    'objet',
    'date_creat',
    'date_publi',
    'adr1',
    'adr2',
    'adr3',
    'adrs_codepostal',
    'libcom',
    'siteweb'
]

colonnes_existantes = [col for col in colonnes_utiles if col in df_paris12.columns]
df_paris12_clean = df_paris12[colonnes_existantes].copy()

print(f"✅ Données nettoyées : {len(df_paris12_clean)} associations")

# ====================
# 3. LOAD (Sauvegarde)
# ====================
print("\n[LOAD] Sauvegarde des données...")

# Sauvegarder en CSV
df_paris12_clean.to_csv('associations_paris12_clean.csv', index=False, encoding='utf-8')
print("💾 associations_paris12_clean.csv")

# Créer un fichier sample pour GitHub (100 lignes)
df_sample = df_paris12_clean.head(100)
df_sample.to_csv('sample_data.csv', index=False, encoding='utf-8')
print("💾 sample_data.csv (pour GitHub)")

# ====================
# 4. ANALYSE
# ====================
print("\n[ANALYSE] Statistiques...")

print(f"\n📊 RÉSULTATS :")
print(f"  • Total associations Paris 12 : {len(df_paris12_clean)}")

# Compter les associations par objet social
if 'objet_social1' in df_paris12.columns:
    print(f"\n🏷️  Top 5 objets sociaux :")
    top_objets = df_paris12['objet_social1'].value_counts().head(5)
    for obj, count in top_objets.items():
        if pd.notna(obj):
            print(f"  • {obj[:40]}: {count}")

# Associations avec site web
if 'siteweb' in df_paris12_clean.columns:
    avec_site = df_paris12_clean['siteweb'].notna().sum()
    pourcentage = (avec_site / len(df_paris12_clean)) * 100
    print(f"\n🌐 Associations avec site web : {avec_site} ({pourcentage:.1f}%)")

# Créer un fichier texte avec les stats
with open('stats_paris12.txt', 'w', encoding='utf-8') as f:
    f.write("STATISTIQUES - ASSOCIATIONS PARIS 12\n")
    f.write("="*50 + "\n\n")
    f.write(f"Total associations : {len(df_paris12_clean)}\n")
    f.write(f"Associations avec site web : {avec_site} ({pourcentage:.1f}%)\n")
    f.write(f"\nDonnées extraites le : 01/09/2025\n")
    f.write(f"Source : RNA - data.gouv.fr\n")

print("💾 stats_paris12.txt")

# Afficher quelques exemples
print(f"\n📋 Exemples d'associations :")
if 'titre' in df_paris12_clean.columns:
    for i, titre in enumerate(df_paris12_clean['titre'].head(5), 1):
        print(f"  {i}. {titre}")

print("\n" + "="*60)
print("✅ ETL TERMINÉ AVEC SUCCÈS !")
print("="*60)
print("\nFichiers créés :")
print("  • associations_paris12_clean.csv (données complètes)")
print("  • sample_data.csv (échantillon pour GitHub)")
print("  • stats_paris12.txt (statistiques)")
print("\n🚀 Prochaine étape : Push sur GitHub !")

input("\nAppuie sur ENTREE...")
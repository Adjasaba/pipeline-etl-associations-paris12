import os
import pandas as pd

print("="*50)
print("ANALYSE RNA - ASSOCIATIONS FRANCAISES")
print("="*50)

# 1. Lister les fichiers
print("\n[1/5] Verification des fichiers...")
fichiers = os.listdir('.')
print(f"Fichiers trouves : {len(fichiers)}")

for f in fichiers:
    if f.endswith('.csv') or f.endswith('.zip'):
        taille = os.path.getsize(f) / (1024*1024)
        print(f"  - {f} ({taille:.1f} MB)")

# 2. Chercher les CSV
fichiers_csv = [f for f in fichiers if f.endswith('.csv')]
print(f"\n[2/5] Fichiers CSV trouves : {len(fichiers_csv)}")

if len(fichiers_csv) == 0:
    print("\n*** ATTENTION ***")
    print("Aucun fichier CSV trouve !")
    print("1. Telecharge le ZIP depuis data.gouv.fr")
    print("2. Extrais-le dans ce dossier")
    print("3. Relance ce script")
    input("\nAppuie sur Entree pour fermer...")
    exit()

# 3. Lire le premier CSV
fichier = fichiers_csv[0]
print(f"\n[3/5] Lecture de {fichier}...")
print("(ca peut prendre 30 secondes...)")

try:
    df = pd.read_csv(
        fichier,
        nrows=5000,  # Seulement 5000 lignes pour commencer
        sep=';',
        encoding='utf-8',
        on_bad_lines='skip',
        low_memory=False
    )
    
    print(f"OK ! {len(df)} lignes chargees")
    print(f"Colonnes : {len(df.columns)}")
    
except Exception as e:
    print(f"ERREUR : {e}")
    print("\nEssaye de changer encoding='utf-8' en encoding='latin-1'")
    input("\nAppuie sur Entree...")
    exit()

# 4. Afficher les colonnes
print(f"\n[4/5] Colonnes disponibles :")
for i, col in enumerate(df.columns, 1):
    print(f"  {i:2d}. {col}")

# 5. Chercher Paris 12
print(f"\n[5/5] Recherche Paris 12...")

# Trouver la colonne code postal
col_cp = None
for col in df.columns:
    if 'postal' in col.lower() or 'cp' in col.lower() or 'code_post' in col.lower():
        col_cp = col
        break

if col_cp:
    print(f"Colonne code postal : {col_cp}")
    df[col_cp] = df[col_cp].astype(str)
    paris12 = df[df[col_cp].str.startswith('75012')]
    print(f"Associations Paris 12 : {len(paris12)}")
    
    if len(paris12) > 0:
        paris12.to_csv('paris12_extrait.csv', index=False)
        print("Sauvegarde dans : paris12_extrait.csv")
else:
    print("Colonne code postal non trouvee")

print("\n" + "="*50)
print("TERMINÉ !")
print("="*50)
input("\nAppuie sur ENTREE pour fermer...")

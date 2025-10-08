import pandas as pd
import matplotlib.pyplot as plt

print("📊 Création des visualisations...")

# Charger les données
df = pd.read_csv('associations_paris12_clean.csv')

print(f"Données chargées : {len(df)} associations")

# ============================================
# GRAPHIQUE 1 : Associations créées par année
# ============================================
if 'date_creat' in df.columns:
    print("\n[1/3] Graphique : Évolution créations...")
    
    # Extraire l'année
    df['annee'] = pd.to_datetime(df['date_creat'], errors='coerce').dt.year
    
    # Filtrer années valides (après 1900)
    df_annee = df[df['annee'] > 1900]
    
    # Compter par année
    creations_par_annee = df_annee['annee'].value_counts().sort_index()
    
    # Créer le graphique
    plt.figure(figsize=(12, 6))
    plt.plot(creations_par_annee.index, creations_par_annee.values, 
             linewidth=2, color='#2E86AB')
    plt.fill_between(creations_par_annee.index, creations_par_annee.values, 
                     alpha=0.3, color='#2E86AB')
    plt.title('Évolution des créations d\'associations à Paris 12', 
              fontsize=14, fontweight='bold')
    plt.xlabel('Année', fontsize=12)
    plt.ylabel('Nombre de créations', fontsize=12)
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig('graphique_evolution.png', dpi=300, bbox_inches='tight')
    print("  ✅ graphique_evolution.png")
    plt.close()

# ============================================
# GRAPHIQUE 2 : Top 10 rues avec le plus d'associations
# ============================================
if 'adr1' in df.columns:
    print("\n[2/3] Graphique : Top rues...")
    
    # Nettoyer les adresses
    df['adr1_clean'] = df['adr1'].fillna('').astype(str).str.upper().str.strip()
    
    # Compter par rue (exclure vides)
    top_rues = df[df['adr1_clean'] != '']['adr1_clean'].value_counts().head(10)
    
    # Créer le graphique
    plt.figure(figsize=(12, 6))
    top_rues.plot(kind='barh', color='#A23B72')
    plt.title('Top 10 des rues avec le plus d\'associations (Paris 12)', 
              fontsize=14, fontweight='bold')
    plt.xlabel('Nombre d\'associations', fontsize=12)
    plt.ylabel('Rue', fontsize=12)
    plt.tight_layout()
    plt.savefig('graphique_rues.png', dpi=300, bbox_inches='tight')
    print("  ✅ graphique_rues.png")
    plt.close()

# ============================================
# GRAPHIQUE 3 : Statistiques globales (infographie)
# ============================================
print("\n[3/3] Infographie statistiques...")

stats = {
    'Total associations': len(df),
    'Avec site web': df['siteweb'].notna().sum() if 'siteweb' in df.columns else 0,
    'Avec adresse complète': df['adr1'].notna().sum() if 'adr1' in df.columns else 0
}

fig, ax = plt.subplots(figsize=(10, 6))
ax.axis('off')

# Titre
ax.text(0.5, 0.9, 'ASSOCIATIONS PARIS 12', 
        ha='center', fontsize=20, fontweight='bold')
ax.text(0.5, 0.82, 'Statistiques clés', 
        ha='center', fontsize=14, style='italic', color='gray')

# Statistiques
y_pos = 0.65
for label, value in stats.items():
    pourcentage = (value / len(df) * 100) if len(df) > 0 else 0
    
    # Valeur
    ax.text(0.5, y_pos, f'{value:,}', 
            ha='center', fontsize=32, fontweight='bold', color='#2E86AB')
    
    # Label
    ax.text(0.5, y_pos - 0.08, label, 
            ha='center', fontsize=12, color='gray')
    
    # Pourcentage (sauf pour le total)
    if label != 'Total associations':
        ax.text(0.5, y_pos - 0.12, f'({pourcentage:.1f}%)', 
                ha='center', fontsize=10, color='gray', style='italic')
    
    y_pos -= 0.22

# Source
ax.text(0.5, 0.05, 'Source : RNA - data.gouv.fr (Sept 2025)', 
        ha='center', fontsize=9, color='gray', style='italic')

plt.tight_layout()
plt.savefig('infographie_stats.png', dpi=300, bbox_inches='tight', 
            facecolor='white')
print("  ✅ infographie_stats.png")
plt.close()

print("\n✅ VISUALISATIONS CRÉÉES !")
print("\nFichiers générés :")
print("  • graphique_evolution.png")
print("  • graphique_rues.png")
print("  • infographie_stats.png")

input("\nAppuie sur ENTREE...")
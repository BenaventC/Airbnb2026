# Split de p10_cognition_affect_detection.ipynb

## Structure du découpage

Le notebook original `p10_cognition_affect_detection.ipynb` a été divisé en **deux scripts** pour une meilleure modularité :

### **p10a_cognition_affect_detection_part_a.ipynb** (Extraction)
**Sections 1-6 : Préparation et extraction des scores**

1. Introduction & Pipeline Overview
2. Imports and Constants
3. Data Loading and Preparation
4. Prompt Templates and Model Selection
5. Extraction (applique les modèles Gemma3 et Mistral aux reviews)
6. Data Export (sauvegarde les résultats)

**Outputs :**
- `data/results_p10_cognition_affect_per_review.csv`
- `data/results_p10_cognition_affect_pivot.csv`

---

### **p10b_cognition_affect_detection_part_b.ipynb** (Analyses)
**Sections 7-10 : Analyses statistiques et visualisations**

7. Analyses
   - 7.1 Distribution Analysis
   - 7.2 Cognition vs Affectivity Scatter Plot
   - 7.3 Language and Neighbourhood Analysis
   - 7.4 PCA Correlation Circle

8. Categorical Factor Analysis (ANOVA)

9. Advanced Multivariate Analysis (MTMM Matrix)

10. Runtime and Carbon Emissions Report

**Inputs :**
- Lit `results_p10_cognition_affect_per_review.csv` généré par **part_a**

**Outputs :**
- Visualisations PNG/JPEG dans `Images/`
- Rapport carbone appendu à `data/carbon_emissions_report.csv`

---

## Workflow d'exécution

1. **Exécuter d'abord : `p10a_cognition_affect_detection_part_a.ipynb`**
   - Préparation, extraction LLM, export CSV
   - Durée : ~1-2h (dépend du nb de reviews et modèles)

2. **Puis exécuter : `p10b_cognition_affect_detection_part_b.ipynb`**
   - Analyses, visualisations, rapports carbone
   - Lit automatiquement les résultats de part_a

---

## Notes importantes

- **Traçabilité IDs** : Les colonnes ID sont conservées dans tous les exports (conforme conventions projet)
- **Indépendance** : Part_b peut être ré-exécutée plusieurs fois sans relancer part_a (tant que le CSV existe)
- **Chemins** : Tous les imports/exports utilisent les chemins relatifs `data/` et `Images/`

---

## Anciennes versions

L'original `p10_cognition_affect_detection.ipynb` reste disponible pour référence historique.

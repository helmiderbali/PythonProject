# 📈 Analyse des Taux de Change EUR/USD

Application Streamlit pour l'analyse des taux de change EUR/USD sur les 2 dernières années.

## Fonctionnalités

Implémentation complète :

### 1️⃣ Téléchargement des données
- ✅ Téléchargement automatique des taux EUR/USD via APIs (ExchangeRate-API, Currency-API, FreeForexAPI)
- ✅ Sauvegarde dans le fichier `eur_usd.csv`
- ✅ Données sur les 2 dernières années

### 2️⃣ Chargement et préparation
- ✅ Chargement avec pandas dans un DataFrame
- ✅ Conversion de la colonne date en index temporel trié
- ✅ Traitement des jours manquants (week-ends/jours fériés) par propagation vers l'avant

### 3️⃣ Analyse exploratoire
- ✅ Calcul du rendement journalier : `(Prix_t - Prix_{t-1}) / Prix_{t-1} * 100`
- ✅ Statistiques descriptives : moyenne, écart-type, min, max
- ✅ Graphiques interactifs des taux et rendements

### 4️⃣ Prévision naïve
- ✅ Implémentation : valeur de demain = valeur d'aujourd'hui
- ✅ Calcul de l'erreur quadratique moyenne (RMSE)
- ✅ Comparaison visuelle réel vs prévision
- ✅ Analyse des erreurs de prévision

## Installation

**Prérequis:** Python 3.8+

```bash
# 1. Installer les dépendances
pip install -r requirements.txt

# 2. Lancer l'application
streamlit run eur_usd_analysis.py

# 3. Ouvrir http://localhost:8501
```

## Structure

```
PythonProject/
├── eur_usd_analysis.py    # Interface Streamlit
├── data_service.py        # Gestion des données
├── analysis_service.py    # Analyses statistiques
├── test_*.py             # Tests unitaires
├── data_service_core.py   # Version sans Streamlit pour tests
├── requirements.txt       # Dépendances
└── eur_usd.csv           # Données (généré automatiquement)
```

## Tests

```bash
# Lancer les tests unitaires
python -m pytest test_*.py -v

# Ou avec unittest
python -m unittest test_analysis.py
python -m unittest test_data_service.py
```

## Détails Techniques

**APIs utilisées:**
- ExchangeRate-API, Currency API, FreeForexAPI
- Fallback sur données générées si APIs indisponibles

**Architecture:**
- Séparation domaine/UI
- Services modulaires
- Tests unitaires complets

**Dépendances:**
streamlit, pandas, numpy, requests, plotly, scikit-learn, pytest

## Utilisation

1. Lancer avec `streamlit run eur_usd_analysis.py`
2. Aller sur http://localhost:8501
3. L'interface affiche automatiquement :
   - Téléchargement et aperçu des données
   - Analyse exploratoire avec rendements
   - Prévision naïve et métriques d'erreur

## Résultats

- Fichier `eur_usd.csv` généré automatiquement
- Graphiques interactifs des taux et rendements
- Statistiques descriptives complètes
- Métriques RMSE et analyse d'erreurs
- Export CSV des données analysées

import unittest
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from unittest.mock import patch, MagicMock
import os
import tempfile

from data_service_core import DataServiceCore

class TestDataService(unittest.TestCase):
    """Tests unitaires pour le service de données"""
    
    def setUp(self):
        """Prépare l'environnement de test"""
        self.temp_csv = tempfile.NamedTemporaryFile(delete=False, suffix='.csv')
        self.temp_csv.close()
    
    def tearDown(self):
        """Nettoie après les tests"""
        if os.path.exists(self.temp_csv.name):
            os.unlink(self.temp_csv.name)
    
    def test_generer_historique_depuis_taux_actuel(self):
        """Test de la génération d'historique depuis un taux actuel"""
        taux_actuel = 1.0850
        date_debut = datetime(2023, 1, 1)
        date_fin = datetime(2023, 1, 31)
        
        df = DataServiceCore._generer_historique_depuis_taux_actuel(taux_actuel, date_debut, date_fin)
        
        # Vérifie que le DataFrame n'est pas vide
        self.assertGreater(len(df), 0)
        
        # Vérifie que la colonne EUR_USD existe
        self.assertIn('EUR_USD', df.columns)
        
        # Vérifie que le dernier taux est dans une plage raisonnable du taux actuel
        # (la fonction ajoute tendance et saisonnalité, donc test plus flexible)
        self.assertGreater(df['EUR_USD'].iloc[-1], taux_actuel * 0.9)
        self.assertLess(df['EUR_USD'].iloc[-1], taux_actuel * 1.1)
        
        # Vérifie que l'index est datetime
        self.assertIsInstance(df.index, pd.DatetimeIndex)
        
        # Vérifie qu'il n'y a pas de week-ends
        weekdays = df.index.dayofweek
        self.assertTrue(all(day < 5 for day in weekdays))
    
    def test_generer_donnees_exemple(self):
        """Test de la génération de données d'exemple"""
        df = DataServiceCore._generer_donnees_exemple()
        
        # Vérifie que le DataFrame n'est pas vide
        self.assertGreater(len(df), 0)
        
        # Vérifie que la colonne EUR_USD existe
        self.assertIn('EUR_USD', df.columns)
        
        # Vérifie que les taux sont dans une plage réaliste
        self.assertTrue(all(0.8 < rate < 1.5 for rate in df['EUR_USD']))
        
        # Vérifie que l'index est datetime
        self.assertIsInstance(df.index, pd.DatetimeIndex)
        
        # Vérifie qu'il n'y a pas de week-ends
        weekdays = df.index.dayofweek
        self.assertTrue(all(day < 5 for day in weekdays))
    
    @patch('data_service_core.os.path.exists')
    @patch('data_service_core.pd.read_csv')
    def test_charger_donnees_depuis_csv_existant(self, mock_read_csv, mock_exists):
        """Test du chargement depuis un CSV existant"""
        # Prépare des données de test
        mock_exists.return_value = True
        dates = pd.date_range(start='2023-01-01', end='2023-01-10', freq='D')
        test_data = pd.DataFrame({'EUR_USD': [1.1] * len(dates)}, index=dates)
        mock_read_csv.return_value = test_data
        
        df = DataServiceCore.charger_et_preparer_donnees()
        
        # Vérifie que read_csv a été appelé
        mock_read_csv.assert_called_once()
        
        # Vérifie que les données sont retournées
        self.assertIsNotNone(df)
        self.assertIn('EUR_USD', df.columns)
    
    def test_donnees_coherence_temporelle(self):
        """Test de la cohérence temporelle des données générées"""
        df = DataServiceCore._generer_donnees_exemple()
        
        # Vérifie que les dates sont triées
        self.assertTrue(df.index.is_monotonic_increasing)
        
        # Vérifie que la plage de dates couvre environ 2 ans
        duree = df.index.max() - df.index.min()
        self.assertGreater(duree.days, 600)  # Au moins 600 jours
        self.assertLess(duree.days, 800)     # Moins de 800 jours
    
    def test_gestion_valeurs_manquantes(self):
        """Test de la gestion des valeurs manquantes"""
        # Crée des données avec des NaN
        dates = pd.date_range(start='2023-01-01', end='2023-01-10', freq='D')
        rates = [1.1, np.nan, 1.12, 1.13, np.nan, 1.15, 1.16, 1.17, np.nan, 1.19]
        df_with_nan = pd.DataFrame({'EUR_USD': rates}, index=dates)
        
        # Sauvegarde temporairement
        df_with_nan.to_csv(self.temp_csv.name)
        
        # Patch pour utiliser notre fichier temporaire
        with patch('data_service_core.os.path.exists', return_value=True), \
             patch('data_service_core.pd.read_csv', return_value=df_with_nan):
            
            df_clean = DataServiceCore.charger_et_preparer_donnees()
            
            # Vérifie qu'il n'y a plus de NaN
            self.assertFalse(df_clean['EUR_USD'].isna().any())

if __name__ == '__main__':
    unittest.main()
import unittest
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from analysis_service import AnalysisService

class TestAnalysisService(unittest.TestCase):
    """Tests unitaires pour le service d'analyse"""
    
    def setUp(self):
        """Prépare des données de test"""
        dates = pd.date_range(start='2023-01-01', end='2023-01-10', freq='D')
        rates = [1.1000, 1.1050, 1.1020, 1.1080, 1.1030, 1.1090, 1.1040, 1.1100, 1.1060, 1.1110]
        self.df = pd.DataFrame({'EUR_USD': rates}, index=dates)
    
    def test_calculer_rendements_journaliers(self):
        """Test du calcul des rendements journaliers"""
        df_with_returns = AnalysisService.calculer_rendements_journaliers(self.df)
        
        # Vérifie que la colonne a été ajoutée
        self.assertIn('Rendement_Journalier', df_with_returns.columns)
        
        # Vérifie le premier rendement (doit être NaN)
        self.assertTrue(pd.isna(df_with_returns['Rendement_Journalier'].iloc[0]))
        
        # Vérifie un calcul de rendement
        expected_return = (1.1050 - 1.1000) / 1.1000 * 100
        actual_return = df_with_returns['Rendement_Journalier'].iloc[1]
        self.assertAlmostEqual(actual_return, expected_return, places=4)
    
    def test_calculer_statistiques_descriptives(self):
        """Test du calcul des statistiques descriptives"""
        df_with_returns = AnalysisService.calculer_rendements_journaliers(self.df)
        stats = AnalysisService.calculer_statistiques_descriptives(df_with_returns)
        
        # Vérifie les clés attendues
        expected_keys = ['Moyenne', 'Ecart_Type', 'Min', 'Max', 'Moyenne_Rendement', 'Ecart_Type_Rendement']
        for key in expected_keys:
            self.assertIn(key, stats)
        
        # Vérifie quelques valeurs
        self.assertAlmostEqual(stats['Min'], 1.1000, places=4)
        self.assertAlmostEqual(stats['Max'], 1.1110, places=4)
        self.assertAlmostEqual(stats['Moyenne'], np.mean(self.df['EUR_USD']), places=4)
    
    def test_prevision_naive(self):
        """Test de la prévision naïve"""
        df_prevision, rmse = AnalysisService.prevision_naive(self.df)
        
        # Vérifie que la colonne de prévision a été ajoutée
        self.assertIn('Prevision_Naive', df_prevision.columns)
        
        # Vérifie que RMSE est un nombre positif
        self.assertIsInstance(rmse, float)
        self.assertGreater(rmse, 0)
        
        # Vérifie le principe de la prévision naïve (valeur précédente)
        # Après dropna(), l'index 0 de df_prevision correspond à l'index 1 de df original
        self.assertEqual(df_prevision['Prevision_Naive'].iloc[0], self.df['EUR_USD'].iloc[0])
    
    def test_calculer_erreurs_prevision(self):
        """Test du calcul des erreurs de prévision"""
        df_prevision, _ = AnalysisService.prevision_naive(self.df)
        metriques = AnalysisService.calculer_erreurs_prevision(df_prevision)
        
        # Vérifie les clés attendues
        expected_keys = ['Erreur_Absolue_Moyenne', 'Erreur_Moyenne', 'Erreurs']
        for key in expected_keys:
            self.assertIn(key, metriques)
        
        # Vérifie que les erreurs sont des nombres
        self.assertIsInstance(metriques['Erreur_Absolue_Moyenne'], float)
        self.assertIsInstance(metriques['Erreur_Moyenne'], float)
        
        # Vérifie que l'erreur absolue moyenne est positive
        self.assertGreaterEqual(metriques['Erreur_Absolue_Moyenne'], 0)

if __name__ == '__main__':
    unittest.main()
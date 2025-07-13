import pandas as pd
import numpy as np
from sklearn.metrics import mean_squared_error

class AnalysisService:
    """Service pour les analyses statistiques et prévisionnelles des taux de change"""
    
    @staticmethod
    def calculer_rendements_journaliers(df):
        """Calcule les rendements journaliers en pourcentage"""
        df_copy = df.copy()
        df_copy['Rendement_Journalier'] = df_copy['EUR_USD'].pct_change() * 100
        return df_copy

    @staticmethod
    def calculer_statistiques_descriptives(df):
        """Calcule les statistiques descriptives"""
        stats = {
            'Moyenne': df['EUR_USD'].mean(),
            'Ecart_Type': df['EUR_USD'].std(),
            'Min': df['EUR_USD'].min(),
            'Max': df['EUR_USD'].max(),
            'Moyenne_Rendement': df['Rendement_Journalier'].mean() if 'Rendement_Journalier' in df.columns else 0,
            'Ecart_Type_Rendement': df['Rendement_Journalier'].std() if 'Rendement_Journalier' in df.columns else 0
        }
        return stats

    @staticmethod
    def prevision_naive(df):
        """Implémente la prévision naïve où la valeur de demain égale celle d'aujourd'hui"""
        df_copy = df.copy()
        df_copy['Prevision_Naive'] = df_copy['EUR_USD'].shift(1)
        
        # Supprime la première ligne car elle aura NaN pour la prévision
        df_prevision = df_copy.dropna()
        
        # Calcule l'erreur quadratique moyenne (RMSE)
        rmse = np.sqrt(mean_squared_error(df_prevision['EUR_USD'], df_prevision['Prevision_Naive']))
        
        return df_prevision, rmse

    @staticmethod
    def calculer_erreurs_prevision(df_prevision):
        """Calcule les métriques d'erreur de prévision"""
        erreurs = df_prevision['EUR_USD'] - df_prevision['Prevision_Naive']
        
        metriques = {
            'Erreur_Absolue_Moyenne': np.abs(erreurs).mean(),
            'Erreur_Moyenne': erreurs.mean(),
            'Erreurs': erreurs
        }
        
        return metriques
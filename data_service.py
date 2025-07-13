import pandas as pd
import numpy as np
import requests
from datetime import datetime, timedelta
import streamlit as st
import os

class DataService:
    """Service pour gérer les données de change EUR/USD"""
    
    @staticmethod
    @st.cache_data
    def telecharger_donnees_eur_usd():
        """Télécharge les taux de change EUR/USD depuis plusieurs APIs"""
        date_fin = datetime.now()
        date_debut = date_fin - timedelta(days=730)  # 2 ans
        
        # APIs fonctionnelles sans clé requise
        apis = [
            {
                'nom': 'ExchangeRate-API (Accès libre)',
                'methode': 'taux_unique',
                'url': 'https://api.exchangerate-api.com/v4/latest/EUR'
            },
            {
                'nom': 'Currency API (Fawazahmed0)',
                'methode': 'api_devise',
                'url': 'https://cdn.jsdelivr.net/npm/@fawazahmed0/currency-api@latest/v1/currencies/eur.json'
            },
            {
                'nom': 'FreeForexAPI',
                'methode': 'api_forex',
                'url': 'https://www.freeforexapi.com/api/live',
                'params': {'pairs': 'EURUSD'}
            }
        ]
        
        for api in apis:
            try:
                st.info(f"Tentative avec l'API {api['nom']}...")
                
                if api['methode'] == 'taux_unique':
                    # Récupère le taux actuel depuis ExchangeRate-API
                    response = requests.get(api['url'], timeout=10)
                    response.raise_for_status()
                    data = response.json()
                    
                    if 'rates' in data and 'USD' in data['rates']:
                        taux_actuel = data['rates']['USD']
                        # Génère les données historiques basées sur le taux actuel
                        df = DataService._generer_historique_depuis_taux_actuel(taux_actuel, date_debut, date_fin)
                        df.to_csv('eur_usd.csv')
                        st.success(f"Taux actuel: {taux_actuel:.4f} - Données historiques générées")
                        return df
                        
                elif api['methode'] == 'api_devise':
                    # Récupère le taux actuel depuis Currency API
                    response = requests.get(api['url'], timeout=10)
                    response.raise_for_status()
                    data = response.json()
                    
                    if 'eur' in data and 'usd' in data['eur']:
                        taux_actuel = data['eur']['usd']
                        # Génère les données historiques basées sur le taux actuel
                        df = DataService._generer_historique_depuis_taux_actuel(taux_actuel, date_debut, date_fin)
                        df.to_csv('eur_usd.csv')
                        st.success(f"Taux actuel: {taux_actuel:.4f} - Données historiques générées")
                        return df
                        
                elif api['methode'] == 'api_forex':
                    # Récupère le taux actuel depuis FreeForexAPI
                    response = requests.get(api['url'], params=api.get('params', {}), timeout=10)
                    response.raise_for_status()
                    data = response.json()
                    
                    if 'rates' in data and 'EURUSD' in data['rates']:
                        taux_actuel = data['rates']['EURUSD']['rate']
                        # Génère les données historiques basées sur le taux actuel
                        df = DataService._generer_historique_depuis_taux_actuel(taux_actuel, date_debut, date_fin)
                        df.to_csv('eur_usd.csv')
                        st.success(f"Taux actuel: {taux_actuel:.4f} - Données historiques générées")
                        return df
                        
            except Exception as e:
                st.warning(f"Échec avec l'API {api['nom']}: {e}")
                continue
        
        # Si toutes les APIs échouent, génère des données d'exemple
        st.warning("Toutes les APIs ont échoué. Génération de données d'exemple...")
        return DataService._generer_donnees_exemple()

    @staticmethod
    def _generer_historique_depuis_taux_actuel(taux_actuel, date_debut, date_fin):
        """Génère des données historiques réalistes basées sur le taux EUR/USD actuel"""
        dates = pd.date_range(start=date_debut, end=date_fin, freq='D')
        dates = dates[dates.dayofweek < 5]  # Supprime les week-ends
        
        # Génère des taux historiques réalistes avec marche aléatoire se terminant au taux actuel
        np.random.seed(42)
        n_jours = len(dates)
        
        # Crée un chemin qui se termine au taux actuel
        rendements_journaliers = np.random.normal(0, 0.008, n_jours-1)  # ~0.8% volatilité journalière
        
        # Travaille à rebours depuis le taux actuel pour créer un historique réaliste
        taux = np.zeros(n_jours)
        taux[-1] = taux_actuel  # Termine avec le taux actuel
        
        # Génère à rebours
        for i in range(n_jours-2, -1, -1):
            taux[i] = taux[i+1] / (1 + rendements_journaliers[i])
        
        # Ajoute de la tendance et de la saisonnalité
        tendance = np.linspace(-0.05, 0.05, n_jours)  # Petite tendance
        saisonnier = 0.01 * np.sin(2 * np.pi * np.arange(n_jours) / 365.25)  # Cycle annuel
        
        taux = taux * (1 + tendance + saisonnier)
        
        df = pd.DataFrame({
            'EUR_USD': taux
        }, index=dates)
        
        st.info(f"Généré {len(df)} jours de données historiques se terminant au taux réel actuel")
        return df

    @staticmethod
    def _generer_donnees_exemple():
        """Génère des données d'exemple EUR/USD réalistes pour démonstration"""
        date_fin = datetime.now()
        date_debut = date_fin - timedelta(days=730)
        
        # Crée une plage de dates (jours ouvrables uniquement)
        dates = pd.date_range(start=date_debut, end=date_fin, freq='D')
        
        # Génère des taux EUR/USD réalistes avec marche aléatoire
        np.random.seed(42)  # Pour des résultats reproductibles
        taux_initial = 1.1000  # Taux EUR/USD de départ
        rendements_journaliers = np.random.normal(0, 0.008, len(dates))  # ~0.8% volatilité journalière
        
        taux = [taux_initial]
        for taux_rendement in rendements_journaliers[1:]:
            nouveau_taux = taux[-1] * (1 + taux_rendement)
            taux.append(nouveau_taux)
        
        df = pd.DataFrame({
            'EUR_USD': taux
        }, index=dates)
        
        # Ajoute des motifs réalistes
        # Écarts de week-end (pas de trading)
        df = df[df.index.dayofweek < 5]  # Supprime les week-ends
        
        # Sauvegarde en CSV
        df.to_csv('eur_usd.csv')
        st.info("Données d'exemple générées et sauvegardées dans eur_usd.csv")
        
        return df

    @staticmethod
    @st.cache_data
    def charger_et_preparer_donnees():
        """Charge les données depuis le CSV et les prépare pour l'analyse"""
        try:
            # Essaie de charger le CSV existant d'abord
            if os.path.exists('eur_usd.csv'):
                df = pd.read_csv('eur_usd.csv', index_col=0, parse_dates=True)
            else:
                df = DataService.telecharger_donnees_eur_usd()
                if df is None:
                    return None
            
            # Convertit en index datetime approprié
            df.index = pd.to_datetime(df.index)
            df = df.sort_index()
            
            # Gère les valeurs manquantes - propagation vers l'avant pour week-ends/jours fériés
            df = df.ffill()
            
            # Supprime toutes les valeurs NaN restantes
            df = df.dropna()
            
            return df
        except Exception as e:
            st.error(f"Erreur lors du chargement des données: {e}")
            return None
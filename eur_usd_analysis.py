import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from data_service import DataService
from analysis_service import AnalysisService

st.set_page_config(page_title="Analyse des Taux EUR/USD", layout="wide")


def main():
    """Interface principale de l'application Streamlit"""
    st.title("📈 Analyse des Taux de Change EUR/USD")
    st.markdown("**Devoir d'analyse des taux de change EUR/USD sur les 2 dernières années**")
    
    # Indicateurs de complétion du devoir
    st.info("🎯 **UE2 exercice Analyse des Taux de Change:**")
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.success("✅ 1️⃣ Téléchargement des données")
    with col2:
        st.success("✅ 2️⃣ Chargement et préparation")
    with col3:
        st.success("✅ 3️⃣ Analyse exploratoire")
    with col4:
        st.success("✅ 4️⃣ Prévision naïve")
    
    # Chargement des données
    with st.spinner("Chargement des données EUR/USD..."):
        df = DataService.charger_et_preparer_donnees()
    
    if df is None:
        st.error("Échec du chargement des données. Veuillez vérifier votre connexion internet.")
        return
    
    # Section 1: Téléchargement et aperçu des données
    st.header("1️⃣ Téléchargement et Aperçu des Données")
    st.markdown("📁 **Données sauvegardées dans:** `eur_usd.csv`")
    col1, col2 = st.columns(2)
    
    with col1:
        st.metric("Nombre total de points", len(df))
        st.metric("Plage de dates", f"{df.index.min().date()} à {df.index.max().date()}")
    
    with col2:
        st.metric("Taux actuel", f"{df['EUR_USD'].iloc[-1]:.4f}")
        st.metric("Source des données", "API de taux de change")
    
    # Affichage des données brutes
    if st.checkbox("Afficher les données brutes"):
        st.dataframe(df.head(10))
    
    # Section 2: Chargement et préparation + Analyse exploratoire
    st.header("2️⃣ Chargement, Préparation et Analyse Exploratoire")
    st.markdown("📊 **Formule du rendement journalier:** `(Prix_t - Prix_{t-1}) / Prix_{t-1} * 100`")
    
    # Calcul des rendements journaliers
    df = AnalysisService.calculer_rendements_journaliers(df)
    
    # Affichage des statistiques
    stats = AnalysisService.calculer_statistiques_descriptives(df)
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.subheader("Statistiques du Taux de Change")
        st.metric("Moyenne", f"{stats['Moyenne']:.4f}")
        st.metric("Écart-type", f"{stats['Ecart_Type']:.4f}")
    
    with col2:
        st.metric("Minimum", f"{stats['Min']:.4f}")
        st.metric("Maximum", f"{stats['Max']:.4f}")
    
    with col3:
        st.subheader("Statistiques des Rendements")
        st.metric("Rendement moyen (%)", f"{stats['Moyenne_Rendement']:.4f}")
        st.metric("Volatilité (%)", f"{stats['Ecart_Type_Rendement']:.4f}")
    
    # Graphique du taux de change
    fig_rate = px.line(df, y='EUR_USD', title="Évolution du Taux EUR/USD dans le Temps")
    fig_rate.update_layout(xaxis_title="Date", yaxis_title="Taux EUR/USD")
    st.plotly_chart(fig_rate, use_container_width=True)
    
    # Graphique des rendements journaliers
    fig_returns = px.line(df, y='Rendement_Journalier', title="Rendements Journaliers (%)")
    fig_returns.update_layout(xaxis_title="Date", yaxis_title="Rendement Journalier (%)")
    st.plotly_chart(fig_returns, use_container_width=True)
    
    # Section 3: Prévision naïve
    st.header("3️⃣ Prévision Naïve")
    st.markdown("🔮 **Principe:** La valeur de demain = valeur d'aujourd'hui")
    
    df_prevision, rmse = AnalysisService.prevision_naive(df)
    
    st.metric("Erreur Quadratique Moyenne (RMSE)", f"{rmse:.6f}")
    
    # Graphique réel vs prévision pour les 30 derniers jours
    derniers_30_jours = df_prevision.tail(30)
    
    fig_prevision = go.Figure()
    fig_prevision.add_trace(go.Scatter(
        x=derniers_30_jours.index,
        y=derniers_30_jours['EUR_USD'],
        mode='lines+markers',
        name='Réel',
        line=dict(color='blue')
    ))
    fig_prevision.add_trace(go.Scatter(
        x=derniers_30_jours.index,
        y=derniers_30_jours['Prevision_Naive'],
        mode='lines+markers',
        name='Prévision Naïve',
        line=dict(color='red', dash='dash')
    ))
    
    fig_prevision.update_layout(
        title="Réel vs Prévision Naïve (30 Derniers Jours)",
        xaxis_title="Date",
        yaxis_title="Taux EUR/USD"
    )
    st.plotly_chart(fig_prevision, use_container_width=True)
    
    # Analyse des erreurs
    st.subheader("Analyse des Erreurs de Prévision")
    metriques_erreur = AnalysisService.calculer_erreurs_prevision(df_prevision)
    
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Erreur Absolue Moyenne", f"{metriques_erreur['Erreur_Absolue_Moyenne']:.6f}")
        st.metric("Erreur Moyenne", f"{metriques_erreur['Erreur_Moyenne']:.6f}")
    
    with col2:
        fig_erreur = px.histogram(metriques_erreur['Erreurs'], title="Distribution des Erreurs de Prévision", nbins=50)
        st.plotly_chart(fig_erreur, use_container_width=True)
    
    # Section téléchargement
    st.header("💾 Télécharger les Données")
    st.markdown("💿 **Fichier CSV généré automatiquement:** `eur_usd.csv`")
    if st.button("Télécharger les données EUR/USD en CSV"):
        csv = df.to_csv()
        st.download_button(
            label="Télécharger CSV",
            data=csv,
            file_name="analyse_eur_usd.csv",
            mime="text/csv"
        )

if __name__ == "__main__":
    main()
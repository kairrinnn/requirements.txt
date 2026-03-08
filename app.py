__import__('pysqlite3')
import sys
sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')

import streamlit as st
import os
from crewai import Agent, Task, Crew
from langchain_community.tools import DuckDuckGoSearchRun

# --- L'INTERFACE WEB ---
st.set_page_config(page_title="Mon AI Swarm Pro", page_icon="🌐", layout="wide")
st.title("🌐 AI Swarm Connecté à Internet")
st.write("Cet essaim de 5 experts scanne le web en direct pour créer des concepts viraux.")

# L'outil de recherche internet 100% gratuit
search_tool = DuckDuckGoSearchRun()

api_key = st.text_input("Entre ta clé API Groq :", type="password")
sujet = st.text_input("Sur quel sujet veux-tu lancer l'essaim ? (ex: Jeux vidéo, IA, Finance...)", value="Nouvelles tendances YouTube")

if st.button("🚀 Lancer l'Essaim Massif") and api_key and sujet:
    os.environ["GROQ_API_KEY"] = api_key
    
    with st.spinner(f"Les 5 agents scannent internet et brainstorment sur : {sujet}... 🧠"):
        
        modele_ia = "groq/llama-3.3-70b-versatile"

        # ==========================================
        # CRÉATION DE L'ESSAIM SPÉCIALISÉ (5 AGENTS)
        # ==========================================

        analyste_web = Agent(
            role="Analyste des Tendances Internet",
            goal=f"Scanner internet pour trouver les toutes dernières tendances, mèmes et actualités sur ce sujet : {sujet}",
            backstory="Tu es un hacker de l'attention. Tu sais exactement ce qui fait le buzz en ce moment sur les réseaux sociaux.",
            llm=modele_ia,
            tools=[search_tool] # On lui donne le pouvoir d'aller sur Google/DuckDuckGo !
        )

        visionnaire = Agent(
            role="Génie Créatif",
            goal="Prendre les tendances brutes d'internet et imaginer 3 concepts totalement fous et innovants.",
            backstory="Tu penses en dehors de la boîte. Tu mixes des idées qui n'ont rien à voir pour créer des concepts uniques.",
            llm=modele_ia
        )

        critique = Agent(
            role="Critique Impitoyable",
            goal="Détruire les idées faibles et sélectionner l'unique concept qui a le potentiel de casser internet.",
            backstory="Tu es cynique et ultra-exigeant. Si une idée est ennuyeuse ou déjà vue, tu la jettes à la poubelle.",
            llm=modele_ia
        )

        marketeur = Agent(
            role="Stratège Viralité",
            goal="Prendre le concept validé et lui inventer des titres putaclics, une miniature choquante et des hashtags.",
            backstory="Tu es un expert du clic. Tu sais comment manipuler l'algorithme pour faire des millions de vues.",
            llm=modele_ia
        )

        directeur = Agent(
            role="Directeur de Production",
            goal="Rassembler tout le travail de l'équipe dans un document final propre, structuré et prêt à être exécuté.",
            backstory="Tu es le boss final. Tu transformes le chaos créatif en un plan d'action clair pour le client.",
            llm=modele_ia
        )

        # ==========================================
        # LES MISSIONS (TÂCHES)
        # ==========================================

        tache1 = Task(
            description=f"Cherche sur internet les tendances d'aujourd'hui concernant : {sujet}.",
            expected_output="Un résumé des 3 plus grandes tendances actuelles sur ce sujet avec des détails.",
            agent=analyste_web
        )

        tache2 = Task(
            description="À partir du rapport de l'analyste, propose 3 idées de contenus/projets révolutionnaires.",
            expected_output="Une liste de 3 concepts fous détaillés.",
            agent=visionnaire
        )

        tache3 = Task(
            description="Critique les 3 concepts. Choisis le meilleur et explique pourquoi il va marcher.",
            expected_output="Le nom du concept gagnant et une critique expliquant pourquoi les autres sont nuls.",
            agent=critique
        )

        tache4 = Task(
            description="Crée un packaging viral pour le concept gagnant : 3 propositions de Titres, une idée de Miniature, et les angles d'accroche.",
            expected_output="Un plan marketing viral (Titres, Miniature, Accroche).",
            agent=marketeur
        )

        tache5 = Task(
            description="Fais la synthèse de tout. Rédige le document final complet du projet.",
            expected_output="Le Master Document structuré avec le concept, le plan marketing, et les étapes à suivre.",
            agent=directeur
        )

        # ==========================================
        # LANCEMENT DU SYSTÈME
        # ==========================================
        crew = Crew(
            agents=[analyste_web, visionnaire, critique, marketeur, directeur],
            tasks=[tache1, tache2, tache3, tache4, tache5],
            verbose=False,
            max_rpm=25 # LE RÉGULATEUR : Empêche de saturer l'API gratuite de Groq !
        )

        result = crew.kickoff()

    # --- AFFICHAGE ---
    st.success("Opération terminée avec succès !")
    st.markdown("### 🏆 Le Master Document de ton Essaim :")
    st.write(result.raw)

elif not api_key:
    st.warning("👆 N'oublie pas de mettre ta clé API pour démarrer.")

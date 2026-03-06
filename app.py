import streamlit as st
import os
from crewai import Agent, Task, Crew
from langchain_groq import ChatGroq

# --- L'INTERFACE WEB ---
st.set_page_config(page_title="Mon AI Swarm", page_icon="🐝")
st.title("🐝 Mon AI Swarm Générateur d'Idées")
st.write("Laisse mes agents IA brainstormer pour toi !")

# Champ pour entrer la clé API de façon sécurisée
api_key = st.text_input("Entre ta clé API Groq (gratuite sur console.groq.com) :", type="password")

if st.button("🚀 Lancer le Brainstorming") and api_key:
    os.environ["GROQ_API_KEY"] = api_key
    
    # On connecte le Llama 3 du cloud (très rapide)
    llm = ChatGroq(model="llama3-70b-8192")

    with st.spinner("Les agents sont en pleine réunion... 🧠"):
        
        # --- TES AGENTS ---
        explorer = Agent(
            role="Creative Explorer",
            goal="generate innovative ideas",
            backstory="expert in creative thinking",
            llm=llm # Il est crucial de donner le LLM à chaque agent !
        )

        critic = Agent(
            role="Critic",
            goal="analyze and critique ideas",
            backstory="expert in evaluating ideas",
            llm=llm
        )

        improver = Agent(
            role="Improver",
            goal="improve the best ideas",
            backstory="expert in optimization",
            llm=llm
        )

        # --- TES TÂCHES ---
        # Note : Dans les nouvelles versions de CrewAI, 'expected_output' est obligatoire
        task1 = Task(
            description="generate 5 viral video ideas",
            agent=explorer,
            expected_output="A list of 5 original viral video concepts."
        )

        task2 = Task(
            description="critique the ideas and remove weak ones",
            agent=critic,
            expected_output="A critique of the 5 ideas, highlighting the flaws and selecting the best one."
        )

        task3 = Task(
            description="improve the best idea and make it more original",
            agent=improver,
            expected_output="A final, highly detailed and optimized video concept ready for production."
        )

        # --- TON ESSAIM ---
        crew = Crew(
            agents=[explorer, critic, improver],
            tasks=[task1, task2, task3],
            verbose=False # On cache le texte de terminal pour l'interface web
        )

        result = crew.kickoff()

    # --- AFFICHAGE DU RÉSULTAT ---
    st.success("Brainstorming terminé !")
    st.markdown("### 🏆 L'Idée Finale :")
    st.write(result.raw)

elif not api_key:
    st.warning("👆 N'oublie pas de mettre ta clé API pour démarrer.")

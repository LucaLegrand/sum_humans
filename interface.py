import streamlit as st
import requests
from datetime import datetime

# URLs des endpoints
API_BASE_URL = "http://localhost:8000"
ENDPOINTS = {
    "instant_count": "/instant_count",
    "last_count": "/last_count",
    "multi_count": "/multi_count"
}

# Titre principal avec style personnalisé
st.markdown(
    """
    <style>
    .stApp {
        background-color: rgba(0, 122, 204, 0.8); /* Bleu opaque */
    }
    .title {
        font-size: 50px;
        font-weight: bold;
        color: white;
        text-align: center;
        font-family: 'Arial', sans-serif;
        margin-bottom: 20px;
    }
    .box {
        background-color: white;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 2px 2px 10px rgba(0, 0, 0, 0.3);
        font-family: 'Arial', sans-serif;
        color: #007acc;
        text-align: center;
        margin-bottom: 15px;
    }
    .stButton button {
        background-color: #007acc;
        color: white;
        border-radius: 8px;
        padding: 10px 20px;
        font-weight: bold;
        font-size: 16px;
        border: none;
        transition: all 0.3s ease;
        margin-top: 20px;
    }
    .stButton button:hover {
        background-color: #005f99;
        color: white;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Titre principal Σ-Humans
st.markdown('<div class="title">Σ-Humans</div>', unsafe_allow_html=True)

# Menu déroulant dans la sidebar
st.sidebar.title("Navigation")
option = st.sidebar.selectbox(
    "Choisissez l'action :",
    ["instant_count", "last_count", "multi_count"]
)

# Comportement en fonction de l'option sélectionnée
if option == "instant_count":
    st.markdown('<div class="box">Endpoint : Instant Count</div>', unsafe_allow_html=True)
    if st.button("Obtenir le nombre de personnes"):
        try:
            response = requests.get(API_BASE_URL + ENDPOINTS["instant_count"])
            if response.status_code == 200:
                data = response.json()
                st.markdown(f'<div class="box">Nombre de personnes détectées : <b>{data["instant_count"]}</b></div>', unsafe_allow_html=True)
                st.markdown(f'<div class="box">Date de la photo : <b>{data["photo_date"]}</b></div>', unsafe_allow_html=True)
            else:
                st.error(f"Erreur : Impossible de contacter l'API. Statut {response.status_code}")
        except Exception as e:
            st.error(f"Erreur lors de l'appel à l'API : {e}")

elif option == "last_count":
    st.markdown('<div class="box">Endpoint : Last Count</div>', unsafe_allow_html=True)
    if st.button("Obtenir le dernier compte"):
        try:
            response = requests.get(API_BASE_URL + ENDPOINTS["last_count"])
            if response.status_code == 200:
                data = response.json()
                st.markdown(f'<div class="box">Dernier compte : <b>{data["last_count"]}</b></div>', unsafe_allow_html=True)
                st.markdown(f'<div class="box">Date de la photo : <b>{data["photo_date"]}</b></div>', unsafe_allow_html=True)
            else:
                st.error(f"Erreur : Impossible de contacter l'API. Statut {response.status_code}")
        except Exception as e:
            st.error(f"Erreur lors de l'appel à l'API : {e}")

elif option == "multi_count":
    st.markdown('<div class="box">Endpoint : Multi Count</div>', unsafe_allow_html=True)

    # Sélection des dates et heures
    start_date = st.date_input("Date de début", datetime.now())
    start_time = st.time_input("Heure de début", datetime.now().time())
    end_date = st.date_input("Date de fin", datetime.now())
    end_time = st.time_input("Heure de fin", datetime.now().time())

    if st.button("Obtenir les comptes multiples"):
        try:
            # Construire les paramètres pour l'API
            params = {
                "start_date": start_date.strftime("%Y-%m-%d"),
                "start_time": start_time.strftime("%H:%M"),
                "end_date": end_date.strftime("%Y-%m-%d"),
                "end_time": end_time.strftime("%H:%M")
            }
            response = requests.get(API_BASE_URL + ENDPOINTS["multi_count"], params=params)
            if response.status_code == 200:
                data = response.json()

                # Vérification des erreurs retournées par l'API
                if "error" in data:
                    st.error(data["error"])
                else:
                    # Affichage des résultats
                    results = data["results"]
                    for result in results:
                        st.markdown(f'<div class="box">Date de la photo : <b>{result["photo_date"]}</b></div>', unsafe_allow_html=True)
                        st.markdown(f'<div class="box">Nombre de personnes détectées : <b>{result["count"]}</b></div>', unsafe_allow_html=True)
            else:
                st.error(f"Erreur : Impossible de contacter l'API. Statut {response.status_code}")
        except Exception as e:
            st.error(f"Erreur lors de l'appel à l'API : {e}")
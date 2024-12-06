from fastapi import FastAPI
import os
from datetime import datetime

app = FastAPI()

# Chemins vers les répertoires d'images
PERSPI_IMAGE_DIR = "Photos/undistorted_image_full"

# Fonction pour extraire la date et l'heure du nom de fichier
def extract_datetime_from_filename(filename):
    try:
        if "_sensor0" in filename:
            date_time_part = filename.split('_sensor0')[0]
            return datetime.strptime(date_time_part, "%d_%m_%Y_%H%M")
        else:
            return None
    except Exception as e:
        print(f"Erreur d'extraction de la date pour le fichier {filename}: {e}")
        return None

@app.get("/instant_count")
def get_instant_count():
    # Simuler une valeur fixe pour le test
    num_people = 5  # Valeur fixe pour tester l'interface
    return {"instant_count": num_people, 
            "photo_date": "2023-12-06 09:20:00",
            }

@app.get("/last_count")
def get_last_count():
    # Simuler une réponse avec les données pertinentes
    return {
        "last_count": 7,
        "photo_date": "2023-12-06 09:20:00",
    }

@app.get("/multi_count")
def get_multi_count(start_date: str, end_date: str):
    # Simuler une réponse avec des données factices
    results = [
        {"photo_date": "2023-12-04 14:32:00", "count": 7},
        {"photo_date": "2023-12-03 15:45:00", "count": 8},
        {"photo_date": "2023-12-02 10:10:00", "count": 6}
    ]
    return {"results": results}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
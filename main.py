from fastapi import FastAPI
import os
from Yolo_v3_copy import detect_humans  # Importer la nouvelle fonction depuis Yolo_v3_copy.py
from datetime import datetime

app = FastAPI()

# Chemins vers les répertoires d'images
PERSPI_IMAGE_DIR = "Photos/undistorted_image_full"

# Fonction pour extraire la date et l'heure du nom de fichier
def extract_datetime_from_filename(filename):
    try:
        # Assurer que le fichier correspond au format attendu "DD_MM_YYYY_HHMM_sensor0.jpg"
        if "_sensor0" in filename:
            # Extraire la partie "DD_MM_YYYY_HHMM"
            date_time_part = filename.split('_sensor0')[0]
            # Convertir en format utilisable pour le tri
            return datetime.strptime(date_time_part, "%d_%m_%Y_%H%M")
        else:
            # Retourner None pour les fichiers qui ne correspondent pas au format
            return None
    except Exception as e:
        print(f"Erreur d'extraction de la date pour le fichier {filename}: {e}")
        return None

@app.get("/instant_count")
def get_instant_count():
    # Lister les fichiers dans le répertoire
    image_files = [f for f in os.listdir(PERSPI_IMAGE_DIR) if f.endswith(".jpg")]

    # Filtrer et trier les fichiers qui respectent le format attendu
    image_files = [f for f in image_files if extract_datetime_from_filename(f) is not None]
    image_files = sorted(image_files, key=lambda x: extract_datetime_from_filename(x), reverse=True)

    if not image_files:
        return {"error": "Aucune image disponible"}

    # Récupérer la dernière image
    latest_image = os.path.join(PERSPI_IMAGE_DIR, image_files[0])

    try:
        # Appeler la fonction de détection à partir de Yolo_v3_copy.py
        num_people = detect_humans(latest_image)
        # Ajouter le nom du fichier analysé à la réponse JSON
        return {"instant_count": num_people, "image_name": os.path.basename(latest_image)}
    except Exception as e:
        return {"error": str(e)}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

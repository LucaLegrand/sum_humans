import os
import cv2
import numpy as np

# Fonction pour détecter le nombre de personnes dans une image
def detect_humans(image_path):
    classes = None
    with open("coco.names", 'r') as f:
        classes = f.read().strip().split('\n')

    # Chargement du modèle YOLOv3
    net = cv2.dnn.readNet("yolov3/yolov3.weights", "yolov3/yolov3_testing.cfg")

    layer_names = net.getLayerNames()
    output_layers_indices = net.getUnconnectedOutLayers()
    output_layers = [layer_names[i - 1] for i in output_layers_indices]

    # Chargement de l'image
    image = cv2.imread(image_path)
    height, width, channels = image.shape

    # Prétraitement de l'image
    blob = cv2.dnn.blobFromImage(image, 0.00392, (416, 416), (0, 0, 0), True, crop=False)
    net.setInput(blob)
    outs = net.forward(output_layers)

    class_ids = []
    confidences = []
    boxes = []

    # Analyse des sorties de YOLOv3 pour détecter les personnes (classe 0)
    for out in outs:
        for detection in out:
            scores = detection[5:]
            class_id = np.argmax(scores)
            confidence = scores[class_id]
            if confidence > 0.5 and class_id == 0:  # Classe 0 pour humain
                # Récupérer les coordonnées de la boîte englobante
                center_x = int(detection[0] * width)
                center_y = int(detection[1] * height)
                w = int(detection[2] * width)
                h = int(detection[3] * height)
                x = int(center_x - w / 2)
                y = int(center_y - h / 2)
                boxes.append([x, y, w, h])
                confidences.append(float(confidence))
                class_ids.append(class_id)

    # Suppression des détections redondantes
    indices = cv2.dnn.NMSBoxes(boxes, confidences, 0.5, 0.4)

    # Retourner le nombre de personnes détectées
    return len(indices)

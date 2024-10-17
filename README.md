# Sum Humans

### Project Overview

**Sum Humans** is a project aimed at establishing correlations between environmental factors such as carbon dioxide (CO2) emissions and sound levels with the number of occupants in the Energy Lab (EL). The project retrieves real-time occupancy data using computer vision (via the **Perspiclass** project) and integrates it with environmental sensor data to provide a comprehensive monitoring solution.

### Project Structure

The project contains the following main components:
- **REST API**: A FastAPI-based server exposing endpoints to fetch real-time occupancy data.
- **Perspiclass Integration**: Uses computer vision (YOLOv3) to count the number of people in images captured by the Energy Lab camera.
- **Future Integration**: Planned support to correlate environmental data (CO2, noise levels) with the occupancy count.

---

## Features

- **Real-Time Occupancy Count**: Retrieve the latest number of occupants detected in the Energy Lab using the `/instant_count` endpoint.
- **Image Processing**: Detect humans using YOLOv3 from fisheye camera images.
- **Easy Integration**: Extendable API design, ready to incorporate environmental data for advanced monitoring.

---

## API Endpoints

| HTTP Method | Endpoint          | Description                                |
| ----------- | ----------------- | ------------------------------------------ |
| `GET`       | `/instant_count`   | Returns the latest occupancy count and the image file analyzed. |

### Sample Response

```json
{
  "instant_count": 5,
  "image_name": "01_10_2024_1530_sensor0.jpg"
}
```

## Prerequisites

Ensure the following tools are installed on your machine:
- **Python 3.7+**
- **Git** (for version control)
- **YOLOv3 Weights & Config Files**: Make sure the YOLOv3 model files (`yolov3.weights`, `yolov3_testing.cfg`, and `coco.names`) are available.

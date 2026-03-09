# Smart AI Campus

AI-powered campus surveillance and identity recognition system built using **Computer Vision, Deep Learning, and FastAPI**.

The system detects people using **YOLOv8**, tracks them in real time, recognizes faces using **FaceNet**, and logs movements across cameras inside a campus environment.

---

# Project Overview

Smart AI Campus is designed to simulate a **modern intelligent surveillance system** that can:

* Detect people in camera streams
* Track individuals across frames
* Recognize registered faces
* Detect unknown individuals
* Log identity events
* Support multiple cameras across campus

The project integrates **AI, backend APIs, and database systems** into a single pipeline.

---

# System Architecture

```
Camera
  ↓
YOLO Detection
  ↓
Tracking Engine
  ↓
Snapshot Capture
  ↓
Face Recognition (FaceNet)
  ↓
Database Matching
  ↓
Logging System
  ↓
Alerts
  ↓
Visualization
```

---

# Features

### Person Detection

Uses **YOLOv8** to detect people in real-time video streams.

### Face Recognition

Uses **FaceNet via DeepFace** to generate facial embeddings and match them against registered users.

### Identity Tracking

Each detected person is assigned a **tracking ID** to maintain identity across frames.

### Snapshot System

Captures a snapshot of each detected individual for recognition.

### Alert System

Triggers alerts when an **unknown person** is detected.

### Logging System

Every recognition event is stored in the database.

### Multi-Camera Ready

System architecture supports multiple cameras across campus locations.

---

# Tech Stack

* Python
* FastAPI
* OpenCV
* YOLOv8 (Ultralytics)
* DeepFace (FaceNet)
* PostgreSQL
* NumPy

---

# Project Structure

```
Smart_AI_Campus
│
├── api
│   └── routes.py
│
├── core
│   ├── tracking_engine.py
│   ├── recognition_engine.py
│   ├── snapshot_manager.py
│   ├── logging_service.py
│   ├── identity_cache.py
│   ├── live_camera.py
│   └── camera_manager.py
│
├── db
│   └── database.py
│
├── models
│
├── snapshots
├── temp
│
├── config.py
├── main.py
├── requirements.txt
└── README.md
```

---

# Installation

### Clone the repository

```
git clone https://github.com/yourusername/smart-ai-campus.git
cd smart-ai-campus
```

---

### Create virtual environment

```
python -m venv venv
```

Activate it:

```
venv\Scripts\activate
```

---

### Install dependencies

```
pip install -r requirements.txt
```

---

# Download YOLO Model

Download YOLO weights and place them in the project root or models folder.

Example:

```
yolov8n.pt
```

---

# Run the Server

```
python -m uvicorn main:app --reload
```

---

# API Documentation

Open Swagger UI:

```
http://127.0.0.1:8000/docs
```

Available endpoints include:

```
POST /register-person
POST /track_snapshot
POST /detect_phone
GET  /live_camera
GET  /start_campus_cameras
GET  /attendance/history
GET  /attendance/summary
```

---

# Database

The system uses **PostgreSQL**.

Main tables:

### persons

Stores registered identities.

```
id
name
embedding
```

### recognition_logs

Stores recognition events.

```
person_id
tracking_id
camera_id
timestamp
status
```

---

# Example Output

When the camera detects a registered user:

```
Ahmed (ID 1)
```

If the system detects an unknown person:

```
Unknown
```

---

# Future Improvements

* DeepSORT / ByteTrack tracking
* Telegram / Email alerts
* Web dashboard
* Real multi-camera synchronization
* Mobile notifications

---

# Author

Ahmed Saad

AI & Computer Vision Project

---

# License

This project is for educational and research purposes.

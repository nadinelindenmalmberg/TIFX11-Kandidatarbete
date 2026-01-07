# TIFX11 Kandidatarbete
A full-stack web application for video pose estimation and human keypoint detection using machine learning.

## 🚀 Tech Stack

**Frontend**
- React 18
- React Router
- Axios

**Backend**
- Django 4.2
- Django REST Framework
- SQLite

## 📋 Prerequisites

- Node.js and npm
- Python 3
- pip

## 🛠️ Installation

### Backend Setup

```bash
cd server/my_project_directory
pip install -r ../../requirements.txt
python manage.py migrate
python manage.py runserver
```

### Frontend Setup

```bash
cd client
npm install
npm start
```

The React app will run on `http://localhost:3000` and proxy requests to the Django backend at `http://localhost:8000`.

## 📁 Project Structure

```
├── client/           # React frontend
│   └── src/
│       └── components/
│           ├── Navbar/
│           ├── VideoUpload/
│           └── Results/
└── server/           # Django backend
    └── my_project_directory/
        └── my_ml_app/
```

## ✨ Features

- Video upload functionality
- **Pose estimation** - Detects 18 human body keypoints per frame
- Frame-by-frame analysis with bounding box detection
- JSON-based results processing
- Real-time results visualization
- RESTful API integration

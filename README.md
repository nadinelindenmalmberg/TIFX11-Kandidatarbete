# RunInsight: AI-Powered Biomechanical Motion Analysis

**RunInsight** is a full-stack web application that democratizes biomechanical analysis by transforming raw 2D video footage into interactive 3D kinematic visualizations.  
Developed as a **Master of Science in Engineering thesis project at Chalmers University of Technology**, in collaboration with the **Swedish Athletics Association**.

---

## 🚀 Project Overview

Traditional motion capture requires expensive labs and physical markers.  
RunInsight leverages state-of-the-art **Deep Learning (Transformer-based models)** to perform **markerless motion capture**, allowing coaches and runners to upload simple smartphone videos and receive professional-grade gait analysis.

The system uses **MotionBERT**, a dual-stream spatio-temporal transformer model, to lift 2D pose estimations into 3D space—enabling detailed analysis of joint angles, step frequency, and running technique.

---

## 🛠 Tech Stack

**Frontend**
- React.js  
- CSS3  

**Backend**
- Django (Python)  
- Django REST Framework  

**AI / ML**
- PyTorch  
- MMPose  
- MotionBERT (Transformer-based architecture)  
- RTMPose  

**Data Processing**
- NumPy  
- Pandas  
- OpenCV  

**Ground Truth Validation**
- Qualisys Track Manager (QTM)  
- COCO format  

---

## ✨ Key Features

- **2D-to-3D Pose Estimation**  
  Automated pipeline transforming single-camera 2D footage into 3D skeletal models using MotionBERT.

- **Interactive 3D Visualization**  
  Web-based 3D environment where users can rotate, zoom, and inspect runner biomechanics frame-by-frame.

- **Kinematic Analysis**  
  Automatic calculation of critical running metrics such as knee flexion angles and step frequency.

- **Inference Pipeline**  
  Custom-engineered backend pipeline handling video serialization, tensor processing, and JSON response formatting for client-side rendering.

---

## 🏗 Architecture

The application follows a **decoupled client–server architecture**:

### Client (React)
- Handles video upload  
- Renders the 3D visualizer using JSON-based coordinate data  

### Server (Django)
- Orchestrates the full inference pipeline:
  - **Preprocessing**: Extracts frames from uploaded video  
  - **Inference**:  
    - RTMPose for 2D pose detection  
    - MotionBERT for 3D pose lifting (via MMPose)  
  - **Serialization**: Converts tensor outputs into structured JSON for frontend consumption  

---

## 📊 Dataset & Validation

To validate model accuracy for running kinematics, a custom evaluation pipeline was built at the **Chalmers Physiology Lab**.

- **Data Collection**  
  High-fidelity ground-truth motion capture using a Qualisys optical system (12+ cameras).

- **Validation Pipeline**  
  Custom scripts synchronize MotionBERT predictions with Qualisys ground truth data to compute **Mean Per Joint Position Error (MPJPE)**.

---

## 📌 Summary

RunInsight demonstrates how modern transformer-based models can bring lab-grade biomechanical analysis to everyday environments—bridging sports science, computer vision, and web-based visualization into a single, accessible system.

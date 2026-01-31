# 👁️ Arjun Netra: AI-Powered Traffic Enforcement System

![Python](https://img.shields.io/badge/Python-3.10%2B-blue)
![YOLOv11](https://img.shields.io/badge/AI-YOLOv11-orange)
![OpenCV](https://img.shields.io/badge/Vision-OpenCV-green)
![Status](https://img.shields.io/badge/Status-Hackathon%20Prototype-red)

**Arjun Netra** is a cost-effective, mobile-first AI solution designed to democratize traffic enforcement. By leveraging a **"Bring Your Own Device" (BYOD)** architecture, it transforms any standard smartphone and laptop into a smart traffic monitoring unit capable of detecting violations and reading license plates in real-time.

---

## 🚀 Key Features

* **🧠 Real-Time Violation Detection:** Instantly identifies "No Helmet" and "Triple Riding" violations using **YOLOv11**.
* **📝 Automatic License Plate Recognition (ANPR):** Extracts vehicle registration numbers using **EasyOCR** on keyframes.
* **🔊 Instant Feedback:** Triggers an audio alert ("Beep") immediately upon detection to enable active interception.
* **📡 Wireless Streaming:** Uses low-latency **WiFi Direct (UDP/HTTP)** to stream video from a Helmet Camera to the Compute Unit.
* **☁️ Evidence Logging:** Auto-saves violation snapshots with timestamps and syncs them to the Cloud (Firebase).

---

## 🛠️ Tech Stack & Technologies Used

We chose a high-performance stack optimized for edge computing and real-time inference.

### 1. **Computer Vision: OpenCV**
* **Role:** The visual backbone of the system.
* **Why used:** Used for acquiring the video stream from the IP Camera, resizing frames for performance, and drawing bounding boxes/overlays on the dashboard.

### 2. **Artificial Intelligence: Ultralytics YOLOv11**
* **Role:** Object Detection Engine.
* **Why used:** YOLOv11 (Nano) provides the best balance between speed (60 FPS on CPU) and accuracy. We use it to detect `Person` and `Motorcycle` classes and apply geometric logic to identify riders.

### 3. **Optical Character Recognition: EasyOCR**
* **Role:** Number Plate Reading.
* **Why used:** A robust deep-learning-based OCR model that handles noisy, tilted, or low-resolution text better than Tesseract. We implement an **Interleaved Processing** strategy (running OCR only every 10th frame) to maintain system speed.

### 4. **Hardware Interface: Android IP Webcam**
* **Role:** Wireless Vision Node.
* **Why used:** Eliminates the need for expensive dedicated hardware. It turns a standard Android phone into a high-res wireless network camera.

### 5. **Backend/Database: Google Firebase (Optional Integration)**
* **Role:** Cloud Storage.
* **Why used:** For scalable, real-time storage of violation images (`Storage`) and challan metadata (`Firestore`).

---

## ⚙️ Architecture

```mermaid
graph LR
    A[Helmet Camera  Android Phone] -- WiFi Stream --> B(Compute Node \n Laptop/Jetson);
    B -- YOLOv11 --> C{Violation Check};
    C -- Yes --> D[Trigger Audio Alert];
    C -- Yes --> E[Save Evidence];
    E -- Internet --> F[Firebase Cloud];
    E -- Interleaved --> G[EasyOCR Plate Read];

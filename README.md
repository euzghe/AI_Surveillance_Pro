# 🛡️ AI Surveillance Pro: Airport Security & Analytics System

This project is a comprehensive end-to-end security solution designed for high-traffic areas like airports and customs zones. It leverages real-time computer vision and artificial intelligence to detect border breaches and track specific entities.

Unlike standard object detection, this system utilizes **Instance Segmentation** to precisely mask objects, providing granular data analysis and high-fidelity visual evidence.



## 🚀 Key Features

* **🔍 AI Engine:** Powered by **YOLOv8-Segmentation** for real-time tracking of passengers and "suspicious" items (bottles, bags, etc.).
* **⚡ Hardware Acceleration:** Fully optimized for Apple Silicon (M1/M2/M3) using **MPS (Metal Performance Shaders)** for high-FPS processing.
* **📊 Live Dashboard:** A sleek, web-based interface displaying real-time crossing statistics and captured violation snapshots.
* **🗄️ Persistent Storage:** Integrated with a **PostgreSQL** database to log every breach with timestamps, unique object IDs, and image paths.
* **🛠️ Modern Architecture:** Built with **FastAPI** (Python) for asynchronous data handling and low-latency API communication.

## 🛠️ Technology Stack

| Component | Technology |
| :--- | :--- |
| **AI & Vision** | Python, Ultralytics YOLOv8-Seg, OpenCV |
| **Backend** | FastAPI, Uvicorn |
| **Database** | PostgreSQL, Psycopg2 |
| **Frontend** | HTML5, Bootstrap 5, JavaScript (Fetch API) |
| **Security** | Python-Dotenv (Environment Variable Management) |



## 📦 Installation & Setup

1.  **Clone the Repository:**
    ```bash
    git clone [https://github.com/euzghe/AI_Surveillance_Pro.git](https://github.com/euzghe/AI_Surveillance_Pro.git)
    cd AI_Surveillance_Pro
    ```

2.  **Environment Setup:**
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
    ```

3.  **Database Configuration:**
    Create a `.env` file in the root directory and define your credentials:
    ```text
    DB_PASSWORD=your_secure_password
    ```

4.  **Run the System:**
    * **Start Backend:** `uvicorn api:app --reload`
    * **Start AI Engine:** `python main.py`
    * **View Dashboard:** Open `index.html` in your browser.

## 🎯 Project Logic (Vertical Border Breach)
The system overlays a virtual vertical line on the video feed. When an entity crosses this line:
1. The AI **segments (masks)** the object for visual evidence.
2. A high-resolution snapshot is saved locally.
3. The metadata is logged into the **PostgreSQL** database.
4. The Web Dashboard UI updates instantly via polling the API.

---
⭐ **Developed as a Senior Project for Software Engineering (4th Year).**

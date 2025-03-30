# 🏝️ AI Travel Planner

AI Travel Planner is a **smart travel itinerary generator** that helps users plan personalized trips using **Google Gemini AI**. It generates **customized itineraries**, provides **map-based locations**, and allows users to **download their itinerary as a PDF**.

## 🚀 Features

✅ **AI-Powered Itinerary Generation** – Generates personalized travel plans.  
✅ **Interactive Maps** – Displays locations using OpenStreetMap.  
✅ **Download Itinerary as PDF** – Saves the travel plan for offline use.  
✅ **User-Friendly Interface** – Built with **Streamlit** for an easy experience.  
✅ **Fast & Efficient Backend** – Uses **Flask API** with Gemini AI.  
✅ **Real-time Search Suggestions** – Provides instant city search functionality.  

---

## 📌 Tech Stack

🔹 **Frontend**: Streamlit  
🔹 **Backend**: Flask  
🔹 **AI Model**: Google Gemini API  
🔹 **Maps & Geolocation**: OpenStreetMap  
🔹 **Deployment**: Render  

---

## 🛠️ Installation & Setup

### **1️⃣ Clone the Repository**
```bash
git clone https://github.com/yourusername/ai-travel-planner.git
cd ai-travel-planner
```
### **2️⃣ Create & Activate Virtual Environment**
```bash
python3 -m venv venv
source venv/bin/activate  # On macOS/Linux
venv\Scripts\activate  # On Windows
```
### **3️⃣ Install Dependencies**
```bash
pip install -r requirements.txt
```
### **4️⃣ Set Up API Keys**
Create a .env file and add your API keys:
```
GEMINI_API_KEY=your_gemini_api_key
UNSPLASH_ACCESS_KEY=your_unsplash_api_key
OPENWEATHER_API_KEY=your_weather_api_key
```
### **5️⃣ Run the Backend (Flask API)**
```bash
python server.py
```
### **6️⃣ Run the Frontend (Streamlit)**
```bash
streamlit run app.py
```

## 🎯 Usage
### 1️⃣ Enter your destination city (e.g., Paris).
### 2️⃣ Select trip duration (e.g., 3 days).
### 3️⃣ Click "Generate Itinerary" to get a personalized plan.
### 4️⃣ View the AI-generated trip plan with recommendations.
### 5️⃣ Explore locations on the map for better insights.
### 6️⃣ Click "Download PDF" to save the itinerary.

## 🌍 Deployment Guide
### Deploy Backend on Render
#### Push your code to GitHub.

#### Go to Render and create a new Web Service.

#### Connect your GitHub repository.

#### Set the Start Command as:
```bash
python server.py
```
#### Deploy & get the public API URL.

### Deploy Frontend on Streamlit Cloud
#### Go to Streamlit Cloud.

#### Create a new app and connect your GitHub repository.

#### Set the Main File Path to app.py.

#### Deploy & share the app link! 🚀

## 🤝 Contributing
### 🔹 Fork the repository
### 🔹 Create a new branch (feature-xyz)
### 🔹 Commit your changes
### 🔹 Push the branch & create a PR

## 📜 License
This project is open-source under the MIT License.

## 📩 Contact
For any questions, reach out to:
📧 garimaabhayanaa@gmail.com

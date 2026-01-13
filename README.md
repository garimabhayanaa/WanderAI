# WanderAI — Product Context

## Overview
WanderAI is a travel itinerary planning tool designed to help users quickly generate personalized, usable travel plans without manual research across multiple sources. The product explores how AI-driven recommendations can balance personalization, clarity, and user control in consumer-facing planning workflows.

## Problem & User Context
Planning a trip often requires users to:
1. Search across multiple platforms for attractions, routes, and logistics
2. Manually reconcile preferences like budget, time, and interests
3. Convert scattered information into a structured, day-by-day plan
   
The core problem was:
How can an AI system reduce planning effort without overwhelming users or removing their sense of control?

## Users & Assumptions

### Intended users
1. Individuals planning short trips or vacations
2. Users who want guidance, not rigid schedules

### Key assumptions
1. Users prefer clear, high-level itineraries over exhaustive lists
2. Visual context (maps) improves trust in recommendations
3. Offline access (PDF export) increases usefulness during travel

## Solution & Key Decisions

### Key product decisions included:
1. Preference-based itinerary generation
The system generates plans based on destination and trip duration, keeping inputs minimal to reduce friction.
2. Map-based visualization
Locations are shown on an interactive map to help users understand geography and feasibility.
3. Downloadable itineraries
PDF export was prioritized to support offline access and real-world usage.
4. Lightweight UI
Streamlit was chosen to keep the interface simple and fast, focusing on clarity over customization.

## Tradeoffs & Constraints
Several tradeoffs shaped the product:

1. Personalization vs complexity
Limiting input parameters reduced precision but improved usability and speed.

2. Automation vs user control
The system suggests itineraries but avoids locking users into rigid plans.

3. Rich detail vs readability
Recommendations are concise to prevent information overload.

## Learnings & Improvements

Key takeaways from building WanderAI:
1. Over-personalization can reduce usability in planning tools
2. Users value confidence and clarity over exhaustive options
3. Visual context significantly improves trust in AI recommendations

Future improvements could include:
1. Optional preference tuning (interests, pace, budget)
2. Feedback-driven refinement of recommendations
3. Multi-city or longer trip support

## Technical Implementation

### Features

**AI-Powered Itinerary Generation** – Generates personalized travel plans.  
**Interactive Maps** – Displays locations using OpenStreetMap.  
**Download Itinerary as PDF** – Saves the travel plan for offline use.  
**User-Friendly Interface** – Built with **Streamlit** for an easy experience.  
**Fast & Efficient Backend** – Uses **Flask API** with Gemini AI.  
**Real-time Search Suggestions** – Provides instant city search functionality.  

---

### Tech Stack

**Frontend**: Streamlit  
**Backend**: Flask  
**AI Model**: Google Gemini API  
**Maps & Geolocation**: OpenStreetMap  
**Deployment**: Render  

---

### Installation & Setup

**1. Clone the Repository**
```bash
git clone https://github.com/yourusername/WanderAI.git
cd WanderAI
```
**2. Create & Activate Virtual Environment**
```bash
python3 -m venv venv
source venv/bin/activate  # On macOS/Linux
venv\Scripts\activate  # On Windows
```
**3. Install Dependencies**
```bash
pip install -r requirements.txt
```
**4. Set Up API Keys**
Create a .env file and add your API keys:
```
GEMINI_API_KEY=your_gemini_api_key
UNSPLASH_ACCESS_KEY=your_unsplash_api_key
OPENWEATHER_API_KEY=your_weather_api_key
```
**5. Run the Backend (Flask API)**
```bash
python server.py
```
**6. Run the Frontend (Streamlit)**
```bash
streamlit run app.py
```

### Usage
1. Enter your destination city (e.g., Paris).
2. Select trip duration (e.g., 3 days).
3. Click "Generate Itinerary" to get a personalized plan.
4. View the AI-generated trip plan with recommendations.
5. Explore locations on the map for better insights.
6. Click "Download PDF" to save the itinerary.

### Deployment Guide
#### Deploy Backend on Render
1. Push your code to GitHub.
2. Go to Render and create a new Web Service.
3. Connect your GitHub repository.
4. Set the Start Command as:
```bash
python server.py
```
5. Deploy & get the public API URL.

#### Deploy Frontend on Streamlit Cloud
1. Go to Streamlit Cloud.
2. Create a new app and connect your GitHub repository.
3. Set the Main File Path to app.py.
4. Deploy & share the app link! 

## Contributing
1. Fork the repository
2. Create a new branch (feature-xyz)
3. Commit your changes
4. Push the branch & create a PR

## License
This project is open-source under the MIT License.

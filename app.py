import streamlit as st
import os
import requests
import json
from io import BytesIO
from fpdf import FPDF
import folium
from streamlit_folium import st_folium
import datetime
import google.generativeai as genai


API_URL = "http://127.0.0.1:5000/api/itinerary"  # Flask API endpoint
UNSPLASH_API_KEY = os.getenv('UNSPLASH_ACCESS_KEY')
OPENWEATHER_API_KEY = os.getenv('OPENWEATHER_API_KEY')

# Page configuration with custom theme and favicon
st.set_page_config(
    page_title="WanderAI",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better UI
st.markdown("""
<style>
    /* Global styles and resets */
    * {
        font-family: 'Segoe UI', Roboto, Helvetica, sans-serif;
    }
    
    [data-testid="stAppViewContainer"] {
        background: linear-gradient(135deg, #f5f7fa 0%, #e4ecfb 100%);
        color: #2c3e50;
        padding: 0;
    }
    
    [data-testid="stSidebar"] {
        background: black;
        border-right: none;
        box-shadow: 2px 0 10px rgba(0, 0, 0, 0.05);
        padding-top: 2rem;
    }
    
    [data-testid="stSidebar"] .block-container {
        padding-top: 1rem;
    }
    
    /* Header styles */
    .main-header {
        font-size: 3.2rem !important;
        font-weight: 800;
        background: linear-gradient(90deg, #3a7bd5, #00d2ff);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin: 1.5rem 0;
        text-shadow: 0 1px 1px rgba(0,0,0,0.1);
    }
    
    .subheader {
        font-size: 1.8rem !important;
        font-weight: 700;
        color: #3a7bd5;
        margin: 1.5rem 0 1rem;
        border-bottom: 2px solid #e0e6ed;
        padding-bottom: 0.5rem;
    }
    
    /* Card styles */
    .card {
        background-color: white;
        border-radius: 12px;
        box-shadow: 0 8px 16px rgba(0,0,0,0.08);
        margin-bottom: 24px;
        transition: transform 0.2s ease, box-shadow 0.2s ease;
        overflow: hidden;
        padding: 24px;
        border: 1px solid rgba(0,0,0,0.05);
    }
    
    .card:hover {
        transform: translateY(-4px);
        box-shadow: 0 12px 20px rgba(0,0,0,0.12);
    }
    
    /* Day and activity styles */
    .day-header {
        background: linear-gradient(90deg, #3a7bd5, #6aadf1);
        color: white;
        padding: 14px 20px;
        border-radius: 10px;
        margin: 24px 0 16px;
        font-weight: 600;
        box-shadow: 0 4px 8px rgba(58, 123, 213, 0.2);
    }
    
    .day-header h3 {
        margin: 0;
        font-weight: 700;
        color: white;
    }
    
    .activity-item {
        padding: 14px 18px;
        margin: 10px 0;
        background-color: #f8faff;
        border-radius: 8px;
        border-left: 4px solid #3a7bd5;
        transition: all 0.2s ease;
    }
    
    .activity-item:hover {
        background-color: #edf3ff;
        transform: translateX(4px);
    }
    
    /* Weather card styles */
    .weather-card {
        background: linear-gradient(135deg, #c2e9fb 0%, #a1c4fd 100%);
        color: white;
        padding: 18px;
        border-radius: 12px;
        margin: 20px 0;
        box-shadow: 0 6px 12px rgba(102, 166, 255, 0.2);
    }
    
    /* Info box styles */
    .info-box {
        background: linear-gradient(135deg, #c2e9fb 0%, #a1c4fd 100%);
        color: white;
        padding: 18px;
        border-radius: 12px;
        margin: 20px 0;
        box-shadow: 0 6px 12px rgba(253, 160, 133, 0.2);
    }
    
    /* Button styles */
    div.stButton > button {
        background: linear-gradient(90deg, #3a7bd5, #00d2ff);
        border: none;
        border-radius: 8px;
        color: white;
        font-weight: 600;
        padding: 12px 20px;
        width: 100%;
        transition: all 0.3s ease;
    }
    
    div.stButton > button:hover {
        background: linear-gradient(90deg, #3372c5, #00c0e8);
        box-shadow: 0 5px 15px rgba(0, 210, 255, 0.3);
        transform: translateY(-2px);
    }
    
    div.stButton > button:active {
        transform: translateY(0);
    }
    
    /* Download button styles */
    .stDownloadButton > button {
        background: linear-gradient(90deg, #3a7bd5, #00d2ff);
        color: white;
        font-weight: 600;
        padding: 12px 20px;
        border-radius: 8px;
        border: none;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        transition: all 0.3s ease;
    }
    
    .stDownloadButton > button:hover {
        background: linear-gradient(90deg, #3372c5, #00c0e8);
        box-shadow: 0 6px 8px rgba(0,0,0,0.15);
        transform: translateY(-2px);
    }
    
    /* Input field styles */
    .stTextInput > div > div > input {
        border-radius: 8px;
        border: 1px solid #e0e6ed;
        padding: 10px 14px;
        box-shadow: 0 2px 5px rgba(0,0,0,0.05);
        transition: all 0.3s ease;
    }
    
    .stTextInput > div > div > input:focus {
        border-color: #3a7bd5;
        box-shadow: 0 0 0 2px rgba(58, 123, 213, 0.2);
    }
    
    /* Slider styles */
    .stSlider > div > div > div {
        color: white;
    }
    
    /* Selectbox styles */
    .stSelectbox > div > div > div {
        background-color: white;
        color:black;
        border-radius: 8px;
        border: 1px solid #e0e6ed;
    }
    
    /* Budget and info panel styles */
    .budget-panel {
        background: linear-gradient(135deg, #c2e9fb 0%, #a1c4fd 100%);
        padding: 20px;
        border-radius: 12px;
        margin: 20px 0;
        box-shadow: 0 6px 12px rgba(161, 196, 253, 0.2);
        color: #2c3e50;
    }
    
    /* Warning styles */
    .warning-panel {
        background: linear-gradient(135deg, #ffdfdf 0%, #ffbbbb 100%);
        padding: 14px;
        border-radius: 8px;
        margin: 10px 0;
        box-shadow: 0 4px 8px rgba(255, 187, 187, 0.2);
    }
    
    /* Footer styles */
    .footer {
        text-align: center;
        margin-top: 60px;
        padding-top: 30px;
        border-top: 1px solid #e0e6ed;
        color: #7f8fa4;
    }
    
    /* Responsive adjustments */
    @media (max-width: 768px) {
        .main-header {
            font-size: 2.5rem !important;
        }
        
        .subheader {
            font-size: 1.5rem !important;
        }
        
        .card, .day-header, .activity-item {
            padding: 14px;
        }
    }
</style>
""", unsafe_allow_html=True)

# API key warnings with better styling
if not UNSPLASH_API_KEY:
    st.sidebar.markdown("""
    <div class="warning-panel">
    ⚠️ <b>Unsplash API key not found.</b> Images won't be displayed.
    </div>
    """, unsafe_allow_html=True)
if not OPENWEATHER_API_KEY:
    st.sidebar.markdown("""
    <div class="warning-panel">
    ⚠️ <b>OpenWeather API key not found.</b> Weather won't be displayed.
    </div>
    """, unsafe_allow_html=True)

# Header with custom styling
st.markdown('<h1 class="main-header">WanderAI</h1>', unsafe_allow_html=True)
st.markdown("""
<div style="text-align:center;margin-bottom:30px;font-size:1.2rem;color:#5a6d87;">
Your AI-generated travel itinerary, tailored just for you! Plan your dream vacation effortlessly.
</div>
""", unsafe_allow_html=True)

# Average cost per day (in USD) for different travel styles
budget_levels = {
    "Economical": {"hotel": 30, "food": 10, "transport": 5},
    "Mid-Range": {"hotel": 70, "food": 25, "transport": 15},
    "Luxury": {"hotel": 200, "food": 50, "transport": 40},
}

def estimate_budget(days, travel_style):
    costs = budget_levels.get(travel_style, budget_levels["Mid-Range"])
    total_cost = (costs["hotel"] + costs["food"] + costs["transport"]) * days
    return total_cost

def get_weather(destination):
    if not OPENWEATHER_API_KEY:
        return None, None, None
        
    url = f"https://api.openweathermap.org/data/2.5/weather?q={destination}&appid={OPENWEATHER_API_KEY}&units=metric"
    
    try:
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            temp = data["main"]["temp"]
            weather_desc = data["weather"][0]["description"].capitalize()
            icon_code = data["weather"][0]["icon"]
            icon_url = f"http://openweathermap.org/img/wn/{icon_code}@2x.png"
            return temp, weather_desc, icon_url
        else:
            return None, None, None
    except Exception:
        return None, None, None

# Sidebar for user input with better organization
with st.sidebar:
    st.markdown('<h3 style="color:#3a7bd5;font-weight:700;margin-bottom:20px;"> Plan Your Trip</h3>', unsafe_allow_html=True)
    
    destination = st.text_input("📍 Destination", "Paris")
    
    col1, col2 = st.columns(2)
    with col1:
        num_days = st.slider(" Days", 1, 10, 3)
    with col2:
        travel_style = st.selectbox(" Budget Level", ["Economical", "Mid-Range", "Luxury"])
    
    transport = st.selectbox(" Transport", ["Public Transport", "Car Rental", "Walking"])
    
    # Budget estimation with better styling
    estimated_cost = estimate_budget(num_days, travel_style)
    st.markdown("""
    <div class="budget-panel">
        <h4 style="margin:0;color:#2c3e50;font-weight:700;"> Budget Estimate</h4>
        <p style="margin:10px 0 0 0;">For {} days in {} ({} style):</p>
        <p style="font-size:1.8rem;font-weight:700;margin:5px 0;color:#2c3e50;">${}
    </div>
    """.format(num_days, destination, travel_style.lower(), estimated_cost), unsafe_allow_html=True)
    
    # Fetch and Display Weather with better styling
    temp, weather_desc, icon_url = get_weather(destination)
    
    if temp and weather_desc:
        st.markdown("""
        <div class="weather-card">
            <h4 style="margin:0;color:white;font-weight:700;">🌤 Weather in {}</h4>
            <div style="display:flex;align-items:center;margin-top:10px;">
                <div style="margin-right:15px;">
                    <img src="{}" width="60">
                </div>
                <div>
                    <p style="margin:0;font-size:1.4rem;font-weight:700;">{}°C</p>
                    <p style="margin:0;">{}</p>
                </div>
            </div>
        </div>
        """.format(destination, icon_url, temp, weather_desc), unsafe_allow_html=True)
    else:
        st.markdown("""
        <div style="background-color:#f0f4f9;padding:15px;border-radius:8px;margin-top:20px;text-align:center;">
            <p>⚠️ Weather data not available.</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Generate button
    generate_button = st.button("✨ Generate Itinerary")

# Fetch an image for the destination
def fetch_destination_image(destination):
    if not UNSPLASH_API_KEY:
        return None
    url = f"https://api.unsplash.com/search/photos?query={destination}&client_id={UNSPLASH_API_KEY}&per_page=1"
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise exception for HTTP errors
        if response.json()["results"]:
            return response.json()["results"][0]["urls"]["regular"]
        else:
            st.warning(f"No images found for {destination}")
            return None
    except Exception as e:
        st.warning(f"Failed to fetch image: {e}")
        return None

# Main content area
# Create columns for better layout
col1, col2 = st.columns([2, 1])

with col1:
    # Display destination image with better styling
    image_url = fetch_destination_image(destination)
    if image_url:
        st.image(image_url, caption=f"{destination}", use_container_width=True)
    else:
        st.markdown("""
        <div style="background:linear-gradient(135deg, #e6e9f0 0%, #eef1f5 100%);height:300px;border-radius:12px;display:flex;align-items:center;justify-content:center;">
            <p style="color:#7f8fa4;font-size:1.2rem;">No image available for {}</p>
        </div>
        """.format(destination), unsafe_allow_html=True)

with col2:
    # Function to generate a map with better styling
    def display_map(destination):
        headers = {
            "User-Agent": "AI-Travel-Planner/1.0 (garimaabhayanaa@gmail.com)"
        }
        location_url = f"https://nominatim.openstreetmap.org/search?format=json&q={destination}"
        
        try:
            response = requests.get(location_url, headers=headers)
            
            if response.status_code == 200 and response.json():
                lat = float(response.json()[0]["lat"])
                lon = float(response.json()[0]["lon"])
                
                m = folium.Map(location=[lat, lon], zoom_start=13)
                folium.Marker(
                    [lat, lon],
                    popup=f"<b>{destination}</b>",
                    tooltip=destination,
                    icon=folium.Icon(color="blue", icon="info-sign")
                ).add_to(m)
                
                # Add a circle to highlight the area
                folium.Circle(
                    location=[lat, lon],
                    radius=2000,  # 2km radius
                    color="#3a7bd5",
                    fill=True,
                    fill_color="#3a7bd5",
                    fill_opacity=0.2
                ).add_to(m)
                
                return m
            else:
                st.error(f"Error creating map: {response.status_code} - {response.reason}")
                return None
        except Exception as e:
            st.error(f"Error creating map: {e}")
            return None

    st.markdown('<h3 class="subheader">📍 Destination Map</h3>', unsafe_allow_html=True)
    map_object = display_map(destination)

    if map_object:
        try:
            st_folium(map_object, width=None, height=350)
        except Exception as e:
            st.error(f"Error displaying map: {e}")
    else:
        st.warning("No map to display")

# Generate Itinerary
if generate_button:
    with st.spinner("✨ Generating your perfect itinerary..."):
        # Send user preferences to backend
        user_input = {
            "destination": destination,
            "num_days": num_days,
            "budget": estimated_cost,
            "transport": transport
        }
        
        try:
            response = requests.post(f"{API_URL}/generate", json=user_input, timeout=30)
            
            if response.status_code == 200:
                response_data = response.json()
                # Check if the response contains the itinerary key
                if "itinerary" in response_data:
                    itinerary = response_data["itinerary"] 
                else:
                    itinerary = response_data  # Fallback in case structure changes
                st.session_state["itinerary"] = itinerary
                st.success(" Your itinerary has been successfully generated!")
            else:
                st.error(f"❌ Failed to generate itinerary: {response.status_code} - {response.reason}")
        except Exception as e:
            st.error(f"❌ Error: {str(e)}")

# Display the itinerary with improved styling
if "itinerary" in st.session_state:
    itinerary = st.session_state["itinerary"]

    st.markdown('<h2 class="subheader">✈️ Your Itinerary</h2>', unsafe_allow_html=True)
    
    # Function to generate PDF - Fixed for Unicode support
    def generate_pdf(itinerary):
        pdf = FPDF()
        pdf.set_auto_page_break(auto=True, margin=15)
        pdf.add_page()
        pdf.set_font("Arial", "B", 16)
        pdf.cell(200, 10, f"Travel Itinerary: {destination}", ln=True, align="C")
        pdf.cell(200, 10, f"({num_days} days, {travel_style} style)", ln=True, align="C")
        
        # Add current date
        pdf.set_font("Arial", "", 10)
        current_date = datetime.datetime.now().strftime("%B %d, %Y")
        pdf.cell(200, 10, f"Generated on: {current_date}", ln=True, align="C")
        
        pdf.set_font("Arial", "", 12)
        
        # Helper function to sanitize text for PDF generation
        def sanitize(text):
            if not isinstance(text, str):
                text = str(text)
            # Replace problematic characters with ASCII equivalents
            # Replace bullet point with hyphen to avoid Unicode issues
            text = text.replace("•", "-")
            text = text.replace("'", "'")
            text = text.replace(""", "\"")
            text = text.replace(""", "\"")
            text = text.replace("–", "-")
            text = text.replace("—", "-")
            text = text.replace("…", "...")
            # Replace any other non-ASCII characters
            return "".join(c if ord(c) < 128 else "-" for c in text)
        
        if isinstance(itinerary, list):
            for day in itinerary:
                pdf.ln(10)
                # Handle both string and dictionary days
                if isinstance(day, dict):
                    pdf.set_font("Arial", "B", 14)
                    pdf.cell(200, 10, sanitize(day["day"]), ln=True, align="L")
                    
                    pdf.set_font("Arial", "B", 12)
                    pdf.cell(200, 10, f"Budget: ${sanitize(day.get('budget', 'N/A'))}", ln=True, align="L")
                    pdf.cell(200, 10, f"Transport: {sanitize(day.get('transport', 'N/A'))}", ln=True, align="L")
                    
                    pdf.set_font("Arial", "", 12)
                    pdf.ln(5)
                    if "activities" in day:
                        for activity in day["activities"]:
                            activity_str = f"- {sanitize(activity['time'])}: {sanitize(activity['activity'])}"
                            # Split long lines to fit the width
                            pdf.multi_cell(0, 10, activity_str)
                            pdf.ln(2)
                else:
                    # If day is a string
                    pdf.set_font("Arial", "B", 14)
                    pdf.cell(200, 10, sanitize(str(day)), ln=True, align="L")
        elif isinstance(itinerary, dict):
            for day_key, day_info in itinerary.items():
                pdf.ln(10)
                pdf.set_font("Arial", "B", 14)
                pdf.cell(200, 10, sanitize(day_key), ln=True, align="L")
                
                if isinstance(day_info, dict):
                    pdf.set_font("Arial", "B", 12)
                    pdf.cell(200, 10, f"Budget: ${sanitize(day_info.get('budget', 'N/A'))}", ln=True, align="L")
                    pdf.cell(200, 10, f"Transport: {sanitize(day_info.get('transport', 'N/A'))}", ln=True, align="L")
                    
                    pdf.set_font("Arial", "", 12)
                    pdf.ln(5)
                    if "activities" in day_info:
                        for activity in day_info["activities"]:
                            activity_str = f"- {sanitize(activity['time'])}: {sanitize(activity['activity'])}"
                            # Split long lines to fit the width
                            pdf.multi_cell(0, 10, activity_str)
                            pdf.ln(2)
        
        # Create a BytesIO object to store the PDF
        pdf_output = BytesIO()
        # Get the PDF data
        pdf_data = pdf.output(dest='S')
        # Check the type and ensure we have bytes
        if isinstance(pdf_data, str):
            pdf_bytes = pdf_data.encode('latin-1')
        else:
            pdf_bytes = pdf_data    
        # Write to BytesIO
        pdf_output.write(pdf_bytes)
        # Reset the pointer to the start of the BytesIO object
        pdf_output.seek(0)
        return pdf_output.getvalue()

    # Generate download files
    itinerary_json = json.dumps(itinerary, indent=4)
    
    try:
        itinerary_pdf = generate_pdf(itinerary)
        pdf_error = None
    except Exception as e:
        itinerary_pdf = None
        pdf_error = str(e)
    
    # Download buttons
    st.markdown("""
    <div style="display:flex;justify-content:center;margin:25px 0 35px 0;">
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        st.download_button(
            label=" Download as JSON",
            data=itinerary_json,
            file_name=f"{destination}_itinerary.json",
            mime="application/json",
            use_container_width=True
        )
    with col2:
        if itinerary_pdf:
            st.download_button(
                label=" Download as PDF",
                data=itinerary_pdf,
                file_name=f"{destination}_itinerary.pdf",
                mime="application/pdf",
                use_container_width=True
            )
        else:
            st.error(f"Could not generate PDF: {pdf_error}")
    
    # Display itinerary with improved styling
    if isinstance(itinerary, list):
        # If itinerary is a list of dictionary days
        for day in itinerary:
            if isinstance(day, dict):
                st.markdown(f'''
                <div class="day-header"><h3>{day["day"]}</h3></div>
                <div class="card">
                    <div class="col-md-6">
                        <p><strong> Budget:</strong> ${day.get('budget', 'N/A')}</p>
                    </div>
                    <div class="col-md-6">
                        <p><strong> Transport:</strong> {day.get('transport', 'N/A')}</p>
                    </div>
                </div>
                ''', unsafe_allow_html=True)
                if "activities" in day and isinstance(day["activities"], list):
                    for activity in day["activities"]:
                        st.markdown(f"""
                        <div class="activity-item">
                            <strong>{activity['time']}</strong>: {activity['activity']}
                        </div>
                        """, unsafe_allow_html=True)
            elif isinstance(day, str):
                # If day is just a string
                st.markdown(f'<div class="day-header"><h3>{day}</h3></div>', unsafe_allow_html=True)
    elif isinstance(itinerary, dict):
        # If itinerary is a dictionary with days as keys
        for day_key, day_info in itinerary.items():
            st.markdown(f'<div class="day-header"><h3>{day_key}</h3></div>', unsafe_allow_html=True)
            
            if isinstance(day_info, dict):
                col1, col2 = st.columns(2)
                with col1:
                    st.markdown(f"** Budget:** ${day_info.get('budget', 'N/A')}")
                with col2:
                    st.markdown(f"** Transport:** {day_info.get('transport', 'N/A')}")
                
                st.markdown('<div class="card">', unsafe_allow_html=True)
                if "activities" in day_info and isinstance(day_info["activities"], list):
                    for activity in day_info["activities"]:
                        st.markdown(f"""
                        <div class="activity-item">
                            <strong>{activity['time']}</strong>: {activity['activity']}
                        </div>
                        """, unsafe_allow_html=True)
                st.markdown('</div>', unsafe_allow_html=True)

# AI Travel Assistant with improved styling
st.markdown('<h2 class="subheader">AI Travel Assistant</h2>', unsafe_allow_html=True)

st.markdown("""
<div class="info-box">
    <h4 style="margin-top:0;color:white;font-weight:600;">Need travel advice?</h4>
    <p style="margin-bottom:0;">Ask me anything about your destination, travel tips, or local attractions!</p>
</div>
""", unsafe_allow_html=True)

def ask_gemini(question):
    try:
        model = genai.GenerativeModel("gemini-2.0-flash")  
        response = model.generate_content(question)
        return response.text.strip()
    except Exception as e:
        return f"⚠️ Error: {str(e)}"

# Create two columns for input and button
col1, col2 = st.columns([3, 1])
with col1:
    user_query = st.text_input("Ask me anything about your trip:", placeholder="E.g., What's the best time to visit the Eiffel Tower?")
with col2:
    ask_button = st.button("Ask", use_container_width=True)

# Process the query
if ask_button:
    if user_query:
        with st.spinner("Thinking..."):
            response = ask_gemini(user_query)
            
            st.markdown("""
            <div class="card" style="margin-top:20px;">
                <h4 style="margin-top:0;color:#3a7bd5;font-weight:600;">AI's Response:</h4>
                <div style="background-color:#f8faff;padding:16px;border-radius:8px;margin-top:10px;border-left:4px solid #3a7bd5;">
            """, unsafe_allow_html=True)
            
            st.write(response)
            
            st.markdown("</div></div>", unsafe_allow_html=True)
    else:
        st.warning("⚠️ Please enter a question.")

# Footer
st.markdown("""
<div class="footer">
    <p>WanderAI | Plan your perfect trip with AI</p>
</div>
""", unsafe_allow_html=True)
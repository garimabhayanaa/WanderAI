# Import necessary libraries
from flask import Flask, request, jsonify
import json
import re
import requests
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize Flask app
app = Flask(__name__)

@app.route('/')
def home():
    return "Backend is running!"
    
# Load existing itinerary
@app.route('/api/itinerary', methods=['GET'])
def get_itinerary():
    try:
        with open("itinerary.json", "r", encoding="utf-8") as file:
            itinerary_data = json.load(file)
        return jsonify(itinerary_data)
    except FileNotFoundError:
        return jsonify({"error": "Itinerary file not found"}), 404

# Function to call Gemini API using requests
def generate_content(prompt):
    api_key = os.getenv('GEMINI_API_KEY')
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={api_key}"
    
    # Prepare the request payload according to the API documentation
    payload = {
        "contents": [{
            "parts": [{"text": prompt}]
        }]
    }
    
    headers = {
        'Content-Type': 'application/json'
    }
    
    # Make the API request
    response = requests.post(url, headers=headers, json=payload)
    
    # Check if the request was successful
    if response.status_code == 200:
        return response.json()
    else:
        print(f"API Error: Status {response.status_code}")
        print(f"Response: {response.text}")
        raise Exception(f"API request failed with status {response.status_code}: {response.text}")

# Helper function to parse the text response into JSON
def parse_itinerary_to_json(text):
    try:
        # Find JSON content (it might be surrounded by markdown code blocks)
        json_match = re.search(r'```json\s*([\s\S]*?)\s*```', text)
        if json_match:
            json_text = json_match.group(1)
        else:
            # If not in code blocks, try to find array directly
            json_match = re.search(r'\[\s*{[\s\S]*}\s*\]', text)
            if json_match:
                json_text = json_match.group(0)
            else:
                # If no clear JSON pattern, try the whole text
                json_text = text
                
        # Clean up the text
        json_text = json_text.strip()
        
        # Parse JSON
        itinerary = json.loads(json_text)
        
        # Validate the itinerary format
        if isinstance(itinerary, list):
            # Fix any day numbering issues
            for i, day in enumerate(itinerary):
                if "day" not in day:
                    day["day"] = f"Day {i+1}"
                elif day["day"] == "Day 0":  # Fix "Day 0" issue
                    day["day"] = f"Day {i+1}"
                
                if "activities" not in day:
                    day["activities"] = []
                    
            return itinerary
        else:
            raise ValueError("Itinerary is not a list")
            
    except Exception as e:
        print(f"JSON parsing error: {e}")
        print(f"Raw text: {text}")
        raise ValueError(f"Failed to parse itinerary JSON: {str(e)}")

@app.route('/api/itinerary/generate', methods=['POST'])
def generate_itinerary():
    try:
        data = request.json
        destination = data.get('destination')
        num_days = data.get('num_days')
        budget = data.get('budget')
        transport = data.get('transport')
        
        # Generate prompt
        prompt = f"""Generate a detailed {num_days}-day travel itinerary for {destination} with a {budget} budget, using {transport}.

        Return ONLY a valid JSON array with the following structure. DO NOT include any explanations, markdown formatting, or text outside the JSON:
        [
        {{
            "day": "Day 1",
            "activities": [
            {{
                "time": "Morning",
                "activity": "Description of morning activity"
            }},
            {{
                "time": "Afternoon", 
                "activity": "Description of afternoon activity"
            }},
            {{
                "time": "Evening",
                "activity": "Description of evening activity"
            }}
            ],
            "budget": "$X per day",
            "transport": "Modes of transport for this day"
        }}
        ]

        IMPORTANT:
        - Return ONLY the JSON array, no other text
        - Format days as "Day 1", "Day 2", etc. (NOT "Day 0")
        - Include at least 3 activities per day
        - The response must be valid JSON that can be parsed with json.loads()
        """

        print(f"Sending prompt to Gemini API")
        
        # Call Gemini API
        result = generate_content(prompt)
        
        # Process the response - extract text from the Gemini 2.0 response format
        try:
            # Extract text from Gemini 2.0 response format
            text_response = result["candidates"][0]["content"]["parts"][0]["text"]
            print("Raw API response:", text_response)  # Debugging
            
            itinerary_json = parse_itinerary_to_json(text_response)
            print("Parsed JSON:", itinerary_json)  # Debugging
            
            # Save the itinerary to a file (for debugging)
            with open('itinerary.json', 'w') as f:
                json.dump(itinerary_json, f, indent=2)
                
            return jsonify({"itinerary": itinerary_json})
            
        except Exception as e:
            print(f"Error processing API response: {e}")
            print(f"Response structure: {json.dumps(result, indent=2)}")
            return jsonify({"error": f"Failed to process itinerary: {str(e)}"}), 500
            
    except Exception as e:
        print(f"Error generating itinerary: {e}")
        return jsonify({"error": f"Failed to generate itinerary: {str(e)}"}), 500

# Run the Flask app
if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))  
    app.run(host="0.0.0.0", port=port, debug=True)  

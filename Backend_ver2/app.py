import requests
from flask import Flask, request, jsonify
import mysql.connector
from db_config import DB_CONFIG
from werkzeug.security import generate_password_hash, check_password_hash
import pickle
import numpy as np
import os
from datetime import datetime

def get_db():
    return mysql.connector.connect(**DB_CONFIG)

app = Flask(__name__)
# WARNING: Replace with a secure key management system in production
OPENWEATHER_API_KEY = "6d708c6c2b815be9da1c818e9468c7fc"

MODEL_PATH = "crop_yield_model.pkl"
crop_yield_model = None
if os.path.exists(MODEL_PATH):
    with open(MODEL_PATH, "rb") as f:
        crop_yield_model = pickle.load(f)

# --- STANDARD API ENDPOINTS ---
@app.route('/register', methods=['POST'])
def register():
    data = request.json
    email = data.get('email')
    password = data.get('password')
    name = data.get('name', '')
    if not email or not password:
        return jsonify({'message': 'Email and password required.'}), 400

    hashed_pw = generate_password_hash(password)
    conn = get_db()
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute("SELECT id FROM users WHERE email=%s", (email,))
        if cursor.fetchone():
            return jsonify({'message': 'User already exists.'}), 400
        cursor.execute("INSERT INTO users (email, password, name) VALUES (%s, %s, %s)", (email, hashed_pw, name))
        conn.commit()
        return jsonify({'message': 'User registered successfully.'})
    finally:
        cursor.close()
        conn.close()

@app.route('/login', methods=['POST'])
def login():
    data = request.json
    email = data.get('email')
    password = data.get('password')
    if not email or not password:
        return jsonify({'message': 'Email and password required.'}), 400

    conn = get_db()
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute("SELECT id, password FROM users WHERE email=%s", (email,))
        user = cursor.fetchone()
        if user and check_password_hash(user['password'], password):
            return jsonify({'message': 'Login successful.', 'user_id': user['id']})
        else:
            return jsonify({'message': 'Invalid credentials.'}), 401
    finally:
        cursor.close()
        conn.close()

@app.route('/farm', methods=['POST'])
def create_farm():
    data = request.json
    user_id = data.get('user_id')
    location = data.get('location')  # city name or "lat,lon"
    crop_type = data.get('crop_type')
    area = data.get('area')
    soil_type = data.get('soil_type', '')
    irrigation_method = data.get('irrigation_method', '')
    if not all([user_id, location, crop_type, area]):
        return jsonify({'message': 'Missing required fields.'}), 400

    conn = get_db()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "INSERT INTO farms (user_id, location, crop_type, area, soil_type, irrigation_method) VALUES (%s, %s, %s, %s, %s, %s)",
            (user_id, location, crop_type, area, soil_type, irrigation_method)
        )
        conn.commit()
        return jsonify({'message': 'Farm profile added.', 'farm_id': cursor.lastrowid})
    finally:
        cursor.close()
        conn.close()

def fetch_weather_by_location(location):
    """
    Fetch weather data from OpenWeatherMap for a given location string (city name or 'lat,lon').
    """
    if ',' in location and all(part.replace('.', '', 1).replace('-', '', 1).isdigit() for part in location.split(',')):
        lat, lon = location.split(',')
        url = f"http://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={OPENWEATHER_API_KEY}&units=metric"
    else:
        url = f"http://api.openweathermap.org/data/2.5/weather?q={location}&appid={OPENWEATHER_API_KEY}&units=metric"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return {
            "temperature": data["main"]["temp"],
            "humidity": data["main"]["humidity"],
            "weather_desc": data["weather"][0]["description"]
        }
    else:
        return None

@app.route('/soil_data', methods=['POST'])
def record_soil_data():
    data = request.json
    farm_id = data.get('farm_id')
    N = data.get('nitrogen_ppm')
    P = data.get('phosphorus_ppm')
    K = data.get('potassium_ppm')
    pH = data.get('ph_level')

    if None in [farm_id, N, P, K, pH]:
        return jsonify({'message': 'Missing farm_id or soil NPK/pH data.'}), 400

    conn = get_db()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "INSERT INTO soil_data (farm_id, nitrogen_ppm, phosphorus_ppm, potassium_ppm, ph_level, test_date) VALUES (%s, %s, %s, %s, %s, CURDATE())",
            (farm_id, N, P, K, pH)
        )
        conn.commit()
        return jsonify({'message': 'Soil data recorded successfully.'})
    finally:
        cursor.close()
        conn.close()

# --- New function to fetch soil data from the open SoilGrids API ---
def fetch_soil_data_from_api(lat, lon):
    """
    Fetches location-specific soil data (N, P, K, pH) from the open SoilGrids API.
    """
    SOIL_API_URL = f"https://rest.isric.org/soilgrids/v2.0/properties/query?lon={lon}&lat={lat}&properties=nitrogen,phosphorus,potassium,phh2o&depths=0-30cm&values=mean"
    
    try:
        response = requests.get(SOIL_API_URL, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        # --- CRUCIAL: Extracting and mapping data from the JSON response ---
        nitrogen_value = data['properties']['layers'][0]['depths'][0]['values']['mean']
        phosphorus_value = data['properties']['layers'][1]['depths'][0]['values']['mean']
        potassium_value = data['properties']['layers'][2]['depths'][0]['values']['mean']
        ph_value = data['properties']['layers'][3]['depths'][0]['values']['mean']
        
        return {
            "nitrogen_ppm": nitrogen_value * 10,
            "phosphorus_ppm": phosphorus_value,
            "potassium_ppm": potassium_value,
            "ph_level": ph_value / 10
        }
    except requests.exceptions.RequestException as e:
        print(f"SoilGrids API call failed for {lat},{lon}: {e}")
        return {'nitrogen_ppm': 70, 'phosphorus_ppm': 20, 'potassium_ppm': 150, 'ph_level': 6.5}

# --- OPTIMIZATION LOGIC ---
def generate_recommendations(crop_type, current_weather, soil_data, predicted_yield):
    """
    Generates actionable recommendations based on simple heuristics/rules.
    """
    irrigation_advice = "Monitor soil moisture regularly."
    fertilizer_advice = "Standard fertilization schedule."
    pest_control_advice = "Scout the field for signs of infestation."

    temp = current_weather['temperature']
    humidity = current_weather['humidity']
    N = soil_data.get('nitrogen_ppm', 0)
    P = soil_data.get('phosphorus_ppm', 0)
    K = soil_data.get('potassium_ppm', 0)
    pH = soil_data.get('ph_level', 7.0)

    # Rule 1: Irrigation Optimization based on weather and yield
    if predicted_yield < 2.0 and temp > 30: # Assuming 2.0 is a target yield
        irrigation_advice = "Increase irrigation frequency slightly to compensate for high heat and maximize potential yield."
    elif humidity > 75 and temp < 20:
        irrigation_advice = "Reduce irrigation frequency to prevent root rot and disease."

    # Rule 2: Fertilization Optimization based on NPK
    if crop_type in ['Wheat', 'Maize']:
        if N < 50:
            fertilizer_advice = f"Nitrogen (N) is critically low ({N} ppm). Apply a top-dressing of 50-75 kg/ha Urea immediately."
        elif P < 10:
             fertilizer_advice = f"Phosphorus (P) is low ({P} ppm). Consider a P-rich supplement during the next application."
        elif K < 100 and predicted_yield > 2.5:
             fertilizer_advice = f"Potassium (K) is marginal ({K} ppm). A boost may help improve grain filling for high yields."
        else:
             fertilizer_advice = "Soil nutrients are adequate for the current growth stage."

    # Rule 3: Pest Control based on environmental risk
    if humidity > 80 and temp > 25:
        pest_control_advice = "High humidity and temperature increase fungal/pest risk. Monitor for rust or blight and consider preventative fungicide."
    elif predicted_yield < 1.0:
        pest_control_advice = "Yield is low. Immediately inspect for severe pest/disease damage."

    return {
        "irrigation_advice": irrigation_advice,
        "fertilizer_advice": fertilizer_advice,
        "pest_control_advice": pest_control_advice
    }

# --- Core Endpoint: Predict and Optimize (Full Workflow) ---
@app.route('/optimize_farm', methods=['POST'])
def optimize_farm():
    if crop_yield_model is None:
        return jsonify({'message': 'ML model not available'}), 500

    data = request.json
    farm_id = data.get('farm_id')

    if not farm_id:
        return jsonify({'message': 'farm_id is required'}), 400

    conn = get_db()
    cursor = conn.cursor(dictionary=True)
    try:
        # 1. Fetch Farm, Weather, and Soil Data
        cursor.execute("SELECT location, crop_type, area FROM farms WHERE id=%s", (farm_id,))
        farm = cursor.fetchone()
        if not farm: return jsonify({'message': 'Farm not found'}), 404

        weather = fetch_weather_by_location(farm['location'])
        if not weather: return jsonify({'message': 'Weather data not found'}), 404

        # --- Hybrid Soil Data Strategy: Manual Override -> API -> Default ---
        soil_data = None
        
        # A. Attempt 1: Get latest manual soil data (farmer's lab report)
        cursor.execute("SELECT nitrogen_ppm, phosphorus_ppm, potassium_ppm, ph_level FROM soil_data WHERE farm_id=%s ORDER BY test_date DESC LIMIT 1", (farm_id,))
        manual_soil_data = cursor.fetchone()
        
        if manual_soil_data:
            soil_data = dict(manual_soil_data)
        else:
            # B. Attempt 2: If no manual data, use API via Lat/Lon
            location_parts = farm['location'].split(',')
            
            if len(location_parts) == 2:
                lat = location_parts[0]
                lon = location_parts[1]
                
                api_soil_data = fetch_soil_data_from_api(lat, lon)
                soil_data = api_soil_data
                
            else:
                # C. Attempt 3: If location is not Lat/Lon, use final defaults
                soil_data = {'nitrogen_ppm': 70, 'phosphorus_ppm': 20, 'potassium_ppm': 150, 'ph_level': 6.5}

        # 2. Predict Yield (Assumes 4 features: area, temp, humidity, N)
        features = np.array([[
            farm['area'],
            weather['temperature'],
            weather['humidity'],
            soil_data['nitrogen_ppm']
        ]])
        
        if features.shape[1] != crop_yield_model.n_features_in_:
             return jsonify({'message': f'Model expects {crop_yield_model.n_features_in_} features, but got {features.shape[1]}. Check model training and feature inputs.'}), 500

        predicted_yield = float(crop_yield_model.predict(features)[0])

        # 3. Generate Actionable Recommendations
        recommendations = generate_recommendations(farm['crop_type'], weather, soil_data, predicted_yield)

        # 4. Store Recommendations
        cursor.execute(
            "INSERT INTO recommendations (farm_id, predicted_yield, irrigation_advice, fertilizer_advice, pest_control_advice) VALUES (%s, %s, %s, %s, %s)",
            (farm_id, predicted_yield, recommendations['irrigation_advice'], recommendations['fertilizer_advice'], recommendations['pest_control_advice'])
        )
        conn.commit()

        # 5. Return Full Insight
        return jsonify({
            'message': 'Prediction and Optimization successful.',
            'predicted_yield': predicted_yield,
            'current_weather': weather,
            'soil_data': soil_data,
            'recommendations': recommendations
        })
    finally:
        cursor.close()
        conn.close()

if __name__ == '__main__':
    app.run(debug=True)

# Crop Yield Platform Backend (Python + MySQL + ML)

## Features

- User registration & login (`/register`, `/login`)
- Farm profile creation (`/farm`)
- Fetch and store weather for a farm (`/fetch_weather`)
- ML model yield prediction (`/predict_yield`)
- MySQL database

## Setup

1. **Install Python dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Set up MySQL:**
   - Run the contents of `mysql_schema.sql` in your MySQL client to create the database and tables.
   - Edit `db_config.py` with your MySQL username and password.

3. **Get your OpenWeatherMap API key:**
   - [Sign up here](https://openweathermap.org/api) and put the key in `app.py` as `OPENWEATHER_API_KEY`.

4. **Train a dummy ML model (to create crop_yield_model.pkl):**
   ```bash
   python train_model.py
   ```

5. **Run the Flask server:**
   ```bash
   python app.py
   ```

## API Endpoints

### Register

- **POST** `/register`
- Body: `{ "email": "...", "password": "...", "name": "..." }`

### Login

- **POST** `/login`
- Body: `{ "email": "...", "password": "..." }`

### Create Farm

- **POST** `/farm`
- Body: `{ "user_id": ..., "location": "...", "crop_type": "...", "area": ..., "soil_type": "...", "irrigation_method": "..." }`
- `location` can be a city name or `"lat,lon"` (e.g., `"28.6139,77.2090"`)

### Fetch and Store Weather for a Farm

- **POST** `/fetch_weather`
- Body: `{ "farm_id": ... }`
- Uses the farm's location to fetch weather from OpenWeatherMap and store it in `weather_data`.

### Predict Crop Yield

- **POST** `/predict_yield`
- Body: `{ "area": ..., "temperature": ..., "humidity": ... }`
- Returns: `{ "predicted_yield": ... }`

---

You can now build your website frontend to connect to these endpoints!

If you want more features or have any questions, just ask!
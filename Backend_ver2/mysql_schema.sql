-- 1. Create the Database (if it doesn't exist)
CREATE DATABASE IF NOT EXISTS crop_db;
USE crop_db;

-- 2. Users Table (for authentication and profile)
CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    email VARCHAR(120) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    name VARCHAR(80)
);

-- 3. Farms Table (stores farm-specific data and location)
CREATE TABLE IF NOT EXISTS farms (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    location VARCHAR(120),
    crop_type VARCHAR(80),
    area FLOAT,
    soil_type VARCHAR(80),
    irrigation_method VARCHAR(80),
    FOREIGN KEY (user_id) REFERENCES users(id)
);

-- 4. Weather Data Table (stores real-time weather snapshots)
CREATE TABLE IF NOT EXISTS weather_data (
    id INT AUTO_INCREMENT PRIMARY KEY,
    farm_id INT,
    temperature FLOAT,
    humidity FLOAT,
    weather_desc VARCHAR(120),
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (farm_id) REFERENCES farms(id)
);

-- 5. Soil Health Data Table (NEW: stores manual soil test results / API fetch data)
CREATE TABLE IF NOT EXISTS soil_data (
    id INT AUTO_INCREMENT PRIMARY KEY,
    farm_id INT NOT NULL,
    nitrogen_ppm FLOAT,
    phosphorus_ppm FLOAT,
    potassium_ppm FLOAT,
    ph_level FLOAT,
    test_date DATE,
    FOREIGN KEY (farm_id) REFERENCES farms(id)
);

-- 6. Recommendations Table (NEW: stores ML prediction and prescriptive advice)
CREATE TABLE IF NOT EXISTS recommendations (
    id INT AUTO_INCREMENT PRIMARY KEY,
    farm_id INT NOT NULL,
    predicted_yield FLOAT,
    irrigation_advice VARCHAR(255),
    fertilizer_advice VARCHAR(255),
    pest_control_advice VARCHAR(255),
    generated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (farm_id) REFERENCES farms(id)
);
select * from recommendations;
select * from soil_data;
select * from weather_data;
select * from farms;
select * from users;

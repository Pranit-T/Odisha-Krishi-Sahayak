import numpy as np
from sklearn.linear_model import LinearRegression
import pickle

# Dummy data: [area, temperature, humidity, nitrogen_ppm, phosphorus_ppm, potassium_ppm, ph_level], yield
X = np.array([
    [1.5, 25, 70, 60, 15, 120, 6.5],
    [2.0, 27, 65, 80, 25, 150, 7.0],
    [1.0, 23, 80, 20, 5, 80, 5.5],
    [2.5, 30, 60, 50, 20, 100, 6.0],
    [1.8, 26, 72, 70, 22, 130, 6.8]
])
y = np.array([2.0, 2.5, 1.2, 3.0, 2.2])

model = LinearRegression()
model.fit(X, y)

# *** CHANGE MADE HERE ***
with open('crop_yield_model_new.pkl', 'wb') as f:
    pickle.dump(model, f)

# *** CHANGE MADE HERE ***
print("Trained dummy crop yield model with 7 features (area, temp, humidity, N, P, K, pH) and saved to crop_yield_model_new.pkl")
import numpy as np
from sklearn.linear_model import LinearRegression
import pickle

# Dummy data: [area, temperature, humidity, nitrogen_ppm], yield
X = np.array([
    [1.5, 25, 70, 60],
    [2.0, 27, 65, 80],
    [1.0, 23, 80, 20],
    [2.5, 30, 60, 50]
])
y = np.array([2.0, 2.5, 1.2, 3.0])

model = LinearRegression()
model.fit(X, y)

with open('crop_yield_model.pkl', 'wb') as f:
    pickle.dump(model, f)

print("Trained dummy crop yield model with 4 features (area, temp, humidity, N) and saved to crop_yield_model.pkl")
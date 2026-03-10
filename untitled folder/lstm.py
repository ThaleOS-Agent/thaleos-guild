from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense
import numpy as np

def train_lstm_model(data):
    X = np.array([data[i:i+5] for i in range(len(data)-5)])
    y = np.array([data[i+5] for i in range(len(data)-5)])
    model = Sequential([
        LSTM(50, activation='relu', input_shape=(5,1)),
        Dense(1)
    ])
    model.compile(optimizer='adam', loss='mse')
    model.fit(X, y, epochs=100, verbose=0)
    return model

# Example usage:
historical_data = [100, 110, 115, 120, 130, 140, 150, 160, 170]
model = train_lstm_model(historical_data)
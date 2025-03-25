import numpy as np
import pandas as pd
import tensorflow as tf
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Dropout

# Load data transaksi (dummy data)
def load_transaction_data():
    data = {
        "timestamp": pd.date_range(start="2025-01-01", periods=500, freq="H"),
        "amount": np.random.uniform(1, 1000, 500),
        "fee": np.random.uniform(0.1, 5, 500),
        "balance": np.cumsum(np.random.uniform(-50, 50, 500))
    }
    df = pd.DataFrame(data)
    return df

# **1. Deteksi Anomali Transaksi dengan Isolation Forest**
def detect_anomalies(df):
    model = IsolationForest(n_estimators=100, contamination=0.05, random_state=42)
    df["anomaly"] = model.fit_predict(df[["amount", "fee", "balance"]])
    return df

# **2. Prediksi Tren Keuangan dengan LSTM**
def prepare_lstm_data(df):
    scaler = MinMaxScaler()
    df_scaled = scaler.fit_transform(df[["balance"]])
    
    X, y = [], []
    for i in range(len(df_scaled) - 10):
        X.append(df_scaled[i:i+10])
        y.append(df_scaled[i+10])
    
    return np.array(X), np.array(y), scaler

def build_lstm_model():
    model = Sequential([
        LSTM(50, activation='relu', return_sequences=True, input_shape=(10, 1)),
        Dropout(0.2),
        LSTM(50, activation='relu'),
        Dropout(0.2),
        Dense(1)
    ])
    model.compile(optimizer='adam', loss='mse')
    return model

# **3. Rekomendasi Strategi Transaksi**
def transaction_recommendation(df):
    avg_fee = df["fee"].mean()
    if df["balance"].iloc[-1] < 100:
        return "Saldo rendah! Kurangi transaksi besar."
    elif avg_fee > 2:
        return "Biaya transaksi tinggi. Gunakan strategi batch processing."
    else:
        return "Transaksi dalam batas normal."

# **Menjalankan Model**
df = load_transaction_data()
df = detect_anomalies(df)

X, y, scaler = prepare_lstm_data(df)
model = build_lstm_model()

# **Latih Model**
model.fit(X, y, epochs=10, batch_size=16, verbose=1)

# **Prediksi Tren Masa Depan**
future_balance = model.predict(X[-1].reshape(1, 10, 1))
future_balance = scaler.inverse_transform(future_balance.reshape(-1, 1))

# **Output Analisis**
print("\n🔍 Anomali yang terdeteksi:", df[df["anomaly"] == -1][["timestamp", "amount", "fee"]])
print("\n📈 Prediksi saldo keuangan selanjutnya:", future_balance[0][0])
print("\n✅ Rekomendasi transaksi:", transaction_recommendation(df))

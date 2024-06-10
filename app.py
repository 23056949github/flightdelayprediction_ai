import streamlit as st
import numpy as np
import pandas as pd
import pickle
from sklearn.ensemble import RandomForestClassifier

# Load the pre-trained models and encoders
scaler = pickle.load(open('scaler.sav', 'rb'))
rf_model = pickle.load(open('rf_model.sav', 'rb'))
encoder = pickle.load(open('encoder.sav', 'rb'))

# Title
st.title("Flight Delay Detection")

# Sidebar for user input
st.sidebar.header("Flight Information")

# Function to get user input
def get_user_input():
    airline = st.sidebar.selectbox("Airline", ["Airline A", "Airline B", "Airline C"])
    origin = st.sidebar.selectbox("Origin", ["JFK", "LAX", "SFO"])
    destination = st.sidebar.selectbox("Destination", ["JFK", "LAX", "SFO"])
    departure_time = st.sidebar.slider("Departure Time (24-hour)", 0, 23, 12)
    
    # Encoding categorical features
    airline_encoded = encoder.transform([[airline]]).toarray()[0]
    origin_encoded = encoder.transform([[origin]]).toarray()[0]
    destination_encoded = encoder.transform([[destination]]).toarray()[0]
    
    # Create a dictionary of inputs
    data = {
        "Airline": airline_encoded,
        "Origin": origin_encoded,
        "Destination": destination_encoded,
        "Departure Time": departure_time
    }
    
    features = pd.DataFrame(data, index=[0])
    return features

# Get user input
user_input = get_user_input()

# Scale input
scaled_input = scaler.transform(user_input)

# Prediction
prediction = rf_model.predict(scaled_input)
prediction_proba = rf_model.predict_proba(scaled_input)

# Display prediction
st.subheader("Prediction")
delay_status = "Delayed" if prediction == 1 else "On Time"
st.write(f"The flight is predicted to be: **{delay_status}**")

# Display prediction probability
st.subheader("Prediction Probability")
st.write(f"Probability of delay: {prediction_proba[0][1]:.2f}")
st.write(f"Probability of on-time: {prediction_proba[0][0]:.2f}")

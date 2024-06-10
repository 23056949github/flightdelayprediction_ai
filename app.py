import streamlit as st
import pandas as pd
import pickle
from sklearn.preprocessing import StandardScaler

# Load the models and encoders
scaler = pickle.load(open('scaler.sav', 'rb'))
airline_encoder = pickle.load(open('airline_encoder.sav', 'rb'))
origin_encoder = pickle.load(open('origin_encoder.sav', 'rb'))
destination_encoder = pickle.load(open('destination_encoder.sav', 'rb'))
model = pickle.load(open('rf_model.sav', 'rb'))

# Define the Streamlit app
st.title('Flight Delay Prediction')

# Input features for prediction
st.sidebar.header('Flight Information')
airline = st.sidebar.selectbox('Airline', ['Airline1', 'Airline2', 'Airline3'])
origin = st.sidebar.selectbox('Origin', ['Origin1', 'Origin2', 'Origin3'])
destination = st.sidebar.selectbox('Destination', ['Destination1', 'Destination2', 'Destination3'])
departure_time = st.sidebar.slider('Departure Time', 0, 23, 12)
arrival_time = st.sidebar.slider('Arrival Time', 0, 23, 14)

# Create DataFrame from inputs
input_data = pd.DataFrame({
    'airline': [airline],
    'origin': [origin],
    'destination': [destination],
    'departure_time': [departure_time],
    'arrival_time': [arrival_time]
})

# Encode and scale the data
input_data['airline'] = airline_encoder.transform(input_data['airline'])
input_data['origin'] = origin_encoder.transform(input_data['origin'])
input_data['destination'] = destination_encoder.transform(input_data['destination'])
input_data = scaler.transform(input_data)

# Make predictions
prediction = model.predict(input_data)
probability = model.predict_proba(input_data)

# Display results
st.write(f'Prediction: {"Delayed" if prediction[0] else "On Time"}')
st.write(f'Probability of Delay: {probability[0][1]:.2f}')

if st.checkbox('Show input data'):
    st.write(input_data)

import os
import pickle
import streamlit as st
import pandas as pd
from PIL import Image

# Set page configuration
st.set_page_config(page_title="Metaverse Fraud Analysis",
                   layout="wide",
                   page_icon="🔐")


# Load the saved models
with open('rf_model.sav', 'rb') as model_file:
    model = pickle.load(model_file)
with open('scaler.sav', 'rb') as scaler_file:
    scaler = pickle.load(scaler_file)
with open('encoder.sav', 'rb') as encoder_file:
    encoder_columns = pickle.load(encoder_file)

# Define the title text
title_text = "Metaverse Fraud Detection"

# Define the background color and text color of the title box
background_color = "#23395d"
box_background_color = "#23395d"
text_color = "#ffffff"

# Apply HTML and CSS to style the title
title_html = f"""
    <div style="background-color:{box_background_color};padding:8px;border-radius:10px;">
        <h1 style="color:{text_color};text-align:center;">{title_text}</h1>
    </div>
    <body>
      <br>
        <center>Welcome! We're here to safeguard the integrity of virtual worlds and ensure a fraud-free experience.</center>
    </body>
"""

# Display the styled title using markdown
st.markdown(title_html, unsafe_allow_html=True)

# Getting the input data from the user
col1, col2 = st.columns(2)

with col1:
    time_category = st.selectbox('Departure Time',('before 6am', '6am to 11.59pm', '12pm to 6pm','after 6pm'))
with col2:
    amount = st.number_input('Flight Number')
with col1:
    transaction_type = st.selectbox('Day of the Week', ('Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'))
with col2:
    session_duration = st.number_input('Flight Time (minutes)')
with col1:
    location_region = st.selectbox('Flight Region', ('Africa', 'Asia', 'Europe', 'North America', 'South America'))
with col2:
    login_frequency = st.number_input('Login Frequency',step=1)
with col2:
    ip_prefix = st.selectbox('IP Prefix', ('10.0', '172.0', '172.16', '192.0', '192.168'))
with col1:
    purchase_pattern = st.selectbox('Departure Airport Traffic', ('Low', 'Medium', 'High'))
with col2:
    age_group = st.selectbox('Arrival Airport Traffic', ('Low', 'Medium', 'High'))

# Code for Prediction
if st.button('Predict Risk'):
    # Create a DataFrame with input data
    input_data = pd.DataFrame({
        'amount': [amount],
        'login_frequency': [login_frequency],
        'session_duration': [session_duration],
        'risk_score': [risk_score],
        'time_category': [time_category],
        'transaction_type': [transaction_type],
        'location_region': [location_region],
        'ip_prefix': [ip_prefix],
        'purchase_pattern': [purchase_pattern],
        'age_group': [age_group]
    })

    # Perform one-hot encoding using pd.get_dummies
    input_data_encoded = pd.get_dummies(input_data[['time_category','transaction_type', 'location_region', 'ip_prefix', 'purchase_pattern', 'age_group']], dtype=int)

    # Scale the numerical features
    numerical_features = ['amount', 'login_frequency', 'session_duration', 'risk_score']
    input_data_scaled = scaler.transform(input_data[numerical_features])
    input_data_scaled = pd.DataFrame(input_data_scaled, columns=numerical_features)
    
    # Concatenate encoded categorical features and standardized numerical features
    input_data = pd.concat([input_data_encoded.reset_index(drop=True), input_data_scaled.reset_index(drop=True)],axis=1)

    # Reorder columns to match the sequence of features used during model training
    input_data = input_data.reindex(columns=encoder_columns, fill_value=0)

    # Make the prediction
    prediction = model.predict(input_data)

    # Select Probability of Delay Output

    if prediction[0] == '0':
        st.success('There is a Low Probability of Delay.')
    elif prediction[0] == '1':
        st.warning('There is a Moderate Probability of Delay.')
    elif prediction[0] == '2':
        st.error('There is a High Probability of Delay.')

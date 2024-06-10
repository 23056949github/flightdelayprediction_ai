import os
import pickle
import streamlit as st
import pandas as pd
from PIL import Image

# Set page configuration
st.set_page_config(page_title="Flight Delay Prediction",
                   layout="wide",
                   page_icon="✈️")

# Define paths for the model files
model_path = 'rf_model.sav'

# Function to load a pickle file and handle errors
def load_pickle(file_path):
    try:
        with open(file_path, 'rb') as file:
            return pickle.load(file)
    except FileNotFoundError:
        st.error(f"File not found: {file_path}")
        return None
    except Exception as e:
        st.error(f"An error occurred while loading {file_path}: {e}")
        return None

# Load the saved model
model = load_pickle(model_path)

# Manually define the encoder columns
encoder_columns = ['time_category_before 6am', 'time_category_6am to 11:59am', 'time_category_12pm to 6pm', 'time_category_after 6pm']

if model is None:
    st.stop()  # Stop execution if the model is not loaded properly

# Define the title text
title_text = "Flight Delay Prediction"

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
        <center>Welcome! We're here to help predict your flight delays.</center>
    </body>
"""

# Display the styled title using markdown
st.markdown(title_html, unsafe_allow_html=True)

# Getting the input data from the user
col1, col2 = st.columns(2)

# Actual input for prediction
with col1:
    time_category = st.selectbox('Departure Time', ('before 6am', '6am to 11:59am', '12pm to 6pm', 'after 6pm'))

# Dummy inputs for display purposes
with col2:
    st.number_input('Flight Number')
with col1:
    st.selectbox('Day of the Week', ('Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'))
with col2:
    st.number_input('Flight Time (minutes)')
with col1:
    st.selectbox('Flight Region', ('Africa', 'Asia', 'Europe', 'North America', 'South America'))
with col2:
    st.number_input('Login Frequency', step=1)
with col2:
    st.selectbox('IP Prefix', ('10.0', '172.0', '172.16', '192.0', '192.168'))
with col1:
    st.selectbox('Departure Airport Traffic', ('Low', 'Medium', 'High'))
with col2:
    st.selectbox('Arrival Airport Traffic', ('Low', 'Medium', 'High'))

# Code for Prediction
if st.button('Predict Delay'):
    # Create a DataFrame with the actual input data
    input_data = pd.DataFrame({
        'time_category': [time_category],
    })

    # Perform one-hot encoding using pd.get_dummies
    input_data_encoded = pd.get_dummies(input_data, dtype=int)

    # Define the expected columns based on the training data
    expected_columns = ['time_category_before 6am', 'time_category_6am to 11:59am', 'time_category_12pm to 6pm', 'time_category_after 6pm']

    # Reindex the DataFrame to match the expected structure
    input_data_encoded = input_data_encoded.reindex(columns=expected_columns, fill_value=0)

    # Ensure input_data_encoded has the correct columns for the model
    for col in expected_columns:
        if col not in input_data_encoded.columns:
            input_data_encoded[col] = 0

    # Perform the prediction
    try:
        prediction = model.predict(input_data_encoded)

        # Select Probability of Delay Output
        if prediction[0] == 0:
            st.success('There is a Low Probability of Delay.')
        elif prediction[0] == 1:
            st.warning('There is a Moderate Probability of Delay.')
        elif prediction[0] == 2:
            st.error('There is a High Probability of Delay.')
    except Exception as e:
        st.error(f"An error occurred during prediction: {e}")

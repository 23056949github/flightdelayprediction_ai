import streamlit as st

# Set page configuration
st.set_page_config(page_title="Flight Delay Prediction",
                   layout="wide",
                   page_icon="✈️")

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


# Define the layout for the inputs
col1, col2 = st.columns(2)

# Select box for Departure Time
with col1:
    departure_time = st.selectbox('Scheduled Departure Time', 
                                  ('before 6am', '6am to 11:59am', '12pm to 6pm', 'after 6pm'))

# Number input for Flight Number
with col2:
    flight_number = st.number_input('Flight Number')

# Select box for Day of the Week
with col1:
    day_of_week = st.selectbox('Day of the Week', 
                               ('Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'))

# Time input for Scheduled Arrival Time
with col2:
    arrival_time = st.selectbox('Scheduled Arrival Time', 
                                ('before 6am', '6am to 11:59am', '12pm to 6pm', 'after 6pm'))

# Select box for Weather at Departure Airport
with col1:
    weather_departure_temp = st.selectbox('Weather at Departure Airport - Temperature', 
                                          ('<0°C', '0-10°C', '10-20°C', '20-30°C', '>30°C'))
    weather_departure_visibility = st.selectbox('Weather at Departure Airport - Visibility', 
                                                ('<1 km', '1-3 km', '3-5 km', '>5 km'))
    weather_departure_wind = st.selectbox('Weather at Departure Airport - Wind Speed', 
                                          ('<10 km/h', '10-20 km/h', '20-30 km/h', '>30 km/h'))
    weather_departure_precipitation = st.selectbox('Weather at Departure Airport - Precipitation', 
                                                   ('None', 'Rain', 'Snow', 'Fog'))

# Select box for Weather at Arrival Airport
with col2:
    weather_arrival_temp = st.selectbox('Weather at Arrival Airport - Temperature', 
                                        ('<0°C', '0-10°C', '10-20°C', '20-30°C', '>30°C'))
    weather_arrival_visibility = st.selectbox('Weather at Arrival Airport - Visibility', 
                                              ('<1 km', '1-3 km', '3-5 km', '>5 km'))
    weather_arrival_wind = st.selectbox('Weather at Arrival Airport - Wind Speed', 
                                        ('<10 km/h', '10-20 km/h', '20-30 km/h', '>30 km/h'))
    weather_arrival_precipitation = st.selectbox('Weather at Arrival Airport - Precipitation', 
                                                 ('None', 'Rain', 'Snow', 'Fog'))

# Select box for Departure Airport Traffic
with col1:
    departure_traffic = st.selectbox('Departure Airport Traffic', ('Low', 'Medium', 'High'))

# Select box for Arrival Airport Traffic
with col2:
    arrival_traffic = st.selectbox('Arrival Airport Traffic', ('Low', 'Medium', 'High'))

# Select box for Historical Delays for the Specific Flight
with col1:
    historical_delays = st.selectbox('Historical Delays for the Specific Flight', ('None', 'Low', 'Medium', 'High'))

# Select box for Airline
with col2:
    airline = st.selectbox('Airline', 
                           ('American Airlines', 'Delta', 'United', 'Southwest', 'JetBlue', 'Alaska Airlines'))

# Define possible outputs for Probability of Delay
st.write("### Probability of Delay")
probability_of_delay = st.radio('Select Probability of Delay Output', 
                                ('Low Probability of Delay', 'Moderate Probability of Delay', 'High Probability of Delay'))

if probability_of_delay == 'Low Probability of Delay':
    st.write("There is a 20% chance that the flight will be delayed.")
elif probability_of_delay == 'Moderate Probability of Delay':
    st.write("There is a 50% chance that the flight will be delayed.")
elif probability_of_delay == 'High Probability of Delay':
    st.write("There is an 80% chance that the flight will be delayed.")

# app.py for Streamlit

import streamlit as st
import pandas as pd
import plotly.express as px

# Set the page configuration for a wider layout
st.set_page_config(layout="wide")

# --- 1. Data Loading and Preparation ---

# Load the monthly accidents data
# Streamlit's caching decorator speeds up the app by not reloading data on every interaction.
@st.cache_data
def load_monthly_data():
    try:
        df = pd.read_csv('https://github.com/harshala2429/RoadAccidentsDashboardNew/blob/main/only_road_accidents_data_month2.csv')
        # Melt the DataFrame to transform the monthly columns into rows
        melted_df = df.melt(
            id_vars=['STATE/UT', 'YEAR', 'TOTAL'],
            var_name='Month',
            value_name='Accidents',
            value_vars=[col for col in df.columns if col not in ['STATE/UT', 'YEAR', 'TOTAL']]
        )
        # Define a categorical type for months to ensure they are sorted correctly
        month_order = ['JANUARY', 'FEBRUARY', 'MARCH', 'APRIL', 'MAY', 'JUNE', 'JULY', 'AUGUST', 'SEPTEMBER', 'OCTOBER', 'NOVEMBER', 'DECEMBER']
        melted_df['Month'] = pd.Categorical(melted_df['Month'], categories=month_order, ordered=True)
        return melted_df
    except FileNotFoundError:
        st.error("Error: 'only_road_accidents_data_month2.csv' not found. Please ensure the file is in the same directory.")
        return pd.DataFrame()

# Load the time-of-day accidents data
@st.cache_data
def load_time_data():
    try:
        df = pd.read_csv('https://raw.githubusercontent.com/harshala2429/RoadAccidentsDashboardNew/refs/heads/main/only_road_accidents_data3.csv')
        # Melt the DataFrame to transform the time-of-day columns into rows.
        melted_df = df.melt(
            id_vars=['STATE/UT', 'YEAR', 'Total'],
            var_name='Time of Day',
            value_name='Accidents',
            value_vars=[col for col in df.columns if col not in ['STATE/UT', 'YEAR', 'Total']]
        )
        # Ensure the time periods are in a logical order
        time_of_day_order = ['0-3 hrs. (Night)', '3-6 hrs. (Night)', '6-9 hrs (Day)', '9-12 hrs (Day)', '12-15 hrs (Day)', '15-18 hrs (Day)', '18-21 hrs (Night)', '21-24 hrs (Night)']
        melted_df['Time of Day'] = pd.Categorical(melted_df['Time of Day'], categories=time_of_day_order, ordered=True)
        return melted_df
    except FileNotFoundError:
        st.error("Error: 'only_road_accidents_data3.csv' not found. Please ensure the file is in the same directory.")
        return pd.DataFrame()

# Load the dataframes
melted_monthly = load_monthly_data()
melted_time = load_time_data()

# Check if data loaded correctly before proceeding
if melted_monthly.empty or melted_time.empty:
    st.stop()

# --- 2. Streamlit UI and Logic ---

st.title("Road Accidents Dashboard")
st.markdown("Analyze road accident data by state, year, and time using interactive charts.")

# Create columns for the dropdowns
col1, col2 = st.columns(2)

with col1:
    states = sorted(melted_monthly['STATE/UT'].unique())
    selected_state = st.selectbox("Select State/UT:", states, index=0)

with col2:
    years = sorted(melted_monthly['YEAR'].unique())
    selected_year = st.selectbox("Select Year:", years, index=0)

# Filter the data based on user selections
filtered_df_monthly = melted_monthly[(melted_monthly['STATE/UT'] == selected_state) & (melted_monthly['YEAR'] == selected_year)]
filtered_df_time = melted_time[(melted_time['STATE/UT'] == selected_state) & (melted_time['YEAR'] == selected_year)]

# Create and display the monthly accidents chart
st.header(f"Monthly Accidents in {selected_state} ({selected_year})")
monthly_fig = px.bar(
    filtered_df_monthly,
    x='Month',
    y='Accidents',
    labels={'Accidents': 'Number of Accidents'},
    color='Accidents',
    color_continuous_scale=px.colors.sequential.RdYlGn_r
)
st.plotly_chart(monthly_fig, use_container_width=True)

# Create and display the time-of-day chart
st.header(f"Accidents by Time of Day in {selected_state} ({selected_year})")
time_fig = px.line(
    filtered_df_time,
    x='Time of Day',
    y='Accidents',
    labels={'Accidents': 'Number of Accidents', 'Time of Day': 'Time Period'},
    markers=True,
    line_shape='linear',
    color_discrete_sequence=['#3498db']
)
st.plotly_chart(time_fig, use_container_width=True)




import streamlit as st
import numpy as np
import pandas as pd

# Example data for routes
route_data = {
    "Route": ["Route 1", "Route 2", "Route 3"],
    "Distance (miles)": [10, 12, 8],
    "Elevation Change (feet)": [300, 100, 400],
    "Road Condition": ["Smooth", "Rough", "Smooth"]
}

df = pd.DataFrame(route_data)

# Vehicle efficiency in kWh per mile (assumed)
efficiency_per_mile = 0.2

# Function to calculate estimated energy consumption (kWh)
def calculate_energy(row):
    distance = row["Distance (miles)"]
    elevation_change = row["Elevation Change (feet)"]
    road_condition = row["Road Condition"]

    # Base energy consumption
    base_energy = distance * efficiency_per_mile

    # Add energy for elevation change (0.05 kWh per 100 feet)
    elevation_energy = (elevation_change / 100) * 0.05

    # Add energy for road condition (rough road consumes more energy)
    if road_condition == "Rough":
        road_condition_energy = distance * 0.1
    else:
        road_condition_energy = 0

    # Total estimated energy consumption
    return base_energy + elevation_energy + road_condition_energy

# Apply the calculation to each route
df["Estimated Energy (kWh)"] = df.apply(calculate_energy, axis=1)

# Streamlit app layout and visuals
st.title("Ford Green Route Integration")
st.write("Visualize energy-efficient routes for Ford's electric vehicles.")

# Show route data with the estimated energy consumption
st.write("### Route Data with Estimated Energy Consumption")
st.dataframe(df)

# Display bar chart to compare energy consumption between routes
st.write("### Energy Consumption Comparison")
st.bar_chart(df["Estimated Energy (kWh)"])

# Battery life slider (change this to 40 as the default value)
battery_life = st.slider("Select current battery life (kWh)", 0, 60, 40)

# Show the routes that can be taken based on the available battery life
st.write(f"With {battery_life} kWh available, the following routes are possible:")
possible_routes = df[df["Estimated Energy (kWh)"] <= battery_life]
st.dataframe(possible_routes)

# Add visual feedback for the energy consumption comparison
st.write("### Routes and Estimated Energy Consumption")
for index, row in df.iterrows():
    if row["Estimated Energy (kWh)"] <= battery_life:
        st.success(f"{row['Route']} is possible with {battery_life} kWh left.")
    else:
        st.warning(f"{row['Route']} requires more energy than {battery_life} kWh.")

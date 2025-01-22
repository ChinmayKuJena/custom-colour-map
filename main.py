import streamlit as st
import geopandas as gpd
import pandas as pd
import matplotlib.pyplot as plt
from io import BytesIO


# Load the shapefile for state boundaries
shapefile_path = "gadm41_IND_1.shp"  # Replace with the actual path
india_states = gpd.read_file(shapefile_path)

# Check for the column with state names
state_name_column = 'NAME_1'  # Update this if the state column name is different

# Sidebar input for custom colors
st.sidebar.header("Customize State Colors")
state_colors = {}

# Get unique state names
unique_states = india_states[state_name_column].unique()

# Create dynamic inputs for each state
for state in unique_states:
    color = st.sidebar.color_picker(f"Pick a color for {state}", "#CCCCCC")  # Default to gray
    state_colors[state] = color

# Convert state_colors to a DataFrame
state_colors_df = pd.DataFrame(list(state_colors.items()), columns=['State', 'Color'])

# Merge shapefile data with state color mapping
india_states = india_states.merge(state_colors_df, left_on=state_name_column, right_on='State', how='left')

# Plot the map dynamically
st.title("Interactive India Map with Custom State Colors")
fig, ax = plt.subplots(1, 1, figsize=(15, 15))
india_states.plot(ax=ax, color=india_states['Color'], edgecolor='black')

# Display the map in the Streamlit app
st.pyplot(fig)

# Save the map as an image in memory
buffer = BytesIO()
fig.savefig(buffer, format='png', dpi=300, bbox_inches='tight')
buffer.seek(0)

# Add a download button to save the map
st.download_button(
    label="Download Map as PNG",
    data=buffer,
    file_name="india_map.png",
    mime="image/png"
)


# Show color mapping as a table
st.write("### State Color Mapping")
st.write(state_colors_df)

import streamlit as st
import plotly.express as px
import pandas as pd

st.set_page_config(layout="wide")


# Streamlit App
st.title("RE Map App")
st.markdown("Welcome to the RE Map App! This is very basic demo app for visualizing localized real estate market data. Basically it's a dynamic choropleth map with a table. Upload a CSV (from realtor.com or similar) and pick a column to chart. Or just use the example data provided.")
# File uploader for CSV file
uploaded_file = st.file_uploader("Upload a CSV file", type=["csv"])

if uploaded_file is not None:
    # Read the uploaded CSV file
    df = pd.read_csv(uploaded_file)

else:
    df = pd.read_csv("example.csv")

"### Choose a column and color scheme"
# Dropdown for selecting column to map
column_to_map = st.selectbox("Select a column to map", df.columns)

# Dropdown for selecting color scale
color_scale = st.selectbox("Select a color scale (it won't break anything)", px.colors.named_colorscales())

"### View the results"
# Choropleth map
fig = px.choropleth(
    df,
    locations="state_id",
    locationmode="USA-states",
    color=column_to_map,
    hover_name="state",
    color_continuous_scale=color_scale,
    scope="usa",
    title=f"{column_to_map.replace('-',' ').capitalize()} by State"
)

col1, col2 = st.columns([1,2], gap="large")

selected_df = df[['state', column_to_map]].sort_values(by=[column_to_map], ascending=False)

with col1:
    percent_col = st.checkbox(f"Format '{column_to_map}' as %?")
    if percent_col:
        selected_df[column_to_map] = selected_df[column_to_map].map('{:.2%}'.format)
    st.dataframe(selected_df, hide_index=True)

# Display the choropleth map
with col2:
    st.plotly_chart(fig, use_container_width=True)

"### Data"
df
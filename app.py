import streamlit as st
import plotly.express as px
import pandas as pd

st.set_page_config(layout="wide")


# Streamlit App
st.title("RE Map App")

# File uploader for CSV file
uploaded_file = st.file_uploader("Upload a CSV file", type=["csv"])

if uploaded_file is not None:
    # Read the uploaded CSV file
    df = pd.read_csv(uploaded_file)

else:
    df = pd.read_csv("example.csv")

# Dropdown for selecting column to map
column_to_map = st.selectbox("Select Column to Map", df.columns)

# Dropdown for selecting color scale
color_scale = st.selectbox("Select Color Scale", px.colors.named_colorscales())

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

df = df[['state', column_to_map]].sort_values(by=[column_to_map], ascending=False)

with col1:
    percent_col = st.checkbox(f"Format '{column_to_map}' as %?")

    if percent_col:
        df[column_to_map] = df[column_to_map].map('{:.2%}'.format)
    st.dataframe(df, hide_index=True)

# Display the choropleth map
with col2:
    st.plotly_chart(fig, use_container_width=True)

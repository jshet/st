import streamlit as st
import plotly.express as px
import pandas as pd

st.set_page_config(layout="wide")

with open( "style.css" ) as css:
    st.markdown( f'<style>{css.read()}</style>' , unsafe_allow_html= True)

# Streamlit App
st.title("Current by state")
"View current real estate data by state."

col1, col2 = st.columns([1,3], gap="large")

with col1:
    "## Settings"
    st.markdown("""Welcome to the RE Map App! 
    This is very basic demo app for visualizing localized real estate market data.  
    Basically, it's a dynamic choropleth map with a table.  
    Upload a CSV (from realtor.com or similar) and pick a column to chart. Or just use the example data provided."""
    )
    
    "#### Upload data"
    # File uploader for CSV file
    uploaded_file = st.file_uploader("Upload a CSV file", type=["csv"])

    if uploaded_file is not None:
        # Read the uploaded CSV file
        df = pd.read_csv(uploaded_file)

    else:
        df = pd.read_csv("./data/example.csv")

    "#### Choose a column"
    # Dropdown for selecting column to map
    column_to_map = st.selectbox("Select a column to map", df.columns)
    percent_col = st.checkbox(f"Format '{column_to_map}' as %?")

    "#### Pick a color scheme (optional)"
    # Dropdown for selecting color scale
    color_scale = st.selectbox("Select a color scale (it won't break anything)", px.colors.named_colorscales())

with col2:
    "## Charts"
    f"### {column_to_map.replace('_',' ').capitalize()} by state (map)"

    # Choropleth map
    fig = px.choropleth(
        df,
        locations="state_id",
        locationmode="USA-states",
        color=column_to_map,
        hover_name="state",
        color_continuous_scale=color_scale,
        scope="usa"
    )
    fig.update_layout(height=800)

    selected_df = df[['state', column_to_map]].sort_values(by=[column_to_map], ascending=False)

    if percent_col:
        selected_df[column_to_map] = selected_df[column_to_map].map('{:.2%}'.format)

    # Display the choropleth map
    st.plotly_chart(fig, use_container_width=True)

    fig = px.bar(df, x="state", y=column_to_map, color=column_to_map, color_continuous_scale=color_scale)
    fig.update_traces(textfont_size=6, textangle=0, textposition="outside", cliponaxis=False)
    fig.update_layout(height=800)

    f"### {column_to_map.replace('_',' ').capitalize()} by state (bar graph)"
    st.plotly_chart(fig, use_container_width=True)

    f"### {column_to_map.replace('_',' ').capitalize()} by state (table)"
    st.dataframe(selected_df, hide_index=True)

    "### Dataframe w/all columns"
    df
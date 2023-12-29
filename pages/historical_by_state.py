import streamlit as st
import plotly.express as px
import pandas as pd

st.set_page_config(layout="wide")

with open( "style.css" ) as css:
    st.markdown( f'<style>{css.read()}</style>' , unsafe_allow_html= True)

# Streamlit App
st.title("Historical by state")
"View current real estate data by state."

col1, col2 = st.columns([1,3], gap="large")

with col1:
    "## Settings"
    
    "#### Upload data"
    # File uploader for CSV file
    uploaded_file = st.file_uploader("Upload a CSV file", type=["csv"])

    if uploaded_file is not None:
        # Read the uploaded CSV file
        df = pd.read_csv(uploaded_file)

    else:
        df = pd.read_csv("./data/example_with_history.csv")

    df['month_date_yyyymm'] = pd.to_datetime(df['month_date_yyyymm'], format='%Y%m')

    "#### Choose a column"
    # Dropdown for selecting column to map
    column_to_map = st.selectbox("Select a column to map", df.columns)

    "#### Select one or more states (optional)"
    # Dropdown for selecting state to map
    container = st.container()
    all = st.checkbox("Select all")
    
    if all:
        selected_options = container.multiselect("Select one or more options:",
            df['state'].unique(),df['state'].unique())
    else:
        selected_options =  container.multiselect("Select one or more options:",
            df['state'].unique())

    df = df.loc[df["state"].isin(selected_options)]


with col2:
    "## Charts"
    f"### {column_to_map.replace('_',' ').capitalize()} by state"

    fig = px.line(df, x="month_date_yyyymm", y=column_to_map, color='state')
    fig.update_layout(height=800)

    selected_df = df[['state', column_to_map]].sort_values(by=[column_to_map], ascending=False)

    st.plotly_chart(fig, use_container_width=True)

    "### Dataframe w/all available columns"
    df
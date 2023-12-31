import streamlit as st
import pandas as pd
import plotly.express as px
import json

st.set_page_config(layout="wide")
with open( "style.css" ) as css:
    st.markdown( f'<style>{css.read()}</style>' , unsafe_allow_html= True)

st.title("Historical by county")
"View historical real estate data by county."

@st.cache_data
def load_county_geo():
    with open('./data/county_geo.json') as f:
        counties = json.load(f)
        return counties

counties = load_county_geo()

@st.cache_data
def load():
    df = pd.read_csv("./data/counties_with_history.csv", dtype={"fips": str})
    df['month_date_yyyymm'] = pd.to_datetime(df['month_date_yyyymm'], format='%Y%m')
    return df

df = load()

col1, col2 = st.columns([1,3], gap='large')

with col1:
    "#### Choose a column"
    # Dropdown for selecting column to map
    column_to_map = st.selectbox("Select a column to map", df.columns)
    if column_to_map == 'month_date_yyyymm':
        column_to_map = 'active_listing_count'

    "#### Select a county"
    # Dropdown for selecting county to map

    selected_options = st.selectbox("Select one or more options:", df['county_name'].unique())

    df = df.loc[df["county_name"] == selected_options]

    latest_df = df.loc[df["month_date_yyyymm"] == df["month_date_yyyymm"].max()]
    st.metric(column_to_map, latest_df[column_to_map], delta=None, delta_color="normal", help=None, label_visibility="visible")

with col2:
    f"### Map of {selected_options}"
    fig = px.choropleth(latest_df, geojson=counties, locations='fips', color=column_to_map,
                            color_continuous_scale="Viridis",
                            #    range_color=(0, 12),
                            scope="usa",
                            labels={column_to_map:column_to_map}
                            )

    fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
    st.plotly_chart(fig)

    fig = px.scatter(df, x="month_date_yyyymm", y=column_to_map, trendline="lowess")

    min_date = df["month_date_yyyymm"].min()
    max_date = df["month_date_yyyymm"].max()

    f"### {column_to_map.replace('_',' ').capitalize()}"
    st.plotly_chart(fig)

    f"### All historical data for {selected_options}"
    df
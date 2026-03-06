import streamlit as st
import pandas as pd
import psycopg2
from streamlit_folium import st_folium
import folium
import json

# 1. PAGE CONFIGURATION
st.set_page_config(page_title="Kiriaini Market Analytics", layout="wide")
st.title("Kiriaini Market: Spatial Data Dashboard")

# 2. DATABASE DATA FETCHING
@st.cache_data # Logic: Cache the data so the app stays fast
def get_data():
    conn = psycopg2.connect(
        dbname=st.secrets["database"]["dbname"],
        user=st.secrets["database"]["user"],
        password=st.secrets["database"]["password"],
        host=st.secrets["database"]["host"],
        port=st.secrets["database"]["port"],
        sslmode="require"
    )
    # Fetch both attributes for stats and geometry for the map
    df = pd.read_sql_query("SELECT gid, length_m, ST_AsGeoJSON(ST_Transform(geom, 4326)) as geom FROM kiriaini_roads", conn)
    conn.close()
    return df

df = get_data()

# 3. SIDEBAR STATISTICS
st.sidebar.header("Market Statistics")
total_length = df['length_m'].sum()
avg_length = df['length_m'].mean()

st.sidebar.metric("Total Roads", len(df))
st.sidebar.metric("Total Road Extend  (m)", f"{total_length:,.2f}")
st.sidebar.metric("Average Road Size", f"{avg_length:,.2f}")

# Transport Valuation Tool
st.sidebar.markdown("---")
st.sidebar.header("Transport Valuation Tool")
unit_price = st.sidebar.number_input("Price per m (KES)", min_value=0, value=1)

# Calculate dynamic value
total_value = total_length * unit_price/55000
st.sidebar.subheader(f"Total Transport Value:")
st.sidebar.write(f"KES {total_value:,.2f}")

# FILTER 
st.subheader("Filter by Size")
min_size, max_size = st.select_slider(
    "Select a range of road extend (m)",
    options=sorted(df['length_m'].unique()),
    value=(df['length_m'].min(), df['length_m'].max())
)

# Filter the dataframe before showing the map
filtered_df = df[(df['length_m'] >= min_size) & (df['length_m'] <= max_size)]
# 4. INTERACTIVE MAP
st.subheader("Interactive Road Explorer")
m = folium.Map(location=[-0.6025998054452301, 36.95381681317332], zoom_start=16)

# Download Filtered Data
csv_data = filtered_df.drop(columns=['geom']).to_csv(index=False).encode('utf-8')
st.download_button(
    label="📥 Download Filtered Report",
    data=csv_data,
    file_name='Kiriaini_Filtered_Report.csv',
    mime='text/csv',
)

# Add GeoJSON to map
for _, row in filtered_df.iterrows():
    geojson_feature = {
        "type" : "Feature",
        "geometry" : json.loads(row['geom']),  #Safe instead of eval()
    }
    
    folium.GeoJson(
        geojson_feature,
        tooltip=f"ID: {row['gid']} | Length: {row['length_m']} m"
        ).add_to(m)

# Render the map in Streamlit

st_folium(m, width=1000, height=500)




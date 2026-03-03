#**Kiriaini Market Spatial Analytics Dashboard**
A lightweight Streamlit web application for visualizing and analyzing spatial road data in Kiriaini Market. The dashboard connects to a PostgreSQL/PostGIS database, provides real-time road statistics, interactive filtering, transport valuation estimates, and downloadable reports.

**Features**
##Market Statistics
Total number of roads
Total road length (meters)
Average road length

**Transport Valuation Tool**
Dynamic price-per-meter input (KES)
Automatic total transport value calculation

**Interactive Filtering**
Filter roads by length range
Real-time updates

**Spatial Visualization**
Interactive Folium map
GeoJSON rendering from PostGIS
Tooltip-based road inspection

**Data Export**
Download filtered results as CSV
**Tech Stack**
Python
Streamlit
Pandas
PostgreSQL + PostGIS
Folium
psycopg2

**Setup**
Clone the repository
Install dependencies:
pip install -r requirements.txt
Configure database credentials in .streamlit/secrets.toml
_Run the app:_
streamlit run app.py
**Data Source**
Road geometry and length data are retrieved from the kiriaini_roads PostGIS table and transformed to WGS84 (EPSG:4326) for web mapping.
**License**
This resources is  for academic and planning use. It can be Modified minimally as needed for production deployment.
Author: Hari Spatial
Location: Kiriaini Market, Kenya
# Render the map in Streamlit
st_folium(m, width=1000, height=500)

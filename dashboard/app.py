from pathlib import Path
import sys, sqlite3
import pandas as pd
import streamlit as st
import plotly.express as px
ROOT=Path(__file__).resolve().parents[1]; sys.path.insert(0,str(ROOT))
from src.utils import DB_PATH, initialize_database
st.set_page_config(page_title="LogiTrack | Logistics Intelligence",page_icon="🚚",layout="wide")

st.markdown("""
<style>
    /* Overall page */
    .stApp {
        background-color: #F7F9FC;
        color: #344054;
    }

    /* Main title */
    h1 {
        color: #405D73;
        font-weight: 700;
    }

    h2, h3 {
        color: #526D82;
    }

    /* KPI metric cards */
    div[data-testid="stMetric"] {
        background-color: #EDF3F7;
        border: 1px solid #DCE7EF;
        padding: 18px;
        border-radius: 14px;
    }

    div[data-testid="stMetricLabel"] {
        color: #617789;
    }

    div[data-testid="stMetricValue"] {
        color: #42657D;
    }

    /* Sidebar */
    section[data-testid="stSidebar"] {
        background-color: #EEF3F5;
    }

    /* Expandable SQL result sections */
    div[data-testid="stExpander"] {
        background-color: #FFFFFF;
        border: 1px solid #DCE6EC;
        border-radius: 12px;
        margin-bottom: 10px;
    }

    /* Tabs */
    button[data-baseweb="tab"] {
        color: #637789;
        font-weight: 500;
    }

    button[data-baseweb="tab"][aria-selected="true"] {
        color: #527D78;
    }

    /* Tables */
    div[data-testid="stDataFrame"] {
        border: 1px solid #E1E8ED;
        border-radius: 10px;
        overflow: hidden;
    }

    /* Buttons */
    .stButton button {
        background-color: #E4EFEB;
        color: #426A60;
        border: 1px solid #D2E3DC;
        border-radius: 8px;
    }

    .stButton button:hover {
        background-color: #D6E7DF;
        border-color: #B9D4C8;
        color: #355B50;
    }

    /* Subtle separators */
    hr {
        border-color: #E3EAF0;
    }
</style>
""", unsafe_allow_html=True)

st.title("🚚 LogiTrack | Logistics Intelligence")
st.caption("SQL-powered delivery operations, driver performance, fleet utilization and customer feedback.")
if not DB_PATH.exists(): initialize_database()
@st.cache_data
def load():
 c=sqlite3.connect(DB_PATH)
 q="""SELECT s.*, d.delivery_id,d.actual_dt,d.status,d.delay_hours,r.origin_city,r.dest_city,r.distance_km,r.route_type,
 dr.name driver_name,dr.experience,v.vehicle_type,w.name warehouse_name,f.rating customer_rating,f.comment,f.feedback_dt
 FROM shipments s LEFT JOIN deliveries d USING(shipment_id) LEFT JOIN routes r USING(route_id)
 LEFT JOIN drivers dr USING(driver_id) LEFT JOIN vehicles v USING(vehicle_id) LEFT JOIN warehouses w USING(warehouse_id)
 LEFT JOIN feedback f USING(delivery_id)"""
 x=pd.read_sql_query(q,c); c.close()
 for col in ["shipment_dt","actual_dt","feedback_dt"]: x[col]=pd.to_datetime(x[col],errors="coerce")
 x["month"]=x.shipment_dt.dt.to_period("M").astype(str)
 return x
df=load()
with st.sidebar:
 st.header("Dashboard Filters"); st.caption("Selections apply to every dashboard tab.")
 dates=df.shipment_dt.dropna()
 drange=st.date_input("Shipment date range",(dates.min().date(),dates.max().date()))
 def choose(label,col): return st.multiselect(label,sorted(df[col].dropna().astype(str).unique()),default=sorted(df[col].dropna().astype(str).unique()))
 statuses=choose("Delivery status","status"); whs=choose("Warehouse","warehouse_name"); routes=choose("Route type","route_type"); drivers=choose("Driver","driver_name"); vehicles=choose("Vehicle type","vehicle_type")
f=df.copy()
if isinstance(drange,tuple) and len(drange)==2: f=f[f.shipment_dt.dt.date.between(drange[0],drange[1])]
for c,vals in [("status",statuses),("warehouse_name",whs),("route_type",routes),("driver_name",drivers),("vehicle_type",vehicles)]: f=f[f[c].astype(str).isin(vals)] if vals else f.iloc[:0]
tabs=st.tabs(["Business Overview","Delivery Analysis","Driver Performance","Vehicle & Route Analysis","Customer Feedback","SQL Queries"])
with tabs[0]:
 st.subheader("Business Overview")
 success=100*f.status.eq("Delivered").sum()/f.status.notna().sum() if f.status.notna().sum() else 0
 cols=st.columns(5)
 for c,l,v in zip(cols,["Total Deliveries","Total Shipments","Average Delay","Average Customer Rating","Delivery Success Rate"],[f"{f.delivery_id.nunique():,}",f"{f.shipment_id.nunique():,}",f"{f.delay_hours.mean():.2f} hrs",f"{f.customer_rating.mean():.2f} / 5",f"{success:.1f}%"]): c.metric(l,v)
 a,b=st.columns(2); a.plotly_chart(px.pie(f,names="status",hole=.45,title="Delivery Outcome Mix"),use_container_width=True)
 b.plotly_chart(px.line(f.groupby("month",as_index=False).shipment_id.nunique(),x="month",y="shipment_id",markers=True,title="Shipment Volume by Month"),use_container_width=True)
 if len(f):
  x=f.groupby("route_type").delay_hours.mean().sort_values(ascending=False)
  st.info(f"Highest average delay in this filtered selection: {x.index[0]} routes ({x.iloc[0]:.2f} hours). Investigate operational causes before drawing causal conclusions.")
with tabs[1]:
 st.subheader("Delivery Analysis"); a,b=st.columns(2)
 a.plotly_chart(px.histogram(f,x="status",title="Delivery Status Distribution"),use_container_width=True)
 b.plotly_chart(px.bar(f.groupby("route_type",as_index=False).delay_hours.mean(),x="route_type",y="delay_hours",title="Average Delay by Route Type"),use_container_width=True)
 a,b=st.columns(2); a.plotly_chart(px.line(f.groupby("month",as_index=False).delivery_id.nunique(),x="month",y="delivery_id",title="Monthly Delivery Trends"),use_container_width=True)
 b.plotly_chart(px.bar(f.groupby("warehouse_name",as_index=False).delay_hours.mean(),x="warehouse_name",y="delay_hours",title="Delay by Warehouse"),use_container_width=True)
with tabs[2]:
 st.subheader("Driver Performance"); g=f.groupby(["driver_name","experience"],as_index=False).agg(deliveries=("delivery_id","nunique"),rating=("customer_rating","mean"),delay=("delay_hours","mean"))
 a,b=st.columns(2); a.plotly_chart(px.bar(g.nlargest(10,"rating"),x="rating",y="driver_name",orientation="h",title="Top 10 Drivers by Rating"),use_container_width=True)
 b.plotly_chart(px.scatter(g,x="experience",y="rating",size="deliveries",hover_name="driver_name",title="Driver Experience vs Performance"),use_container_width=True)
 st.plotly_chart(px.bar(g.nlargest(20,"deliveries"),x="driver_name",y="deliveries",title="Driver Workload Distribution"),use_container_width=True); st.dataframe(g,use_container_width=True,hide_index=True)
with tabs[3]:
 st.subheader("Vehicle & Route Analysis"); a,b=st.columns(2)
 a.plotly_chart(px.histogram(f,x="vehicle_type",title="Vehicle Utilization (Shipment Count)"),use_container_width=True)
 route=f.groupby(["route_type","origin_city","dest_city"],as_index=False).agg(delay_hours=("delay_hours","mean"),distance_km=("distance_km","mean")); route["route"]=route.origin_city+" → "+route.dest_city
 b.plotly_chart(px.bar(route.nlargest(12,"delay_hours"),x="delay_hours",y="route",orientation="h",title="Route Performance Comparison"),use_container_width=True)
 st.plotly_chart(px.scatter(f,x="distance_km",y="delay_hours",color="route_type",title="Distance vs Delay"),use_container_width=True)
with tabs[4]:
 st.subheader("Customer Feedback"); a,b=st.columns(2)
 a.plotly_chart(px.histogram(f,x="customer_rating",title="Rating Distribution"),use_container_width=True)
 b.plotly_chart(px.bar(f.groupby("status",as_index=False).customer_rating.mean(),x="status",y="customer_rating",title="Rating by Delivery Status"),use_container_width=True)
 trend=f.dropna(subset=["feedback_dt"]).assign(feedback_month=lambda z:z.feedback_dt.dt.to_period("M").astype(str)).groupby("feedback_month",as_index=False).customer_rating.mean()
 st.plotly_chart(px.line(trend,x="feedback_month",y="customer_rating",markers=True,title="Rating Trends Over Time"),use_container_width=True)

with tabs[5]:
    queries = [
        ("Total Deliveries by Status", """
            SELECT status, COUNT(*) AS total_deliveries
            FROM deliveries
            GROUP BY status
            ORDER BY total_deliveries DESC
        """),
        ("Monthly Shipment Volume", """
            SELECT substr(shipment_dt, 1, 7) AS month,
                   COUNT(*) AS total_shipments
            FROM shipments
            GROUP BY month
            ORDER BY month
        """),
        ("Average Delay by Route Type", """
            SELECT r.route_type,
                   ROUND(AVG(d.delay_hours), 2) AS average_delay_hours
            FROM deliveries d
            JOIN shipments s ON d.shipment_id = s.shipment_id
            JOIN routes r ON s.route_id = r.route_id
            GROUP BY r.route_type
        """),
        ("Warehouse Performance", """
            SELECT w.name AS warehouse,
                   ROUND(AVG(d.delay_hours), 2) AS average_delay_hours
            FROM warehouses w
            JOIN shipments s ON w.warehouse_id = s.warehouse_id
            JOIN deliveries d ON s.shipment_id = d.shipment_id
            GROUP BY w.name
            ORDER BY average_delay_hours DESC
        """),
        ("Top 10 Drivers by Rating", """
            SELECT dr.name AS driver,
                   ROUND(AVG(f.rating), 2) AS average_rating
            FROM drivers dr
            JOIN shipments s ON dr.driver_id = s.driver_id
            JOIN deliveries d ON s.shipment_id = d.shipment_id
            LEFT JOIN feedback f ON d.delivery_id = f.delivery_id
            GROUP BY dr.driver_id, dr.name
            ORDER BY average_rating DESC
            LIMIT 10
        """),
        ("Vehicle Utilization", """
            SELECT v.vehicle_type,
                   COUNT(s.shipment_id) AS total_shipments
            FROM vehicles v
            LEFT JOIN shipments s ON v.vehicle_id = s.vehicle_id
            GROUP BY v.vehicle_type
        """),
        ("Customer Rating by Delivery Status", """
            SELECT d.status,
                   ROUND(AVG(f.rating), 2) AS average_rating
            FROM deliveries d
            LEFT JOIN feedback f ON d.delivery_id = f.delivery_id
            GROUP BY d.status
        """),
        ("Average Delay by Distance Category", """
            SELECT CASE
                WHEN r.distance_km < 100 THEN 'Short'
                WHEN r.distance_km < 500 THEN 'Medium'
                WHEN r.distance_km < 1000 THEN 'Long'
                ELSE 'Very Long'
            END AS distance_category,
            ROUND(AVG(d.delay_hours), 2) AS average_delay_hours
            FROM routes r
            JOIN shipments s ON r.route_id = s.route_id
            JOIN deliveries d ON s.shipment_id = d.shipment_id
            GROUP BY distance_category
        """),
        ("Driver Experience Analysis", """
            SELECT CASE
                WHEN dr.experience <= 2 THEN 'Junior'
                WHEN dr.experience <= 5 THEN 'Mid'
                WHEN dr.experience <= 10 THEN 'Senior'
                ELSE 'Expert'
            END AS experience_level,
            ROUND(AVG(f.rating), 2) AS average_rating,
            ROUND(AVG(d.delay_hours), 2) AS average_delay_hours
            FROM drivers dr
            JOIN shipments s ON dr.driver_id = s.driver_id
            JOIN deliveries d ON s.shipment_id = d.shipment_id
            LEFT JOIN feedback f ON d.delivery_id = f.delivery_id
            GROUP BY experience_level
        """),
        ("Shipments by Day of Week", """
            SELECT strftime('%w', s.shipment_dt) AS weekday,
                   COUNT(*) AS total_shipments,
                   ROUND(AVG(d.delay_hours), 2) AS average_delay_hours
            FROM shipments s
            JOIN deliveries d ON s.shipment_id = d.shipment_id
            GROUP BY weekday
            ORDER BY weekday
        """)
    ]

    with sqlite3.connect(DB_PATH) as conn:
        for title, query in queries:
            with st.expander(title, expanded=False):
                result = pd.read_sql_query(query, conn)
                st.dataframe(
                    result,
                    use_container_width=True,
                    hide_index=True
                )

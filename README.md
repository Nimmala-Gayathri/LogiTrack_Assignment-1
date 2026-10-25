# LogiTrack: Supply Chain & Logistics Performance Analytics

End-to-end logistics analytics with Python, Pandas, SQLite SQL, statistics, Plotly and Streamlit. Dashboard sections: Business Overview, Delivery Analysis, Driver Performance, Vehicle & Route Analysis, Customer Feedback, SQL Queries. Sidebar filters apply across chart tabs.

**Dataset note:** The brief references seven expanded CSV files, but those originals were not attached. This package includes clearly labelled synthetic demo data (10 warehouses, 50 drivers, 30 vehicles, 90 routes, 2,000 shipments/deliveries/feedback rows). Replace `data/raw/logitrack_*.csv` with official files before interpreting results as real business findings.

## Run (Python 3.10+)
```bash
python -m venv .venv
# Windows: .venv\Scripts\activate
# macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
python src/data_cleaning.py
python src/feature_engineering.py
python -c "from src.utils import initialize_database; initialize_database()"
streamlit run dashboard/app.py
```
KPI rules: Total Deliveries and Total Shipments are distinct IDs; Average Delay is mean non-null `delay_hours`; Average Rating is mean available feedback rating; Success Rate is Delivered / all non-null delivery statuses × 100.

Feature engineering includes delivery days, `is_delayed`, weight/distance categories, driver experience levels, month, weekday and hour. Statistical notebook includes the five tests requested in the brief. Do not commit sensitive data, credentials or generated databases to GitHub.

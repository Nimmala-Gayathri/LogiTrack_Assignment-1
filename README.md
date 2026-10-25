# LogiTrack_Assignment-1
LogiTrack is a logistics analytics project that uses Python, SQL, and Streamlit to analyze shipments, delivery delays, driver performance, vehicle usage, route efficiency, and customer satisfaction through interactive dashboards, data visualizations, and statistical analysis using synthetic data.
# LogiTrack – Supply Chain & Logistics Performance Analytics

## Project Overview

LogiTrack is a data analytics project designed to analyze supply chain and logistics operations. It helps explore shipment volumes, delivery delays, driver performance, vehicle and route efficiency, warehouse performance, and customer satisfaction.

The project uses Python, SQL, data visualization, and statistical analysis to convert raw logistics data into meaningful insights. An interactive Streamlit dashboard presents key performance indicators (KPIs), charts, filters, and SQL analysis results in an easy-to-understand format.

The project uses synthetic sample data for learning and demonstration purposes.

## Project Architecture

```text
LogiTrack/
│
├── data/
│   ├── raw/
│   │   ├── logitrack_warehouses.csv
│   │   ├── logitrack_drivers.csv
│   │   ├── logitrack_vehicles.csv
│   │   ├── logitrack_routes.csv
│   │   ├── logitrack_shipments.csv
│   │   ├── logitrack_deliveries.csv
│   │   └── logitrack_feedback.csv
│   │
│   └── cleaned/
│
├── notebooks/
│   ├── 01_data_cleaning.ipynb
│   ├── 02_feature_engineering.ipynb
│   ├── 03_eda.ipynb
│   └── 04_statistical_analysis.ipynb
│
├── sql/
│   ├── schema.sql
│   └── analysis_queries.sql
│
├── src/
│   ├── data_cleaning.py
│   ├── feature_engineering.py
│   └── utils.py
│
├── dashboard/
│   └── app.py
│
├── requirements.txt
└── README.md
```

## Data Workflow

1. **Data Collection:** Load logistics datasets from CSV files containing warehouse, driver, vehicle, route, shipment, delivery, and customer feedback information.
2. **Data Cleaning:** Remove duplicate records, standardize column names and text values, and convert date columns into suitable formats.
3. **Feature Engineering:** Create additional fields such as delivery duration, delay indicators, shipment weight categories, route distance categories, driver experience levels, and delivery date attributes.
4. **Database Management:** Load datasets into SQLite tables and use SQL queries and joins to analyze relationships between logistics entities.
5. **Exploratory Data Analysis:** Use Pandas, NumPy, and visualizations to identify patterns, trends, distributions, and potential operational issues.
6. **Statistical Analysis:** Apply statistical tests, correlation analysis, and z-score-based outlier detection to explore relationships and unusual observations.
7. **Dashboard Development:** Present KPIs, interactive charts, filters, and SQL query result tables using Streamlit and Plotly.

## Dashboard Modules

### 1. Business Overview
Displays total deliveries, total shipments, average recorded delay, average customer rating, and delivery success rate.

### 2. Delivery Analysis
Analyzes delivery status distribution, monthly delivery trends, average delay by route type, and delays by warehouse.

### 3. Driver Performance
Compares driver ratings, experience levels, and workload to explore driver performance.

### 4. Vehicle & Route Analysis
Examines shipment counts by vehicle type, route performance, and the relationship between route distance and delivery delays.

### 5. Customer Feedback
Analyzes customer rating distributions, ratings by delivery status, and rating trends over time.

### 6. SQL Queries
Displays the results of predefined SQL analyses in expandable sections, allowing users to open each section and view its result table.

## Technologies Used

- **Python:** Core programming and data processing
- **Pandas and NumPy:** Data cleaning, transformation, and analysis
- **SQL and SQLite:** Database management, joins, aggregations, and querying
- **SciPy:** Statistical testing and analysis
- **Plotly:** Interactive data visualizations
- **Streamlit:** Interactive web dashboard
- **Jupyter Notebook:** Data exploration and experimentation
- **Git and GitHub:** Version control and project hosting

## Project Objectives

- Understand logistics and delivery performance.
- Identify delivery patterns and potential delay factors.
- Analyze driver, warehouse, vehicle, and route performance.
- Explore customer satisfaction and feedback.
- Practice SQL, Python, statistics, and dashboard development.
- Present data-driven insights through interactive visualizations.

## Limitations

This project uses synthetic sample data rather than verified company records. Delay metrics are based on the fields provided in the sample data, and shipment counts by vehicle type are not a direct measurement of vehicle capacity utilization. Statistical findings are exploratory and should not be treated as proof of real-world operational relationships.

## Conclusion

LogiTrack demonstrates an end-to-end data analytics workflow, from raw data cleaning and feature engineering to SQL analysis, statistical exploration, and interactive dashboard development. It provides a practical example of how data analytics can help investigate logistics performance and support informed decision-making.

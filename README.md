# Operational Visibility & Capacity Dashboard
**A Python-based solution for real-time team management and capacity planning.**

## 🎯 Project Overview
This project was developed to bridge the visibility gap between instructor availability and curriculum delivery. Originally integrated with a private enterprise API, this version includes a **Mock Data Generator** to demonstrate the system's logic and visualization capabilities while maintaining data confidentiality.

## 🚀 Key Features
*   **Modular Architecture**: Separated data processing (`main.py`) from the visualization layer (`streamlitdash.py`) for scalability.
*   **Capacity Insights**: Real-time KPI tracking for leave requests, status distributions, and team-wide trends.
*   **Anomaly Detection**: Visualized "Request Peaks" to identify periods of high operational pressure.
*   **Automated Reporting**: Replaces manual spreadsheet tracking with an automated, filterable dashboard.

## 🛠️ Tech Stack
*   **Language**: Python 3.12
*   **Framework**: Streamlit (Dashboard UI)
*   **Data Handling**: Pandas (ETL & Grouping)
*   **Visualization**: Plotly (Interactive Charts)
*   **Deployment**: Streamlit Community Cloud
*   [**Click here to view a live demo**](https://operational-visibility-dashboard.streamlit.app/)

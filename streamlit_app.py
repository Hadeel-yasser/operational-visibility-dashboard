import plotly.express as px
import streamlit as st # used for creating interactive visualizations (through a web app)
import pandas as pd
import main
import os
st.set_page_config(page_title="Leave Requests Dashboard", layout="wide")

def visualize_data():
    
    
    st.title("Operational Health: Leave Requests Dashboard")
    st.sidebar.header("Data Management")
    if st.sidebar.button("Generate New Demo Data"):
        data = main.get_request(use_dummy=True)
        main.save_to_csv(data)
        st.sidebar.success("New data generated!")
        st.rerun()

    if not os.path.exists("Leave_Requests.csv"):
        # Initial data seed if file doesn't exist
        data = main.get_request(use_dummy=True)
        main.save_to_csv(data)

    df = pd.read_csv("Leave_Requests.csv")

    df["request_date"] = pd.to_datetime(df["request_date"], errors="coerce")

    total_requests = len(df)
    print(f"Total number of leave requests: {total_requests}")
    
    
    col1,col2,col3 = st.columns(3)
    col1.metric("Total Requests", total_requests,) 
    col2.metric("Accepted", (df["status"] == "accepted").sum())
    col3.metric("Rejected", (df["status"] == "rejected").sum())

    st.sidebar.header("Filters")
    status_filter = st.sidebar.multiselect(
    "Status",
    options=df["status"].dropna().unique(),
    default=df["status"].dropna().unique()
    )

    type_filter = st.sidebar.multiselect(
    "Request Type",
    options=df["request_type"].dropna().unique(),
    default=df["request_type"].dropna().unique()
)

    filtered_df = df[
    (df["status"].isin(status_filter)) &
    (df["request_type"].isin(type_filter))
]
    
    col1, col2 = st.columns(2)
    
    with col1:
        status_fig = px.bar(
            filtered_df["status"].value_counts().reset_index(),
            x="status",
            y="count",
            title="Requests by Status",
            color="status",
            color_discrete_map={"accepted": "lightgreen", "rejected": "lightcoral"}
        )
        st.plotly_chart(status_fig, width="stretch")
    
    with col2:
        type_fig = px.bar(
            filtered_df["request_type"].value_counts().reset_index(),
            x="request_type",
            y="count",
            color="request_type",
            color_discrete_sequence=px.colors.qualitative.Pastel,
            title="Requests by Type"
        )
        st.plotly_chart(type_fig, width="stretch")
    
    # Requests over time
    requests_over_time = (
        filtered_df.groupby("request_date")
        .size()
        .reset_index(name="count")
        .sort_values("request_date")
    )

    time_fig = px.line(
        requests_over_time,
        x="request_date",
        y="count",
        markers=True,
        title="Requests Over Time"
    )

    st.plotly_chart(time_fig, width="stretch")
    st.info("**Product Ops Insight:** Clustered spikes indicate periods of high operational pressure.")

    # Type vs Status
    type_status = (
        filtered_df.groupby(["request_type", "status"])
        .size()
        .reset_index(name="count")
    )

    type_status_fig = px.bar(
        type_status,
        x="request_type",
        y="count",
        color="status",
        barmode="group",
        color_discrete_map={"accepted": "lightgreen", "rejected": "lightcoral"},
        title="Request Type by Status"
    )

    st.plotly_chart(type_status_fig, width="stretch")

    # Top tutors
    top_tutors = (
        filtered_df["tutor_name"]
        .value_counts()
        .head(10)
        .reset_index()
    )

    top_tutors_fig = px.bar(
        top_tutors,
        x="count",
        y="tutor_name",
        orientation="h",
        color="count",
        color_continuous_scale=px.colors.sequential.Peach,
        title="Top 10 Tutors by Leave Requests"
    )

    st.plotly_chart(top_tutors_fig, width="stretch")


if __name__ == "__main__":
    visualize_data()
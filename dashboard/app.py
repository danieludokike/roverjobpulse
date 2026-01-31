
import streamlit as st
import pandas as pd
import sqlite3
from pathlib import Path
from datetime import datetime, timedelta, timezone

# ---- Database path ----
DB_PATH = Path("../database/roverjobpulse.db")


# ---- Load data ----
def load_data():
    conn = sqlite3.connect(DB_PATH)
    df = pd.read_sql("SELECT * FROM jobs", conn)
    conn.close()

    df["date_posted"] = pd.to_datetime(df["date_posted"], errors="coerce")
    df["date_scraped"] = pd.to_datetime(df["date_scraped"], errors="coerce")

    return df


# ---- Filter helpers ----
def filter_by_days(df, days):
    if days == "ALL":
        return df

    cutoff = datetime.now(timezone.utc) - timedelta(days=days)
    return df[df["date_scraped"] >= cutoff]


# ---- App ----
def main():
    st.set_page_config(
        page_title="RoverJobPulse",
        layout="wide",
        initial_sidebar_state="expanded"
    )

    st.title("📡 RoverJobPulse")
    st.caption("Automated Python job market monitoring (RemoteOK)")

    df = load_data()

    if df.empty:
        st.warning("No job data available yet. Run the scraper first.")
        return

    # ======================
    # Sidebar Filters
    # ======================
    st.sidebar.header("🔎 Filters")

    period_label = st.sidebar.radio(
        "Time range",
        ["Last 7 days", "Last 14 days", "Last 30 days", "All time"],
        index=0
    )

    period_map = {
        "Last 7 days": 7,
        "Last 14 days": 14,
        "Last 30 days": 30,
        "All time": "ALL"
    }

    df_filtered = filter_by_days(df, period_map[period_label])

    search = st.sidebar.text_input("Search title or company")

    if search:
        df_filtered = df_filtered[
            df_filtered["title"].str.contains(search, case=False, na=False)
            | df_filtered["company"].str.contains(search, case=False, na=False)
        ]

    # ======================
    # Metrics
    # ======================
    col1, col2, col3 = st.columns(3)

    col1.metric("Total Jobs Collected", len(df))
    col2.metric("Jobs in Selected Period", len(df_filtered))

    last_scrape = df["date_scraped"].max()
    col3.metric(
        "Last Scrape",
        last_scrape.strftime("%Y-%m-%d %H:%M UTC")
    )

    st.divider()

    # ======================
    # Trend Chart
    # ======================
    st.subheader("📈 Job Collection Trend")

    trend = (
        df_filtered
        .groupby(df_filtered["date_scraped"].dt.date)
        .size()
        .reset_index(name="count")
    )

    if trend.empty:
        st.info("No job data available for the selected time range.")
    else:
        st.line_chart(
            trend.set_index("date_scraped")["count"]
        )

    # ======================
    # Top Companies
    # ======================
    st.subheader("🏢 Top Hiring Companies")

    top_companies = df_filtered["company"].value_counts().head(10)

    if top_companies.empty:
        st.info("No company data available for the selected time range.")
    else:
        st.bar_chart(top_companies)

    # ======================
    # Job Listings Table
    # ======================
    st.subheader("📋 Job Listings")

    if df_filtered.empty:
        st.warning("No jobs found for the selected filters.")
    else:
        st.dataframe(
            df_filtered[
                [
                    "title",
                    "company",
                    "location",
                    "tags",
                    "date_posted",
                    "job_url",
                ]
            ]
            .sort_values("date_posted", ascending=False),
            width="stretch",
            hide_index=True
        )


if __name__ == "__main__":
    main()

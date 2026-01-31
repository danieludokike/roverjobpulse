
import streamlit as st
import pandas as pd
import sqlite3
from pathlib import Path

DB_PATH = Path("database/roverjobpulse.db")


def load_data():
    conn = sqlite3.connect(DB_PATH)
    df = pd.read_sql("SELECT * FROM jobs", conn)
    conn.close()

    # Convert dates
    df["date_posted"] = pd.to_datetime(df["date_posted"], errors="coerce")
    df["date_scraped"] = pd.to_datetime(df["date_scraped"], errors="coerce")

    return df


def main():
    st.set_page_config(page_title="RoverJobPulse", layout="wide")

    st.title("RoverJobPulse — Python Job Market Monitor")
    st.caption("Automated tracking of Python job listings (RemoteOK)")

    df = load_data()

    if df.empty:
        st.warning("No job data available yet. Run the scraper first.")
        return

    # ---- Metrics ----
    total_jobs = len(df)
    jobs_today = df[
        df["date_scraped"].dt.date == pd.Timestamp.utcnow().date()
    ].shape[0]

    col1, col2 = st.columns(2)
    col1.metric("Total Jobs Collected", total_jobs)
    col2.metric("Jobs Collected Today", jobs_today)

    st.divider()

    # ---- Jobs over time ----
    st.subheader("Jobs Collected Over Time")
    jobs_by_day = (
        df.groupby(df["date_scraped"].dt.date)
        .size()
        .reset_index(name="count")
    )

    st.line_chart(jobs_by_day.set_index("date_scraped")["count"])

    # ---- Top companies ----
    st.subheader("Top Hiring Companies")
    top_companies = df["company"].value_counts().head(10)
    st.bar_chart(top_companies)

    # ---- Job listings ----
    st.subheader("Job Listings")
    search = st.text_input("Search by title or company")

    if search:
        filtered_df = df[
            df["title"].str.contains(search, case=False, na=False)
            | df["company"].str.contains(search, case=False, na=False)
        ]
    else:
        filtered_df = df

    st.dataframe(
        filtered_df[
            [
                "title",
                "company",
                "location",
                "tags",
                "date_posted",
                "job_url",
            ]
        ],
        use_container_width=True,
    )


if __name__ == "__main__":
    main()

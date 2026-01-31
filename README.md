# RoverJobPulse

RoverJobPulse is an automated Python system that tracks the Python job market by collecting live job listings daily, storing them in a structured database, and presenting insights through an interactive dashboard.

The project is designed to simulate a real-world production data pipeline, covering web scraping, automation, data persistence, analytics, and visualization.

## Project Overview

Job listings change frequently and are often scattered across multiple platforms. This makes it difficult to track trends, demand, and opportunities over time.

RoverJobPulse solves this by:

Automatically collecting Python-related job listings

Persisting data for historical analysis

Preventing duplicate records

Providing a live, filterable dashboard for insights

### Key Features

. Automated job scraping using the RemoteOK API

. Persistent storage with SQLite

. Duplicate prevention using database constraints

. Incremental historical data collection

. Interactive Streamlit dashboard

. Time-range filtering (7 / 14 / 30 days, all time)

. Search by job title or company

. Timezone-aware datetime handling

### Design Philosophy

Incremental data collection
The system does not rely on external historical APIs. Instead, it builds its own dataset over time by collecting daily snapshots of live job listings.

#### Separation of concerns
Scraping, persistence, scheduling, analytics, and visualization are clearly separated into modules.

### Production-oriented choices
SQLite is used for reliability, deduplication, and efficient querying, with a clear upgrade path to PostgreSQL.

### Project Structure

```roverjobpulse/
│
├── scraper/             
│   ├── base.py
│   └── remoteok.py
│
├── database/          
│   ├── db.py
│   └── models.py
│
├── scheduler/           
│   └── daily.py
│
├── dashboard/          
│   └── app.py
│
├── analytics/          
│
├── notifications/     
│
├── data/
│   ├── raw/
│   └── processed/
│
├── logs/
│
├── main.py            
├── requirements.txt
└── README.md
```

### Tech Stack

Language: Python 3.10+

Data Source: RemoteOK API

HTTP Requests: requests

Storage: SQLite

Data Analysis: pandas

Dashboard: Streamlit

Scheduling: schedule (cron-ready)

### Data Model

Each job record includes:

title

company

location

tags

job_url (unique)

source

date_posted (from job source)

date_scraped (when collected by RoverJobPulse)

This allows accurate trend analysis and time-based filtering.

### Installation & Setup
1. Clone the repository
``` git clone https://github.com/danieludokike/roverjobpulse.git```        
```cd roverjobpulse```

2. Create virtual environment
```python -m venv env```
```source env/bin/activate```  # Linux / macOS
```env\Scripts\activate```      # Windows

3. Install dependencies
```pip install -r requirements.txt```

4. Running the Scraper
```python main.py```


#### This will:

Fetch current Python jobs

Store new jobs in SQLite

Skip duplicates automatically

#### Running the Scheduler (Automation)
```python scheduler/daily.py```


The scheduler runs the scraper automatically at a configured time (UTC).

### Running the Dashboard
```cd dashboard```
```streamlit run app.py```


Open the browser at:

```http://localhost:8501```

### Dashboard Capabilities

View total jobs collected

Filter jobs by:

Last 7 days

Last 14 days

Last 30 days

All time

Visualize job collection trends

See top hiring companies

Search jobs by title or company

View historical data built over time

### Future Enhancements

Email notifications for new jobs

Job age analysis (posted vs scraped)

Multi-source job scraping

PostgreSQL migration

Dockerized deployment

CI/CD pipeline

Portfolio Value

RoverJobPulse demonstrates:

Clean Python architecture

Automation and scheduling

Database design & deduplication

Time-series data handling

Analytics and visualization

Production-ready engineering mindset

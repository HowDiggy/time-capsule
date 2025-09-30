# Project: Digital Time Capsule

A personal data engineering project designed to capture a daily snapshot of the world. This pipeline collects data from various public APIs and sources, processes it, and stores it in a data lake, creating a queryable "time capsule" for each day.

---

## Overview

The goal of this project is to build a resilient, automated data pipeline that runs daily to collect a variety of data points, including:

* **Financial Data:** Opening and closing prices for the top 25 stocks by market cap.
* **Meteorological Data:** Weather conditions for the top 25 global cities.
* **News & Culture:** Top headlines from major news sources and trending topics from social media.
* **Sentiment Analysis:** Processing text-based data to gauge public sentiment.

The entire pipeline is orchestrated using **Dagster**, with data stored as Parquet files in an S3-compatible object store.

---

## Key Features

* **Automated Daily Ingestion:** Runs on a schedule to fetch new data every day.
* **Asset-Based Orchestration:** Leverages Dagster's software-defined assets for a declarative and observable pipeline.
* **Scalable Storage:** Uses MinIO for a self-hosted, S3-compatible data lake.
* **Efficient Querying:** Data is stored in the columnar Parquet format, enabling fast analytical queries with DuckDB.
* **Modular Design:** Each data source is a distinct, testable asset.

---

## Tech Stack

* **Orchestrator:** [Dagster](https://dagster.io/)
* **Language:** Python 3.10+
* **Dependency Management:** [Poetry](https://python-poetry.org/)
* **Data Storage:** [MinIO](https://min.io/) (S3-compatible object storage)
* **Query Engine:** [DuckDB](https://duckdb.org/)
* **Deployment:** Docker, Kubernetes (via Helm), ArgoCD

---

## Getting Started

### Prerequisites

* Python 3.10+
* Poetry installed
* Docker (for eventual containerization)

### 1. Clone the Repository

```bash
git clone git@github.com:HowDiggy/time-capsule.git
cd time-capsule
```

### 2. Install Dependencies

This project uses Poetry to manage dependencies. Run the following command to create a virtual environment and install the required packages.

```bash
poetry install
```

### 3. Configure Environment Variables

Create a `.env` file in the root of the project by copying the example file.

```bash
cp .env.example .env
```

Now, edit the `.env` file to add your API keys and any other necessary configuration.

### 4. Run the Dagster UI

To start the local Dagster webserver and view the asset graph, run:

```bash
dagster dev -m time_capsule
```

Navigate to `http://localhost:3000` in your browser. From the UI, you can manually materialize assets to test the pipeline.

---

## Project Roadmap

This project is being developed in iterative phases:

* [x] **Phase 1: Foundation:** Local project setup and basic Dagster asset definition.
* [ ] **Phase 2: Core Assets:** Implement ingestion for primary data sources (weather, news) and configure local Parquet storage.
* [ ] **Phase 3: Scale Out:** Add remaining data sources and implement sentiment analysis.
* [ ] **Phase 4: Productionize:** Deploy to a Kubernetes cluster and schedule for automated daily runs.
* [ ] **Phase 5: Access Layer:** Build a FastAPI and frontend to query and explore the time capsule data.
# Enrollment Data Cleaning and Airtable Integration

## Overview

This repository contains my solution to a technical exercise focused on cleaning, structuring, and reviewing enrollment data using Airtable. The goal of the exercise is to support a high-level review of program engagement and participation patterns across cities.

---

## Problem Context

The provided CSV represents leader participation in one or more programs. Each record includes compound fields describing leader information, course enrollments, associated cities, and completion status.

The data is not analysis-ready in its original form and requires normalization before meaningful review.

---

## Data Preparation

The raw CSV contained multiple non-atomic, delimiter-separated fields that required cleaning and normalization.

### Running the Script

```bash
# Install dependencies
pip install pandas

# Run the cleaning script
python scripts/clean_data.py
```

### Output

The script generates three normalized CSV files in the `data/` directory:

* `leaders.csv`
  Unique leaders with contact information and associated city

* `cities.csv`
  Unique cities with population and region data

* `enrollments.csv`
  One row per course enrollment, including dates, program center, and completion percentage

### Data Parsing

The script parses the following compound fields from the source CSV:

* **leader_info**: `Name|email|Title:Role|Tenure`
* **city_data**: `City, ST|Population:XXXXXX|Region:RegionName`
* **course_enrollment**: `Course Name~Duration~Start Date~End Date`
  (pipe-separated for multiple courses)
* **completion_status**: `Completed:Course Name:XX%`
  (comma-separated for multiple courses)
* **program_center**: Comma-separated list aligned by index with course enrollments

---

## Airtable Data Model

The cleaned CSVs are imported into Airtable as three related tables: **Leaders**, **Cities**, and **Enrollments**.

Relationships are modeled using Airtable link fields:

* **Leaders -> Cities**
  Each leader is linked to a single city record.

* **Enrollments -> Leaders**
  Each enrollment links to one leader.

* **Enrollments -> Cities**
  Each enrollment links to one city.

---

## Definitions and Assumptions

* **Engagement** is defined as the volume of enrollments and average completion percentage associated with a city.
* Cities with very small numbers of enrollments may show high completion averages that are not representative of broader participation.

---

## Summary Observations

To support review of engagement and completion patterns, the following Airtable views are created:

* **Cities by Highest Enrollment**
  Cities sorted by total number of enrollments, derived from rollups on the Enrollments table. 
  
  Top 3 by enrollment were: 
  - Baltimore, MD
  - San Francisco, CA
  - Austin, TX

* **Cities by Highest Completion**
  Cities sorted by average completion percentage, with a filter applied to require a minimum number of enrollments. This avoids over-interpreting completion rates based on very small sample sizes.

  Top 3 by completion percentage were: 
  - Seattle, WA
  - Austin, TX
  - San Francisco, CA


These views provide an overview of where participation is concentrated and where enrolled participants demonstrate strong follow-through.

---

## Design Decisions

* **Normalization**
  Non-atomic fields in the source CSV are split into separate tables to reduce duplication and improve clarity.

* **Identifiers vs. relationships**
  CSV outputs use stable textual identifiers for import and traceability, while Airtable link fields represent relationships.

* **Completion percentages**
  Completion values are stored as whole-number percentages to match the source data. No display-only percentage fields are used in order to preserve accurate rollup behavior.

* **Primary fields**
  Airtable primary fields are treated as human-readable labels rather than enforced keys, consistent with Airtable’s data model.

---

## Repository Structure

```
/
├── data/
│   ├── enrollment_data_raw.csv   # Original data
│   ├── leaders.csv               # Output: unique leaders
│   ├── cities.csv                # Output: unique cities
│   └── enrollments.csv           # Output: course enrollments
├── scripts/
│   └── clean_data.py             # Data cleaning script
└── README.md
```

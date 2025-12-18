# Enrollment Data Cleaning and Airtable Integration

## Overview

This repository contains my solution to a technical exercise focused on cleaning, structuring, and reviewing enrollment data using Airtable. The goal of the exercise is to support a high-level review of program engagement and participation patterns across cities, program centers, and individual course offerings.

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

The cleaned CSVs are imported into Airtable as three related tables: **Leaders**, **Cities**, and **Enrollments**. Additional dimension tables for **Program Centers** and **Courses** are created directly within Airtable using link fields.

Relationships are modeled using Airtable link fields:

* **Leaders → Cities**
  Each leader is linked to a single city record.

* **Enrollments → Leaders**
  Each enrollment links to one leader.

* **Enrollments → Cities**
  Each enrollment links to one city.

* **Enrollments → Program Centers**
  Each enrollment links to one program center.

* **Enrollments → Courses**
  Each enrollment links to one course.

---

## Analysis

See [analysis.md](analysis.md) for engagement findings and summary observations addressing the Dean's questions about impact and city engagement.

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

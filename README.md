# Enrollment Data Cleaning and Airtable Integration

## Overview

This repository contains my solution to a technical exercise focused on cleaning, structuring, and reviewing enrollment data using Airtable. The work is framed as a simulated internal request and emphasizes clear assumptions, maintainable data modeling, and practical decision‑making.

## Problem Context

The provided CSV represents leader participation in one or more programs. Each record includes compound fields describing leader information, course enrollments, associated cities, and completion status.


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
- `leaders.csv` - Unique leaders with contact info and location
- `cities.csv` - Unique cities with population and region data
- `enrollments.csv` - One row per course enrollment with completion status

### Data Parsing

The script parses the following compound fields:
- **leader_info**: `Name|email|Title:Role|Organization`
- **city_data**: `City, ST|Population:XXXXXX|Region:RegionName`
- **course_enrollment**: `Course Name~Duration~Start Date~End Date` (pipe-separated for multiple)
- **completion_status**: `Completed:Course Name:XX%` (comma-separated for multiple)
- **program_center**: Comma-separated list matched by index to courses


## Airtable Data Model

The cleaned CSVs are imported into Airtable as three related tables: Leaders, Cities, and Enrollments.

Relationships are modeled using Airtable link fields rather than embedded text values:

- **Leaders → Cities**: Each leader is linked to a single city record.
- **Enrollments → Leaders**: Each enrollment links to one leader.
- **Enrollments → Cities**: Each enrollment links to one city.

During import, stable identifier columns (e.g., `leader_email`, `city_state`) are used to resolve links. These identifier fields are retained as audit references, while link fields are treated as the authoritative relationships within Airtable.

## Definitions and Assumptions


## Summary Observations


## Repository Structure

```
/
├── data/
│   ├── enrollment_data_raw.csv   # Original data
│   ├── leaders.csv                # Output: unique leaders
│   ├── cities.csv                 # Output: unique cities
│   └── enrollments.csv            # Output: course enrollments
├── scripts/
│   └── clean_data.py              # Data cleaning script
└── README.md
```

## Design Decisions

- **Normalization**: Non-atomic fields in the source CSV are split into separate tables to avoid duplication and improve clarity.
- **Identifiers vs. relationships**: CSV outputs use stable textual identifiers (e.g., email, city/state) while Airtable link fields represent relationships.
- **Completion percentages**: Completion values are stored as whole-number percentages to match the source data. A derived display field is used in Airtable to append `%` for readability.
- **Primary fields**: Airtable primary fields are treated as human-readable labels rather than enforced keys, consistent with Airtable’s data model.

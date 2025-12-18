import pandas as pd
from pathlib import Path

# -----------------------------
# Paths
# -----------------------------
BASE_DIR = Path(__file__).resolve().parents[1]
DATA_DIR = BASE_DIR / "data"

RAW_CSV = DATA_DIR / "enrollment_data_raw.csv"
LEADERS_OUT = DATA_DIR / "leaders.csv"
CITIES_OUT = DATA_DIR / "cities.csv"
ENROLLMENTS_OUT = DATA_DIR / "enrollments.csv"

# -----------------------------
# Load raw data
# -----------------------------
try:
    df = pd.read_csv(RAW_CSV)
except FileNotFoundError:
    print(f"Error: Could not find raw data file at {RAW_CSV}")
    exit(1)
except Exception as e:
    print(f"Error reading CSV file: {e}")
    exit(1)

# -----------------------------
# Helper parsers
# -----------------------------
def parse_leader_info(value):
    """
    Expected format:
    Name|email|Title:Role|Tenure:YYYY-Present
    """
    parts = value.split("|")
    return {
        "leader_name": parts[0].strip(),
        "email": parts[1].strip(),
        "title": parts[2].replace("Title:", "").strip() if len(parts) > 2 else None,
        "tenure": parts[3].replace("Tenure:", "").strip() if len(parts) > 3 else None,
    }


def parse_city_data(value):
    """
    Expected format:
    City, ST|Population:XXXXXX|Region:RegionName
    """
    parts = value.split("|")

    city_state = parts[0].split(",")
    city = city_state[0].strip()
    state = city_state[1].strip() if len(city_state) > 1 else None

    population = None
    region = None

    for part in parts[1:]:
        if part.startswith("Population:"):
            population = int(part.replace("Population:", "").strip())
        elif part.startswith("Region:"):
            region = part.replace("Region:", "").strip()

    return {
        "city": city,
        "state": state,
        "population": population,
        "region": region,
    }


def parse_courses(value):
    """
    Expected format (multiple, pipe-separated):
    Course Name~Duration~Start Date~End Date
    """
    courses = []
    for entry in value.split("|"):
        parts = entry.split("~")
        courses.append({
            "course_name": parts[0].strip(),
            "duration_weeks": parts[1].replace("weeks", "").strip() if len(parts) > 1 else None,
            "start_date": parts[2].strip() if len(parts) > 2 else None,
            "end_date": parts[3].strip() if len(parts) > 3 else None,
        })
    return courses


def parse_completion(value):
    """
    Expected format:
    Completed:Course Name:XX%,Completed:Course Name:YY%
    """
    results = {}
    for entry in value.split(","):
        parts = entry.split(":")
        if len(parts) >= 3:
            course = parts[1].strip()
            percent = parts[2].replace("%", "").strip()
            results[course] = int(percent)
    return results


# -----------------------------
# Process data and build tables
# -----------------------------
leaders = []
cities = {}
enrollments = []

for idx, row in df.iterrows():
    try:
        leader = parse_leader_info(row["leader_info"])
        city = parse_city_data(row["city_data"])

        city_key = f"{city['city']}, {city['state']}"
        cities[city_key] = city

        courses = parse_courses(row["course_enrollment"])
        completion_map = parse_completion(row["completion_status"])

        program_centers = [p.strip() for p in row["program_center"].split(",")]

        leaders.append({
            **leader,
            "city_state": city_key,
        })

        for i, course in enumerate(courses):
            enrollments.append({
                "leader_email": leader["email"],
                "course_name": course["course_name"],
                "duration_weeks": course["duration_weeks"],
                "start_date": course["start_date"],
                "end_date": course["end_date"],
                "completion_percent": completion_map.get(course["course_name"]),
                "program_center": program_centers[i] if i < len(program_centers) else None,
                "city_state": city_key,
            })
    except Exception as e:
        print(f"Warning: Failed to parse row {idx}: {e}")
        continue

# -----------------------------
# Output tables
# -----------------------------
leaders_df = pd.DataFrame(leaders).drop_duplicates(subset=["email"])
cities_df = pd.DataFrame(cities.values()).drop_duplicates(subset=["city", "state"])
enrollments_df = pd.DataFrame(enrollments)

try:
    leaders_df.to_csv(LEADERS_OUT, index=False)
    cities_df.to_csv(CITIES_OUT, index=False)
    enrollments_df.to_csv(ENROLLMENTS_OUT, index=False)
except Exception as e:
    print(f"Error writing output files: {e}")
    exit(1)

print("Data cleaning complete.")
print(f"Wrote {len(leaders_df)} leaders")
print(f"Wrote {len(cities_df)} cities")
print(f"Wrote {len(enrollments_df)} enrollments")

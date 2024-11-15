"""Process combined csv file."""

import csv
import sys
import datetime


# example row
# {'Show Name': 'Macro Horizons', 'Episode ID': '1000676248116', 'Episode GUID': 'c9a5fe44-9deb-11ef-884f-cfb00435c437', 'Episode Number': '', 'Episode Title': 'Dear Santa Pause...', 'Release Date': '2024-11-08', 'Duration': '1189', 'Unique Listeners': '430', 'Unique Engaged Listeners': '360', 'Plays': '1972', 'Average Consumption': '0.8997770258376201'}

keys = [
    "Show Name",
    "Episode ID",
    "Episode GUID",
    "Episode Number",
    "Episode Title",
    "Release Date",
    "Duration",
    "Unique Listeners",
    "Unique Engaged Listeners",
    "Plays",
    "Average Consumption",
]

keys_to_drop = [
    "Episode ID",
    "Episode GUID",
    "Episode Number",
    "Unique Engaged Listeners",
]


column_order = [
    "Show Name",
    "Episode Title",
    "Release Date",
    "Duration",
    "Duration (seconds)",
    "Unique Listeners",
    "Plays",
    "Average Consumption",
]


def process(data):
    output = []
    for row in data:
        out_row = {}
        for key in row:
            if key in keys_to_drop:
                continue
            if key == "Duration":
                # nicely formatted `"Duration"` field, which is in seconds to start
                # but should be hh:mm:ss
                duration = int(row["Duration"])
                hours = duration // 3600
                minutes = (duration % 3600) // 60
                seconds = duration % 60
                out_row["Duration (seconds)"] = row["Duration"]
                out_row["Duration"] = f"{hours:02d}:{minutes:02d}:{seconds:02d}"
                continue

            out_row[key] = row[key]
        output.append(out_row)

    def sort_key(row):
        # convert date to yearmonth
        # sort by year desc, then month desc, then show name, then release date desc

        release_date = datetime.datetime.strptime(row["Release Date"], "%Y-%m-%d")
        release_year = release_date.year
        release_month = release_date.month

        return (-release_year, -release_month, row["Show Name"], -release_date.timestamp())

    output.sort(key=sort_key)

    return output


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python process_combined.py <in.csv> <out.csv>")
        sys.exit(1)

    in_file = sys.argv[1]
    out_file = sys.argv[2]
    with open(in_file, "r") as f:
        reader = csv.DictReader(f)
        data = [row for row in reader]

    data2 = process(data)

    with open(out_file, "w") as f:
        writer = csv.DictWriter(f, fieldnames=column_order)
        writer.writeheader()
        writer.writerows(data2)

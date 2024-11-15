#!/bin/bash

set -e

source venv/bin/activate
python combine_csvs.py /Users/Jonah/Documents/BMO\ podcast\ CSV/*.csv
python process_combined.py combined.csv processed.csv
python upload_csv_to_sheets.py processed.csv

echo "Done!"

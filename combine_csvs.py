# Read a list of CSV filepaths from the command line,
# and write the contents of all of them to a single CSV file.
# All CSV files have the same set of headers

import csv
import sys

# Check that the user has provided at least one CSV file
if len(sys.argv) < 2:
    print("Usage: python combine_csvs.py file1.csv file2.csv ...")
    sys.exit(1)

# Open the output file
with open("combined.csv", "w") as output_file:
    output_writer = csv.writer(output_file)

    # Loop over the input files
    for i, input_filename in enumerate(sys.argv[1:]):
        with open(input_filename, "r") as input_file:
            input_reader = csv.reader(input_file)

            # Write the headers to the output file if it's the first file
            if i == 0:
                output_writer.writerow(next(input_reader))
            else:
                # Skip the headers in the other files
                next(input_reader)

            # Write the data rows to the output file
            for row in input_reader:
                output_writer.writerow(row)

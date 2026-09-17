# Script to calculate historical Ne, which is the harmonic mean of Ne estimates older than 10 kya, as defined in Wilder et al. (2023).
# Input is one or more output files from MSMC2
# Usage: python msmc2_historical_Ne.py sample1.consensus.final.txt sample2.consensus.final.txt ...
# change mutation rate (mu) and generation time as needed
# Author: Jonas Lescroart with ChatGPT
# Date: 22 July 2023
# Update 27 October 2024: removed oldest time intervals from harmonic mean calculation. Added Ne of most recent time interval to output file.

import numpy as np
import sys

mu = 8.6 * 10 ** -9
generation_time = 3.8

def harmonic_mean(Ne, time):
    filtered_data = np.array([ne for ne, t in zip(Ne, time) if t > 10000])
    return len(filtered_data) / np.sum(1.0 / filtered_data)

def process_file(filename):
    # Read the input data from the file
    data = np.genfromtxt(filename, skip_header=1, usecols=(3), dtype=float)
    left_time_boundary = np.genfromtxt(filename, skip_header=1, usecols=(1), dtype=float)

    # Transform the 'lambda' column and calculate 'Ne'
    Ne = (1 / data) / (2 * mu)

    # Transform the 'left_time_boundary' column and calculate 'time'
    time = left_time_boundary / mu * generation_time

    # Get Ne of most recent time interval
    recent_Ne = Ne[0]

# Calculate the harmonic mean of 'Ne' for 'time' > 10000
#    h_mean = harmonic_mean(Ne, time)
    # To ignore the 2*1 and 3*1 time intervals in the oldest part of the track, which often behaves weird, use instead:
    h_mean = harmonic_mean(Ne[:-5], time[:-5])

    # Extract the sample name from the file name
    sample_name = filename.split('.consensus.final.txt')[0]

    return sample_name, h_mean, recent_Ne

def main():
    if len(sys.argv) < 2:
        print("Usage: python script.py input_file1 [input_file2 ...]")
        sys.exit(1)

    output_filename = "harmonic_means_output.txt"

    with open(output_filename, 'w') as output_file:
        output_file.write("sample\thistorical_Ne\trecent_Ne\n")
        for input_file in sys.argv[1:]:
            sample_name, h_mean, recent_Ne = process_file(input_file)
            output_file.write(f"{sample_name}\t{h_mean}\t{recent_Ne}\n")

    print("Output written to", output_filename)

if __name__ == "__main__":
    main()


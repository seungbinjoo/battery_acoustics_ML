#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul 17 12:19:12 2023

@author: seungbinjoo
"""

# HOW TO RUN THE CODE:
    # 1. Change directory in line 43 to a folder which contains folders containing the raw waveform csv files. This directory can have
    # miscellaneous files, e.g. other TXT files, but cannot have folders which do not contain raw waveform csv files.
    # 2. Change "experiment_name" to something appropriate (line 49).
    # 3. Check the code for axes limits, line thickness, aspect ratio, etc. of each of the unfiltered, filtered and FFT plots. Check that they are set to the desired values.
    # 4. Run the code.
    
# IMPORTANT NOTE:
    # The code assumes all the raw data folders containing raw waveform csv files are named like so: "DDMMYYYY_EXPERIMENT_NAME_##dB_..." (i.e. file names must start with 8 digit dates)
    # Code also assumes that one experiment is performed per day. If this is not the case then change the code and file names like so:
        # Name the folders like so: "DDMMYYYY_1_EXPERIMENT_NAME_##dB_...", "DDMMYYYY_2_EXPERIMENT_NAME_##dB_..." and so on
        # Then, change line 73 and 75 code: change [:8] to [:10]

# Import relevant libraries

import matplotlib.pyplot as plt
import pandas as pd
import scipy
from scipy import signal
from scipy.signal import butter
from scipy.fft import fft, fftfreq
import numpy as np
from scipy.signal import find_peaks
import os
import csv
import shutil
import math
import re


# /////////////////////////////////////////////////////// FOLDER ORGANIZATION ///////////////////////////////////////////////////////

# Set cwd to file path with all the folders containing AE waveform data --> print cwd
# NOTE: if multiple experiments were run each day, code and file names may need to be modified accordingly
os.chdir("/Users/seungbinjoo/Desktop/UCL FUSE Internship/Work/5 Experiments/Cylindrical Cell AE Matrix Experiment/Cylindrical Cell AE Matrix Experiment Pristine 1C/AEwin Data")
cwd = os.getcwd()
print(cwd)


# What is the name of the experiment?
experiment_name = 'Cylindrical_Cell_Experiment_1C'


# get the number of experiments by counting the number of folders in cwd containing wavform data
num = len(next(os.walk(cwd))[1])


# creating a list with names of the original folders
def get_folder_names(directory):
    folder_names = [] # initialization
    for item in os.listdir(directory): # os.listdir() gives a list of strings containing all file names in a certain directory
        item_path = os.path.join(directory,item) # item_path is the filepath to an item in the directory
        if os.path.isdir(item_path): # checking whether the item itself is a directory, i.e. a folder
            folder_names.append(item) # if so, then add the name to our list since it is a folder
    return folder_names

folder_names = get_folder_names(cwd)


# name the folders according to their dates + experiment name + threshold
for i in range(num):
    index_dB = folder_names[i].find('dB')
    if index_dB != -1:
        threshold = folder_names[i][index_dB-2:index_dB+2]
        folder_names[i] = folder_names[i][:8] + '_' + experiment_name + '_' + threshold
    elif index_dB == -1:
        folder_names[i] = folder_names[i][:8] + '_' + experiment_name
    i=i+1


# Make a new folder called Waveforms Processed in cwd and inside that folder put our new folders
path = "./Waveforms Processed" # ./ means current directory
os.makedirs(path, exist_ok=True)

for items in folder_names:
    new_path = os.path.join(path, items)
    os.makedirs(new_path, exist_ok=True)


# Make sub folders which will contain unfiltered, filtered and FFT
new_folder_names = os.listdir("./Waveforms Processed")
new_folder_names.sort()
sub_folder_names = ['Unfiltered Waveform', 'Filtered Waveform', 'FFT']

for folder in new_folder_names:
    folder_path = os.path.join("./Waveforms Processed", folder)
    for sub_folder in sub_folder_names:
        sub_folder_path = os.path.join(folder_path, sub_folder)
        os.makedirs(sub_folder_path, exist_ok=True)



# ////////////////////////////////////////////////////// UNFILTERED WAVEFORM ///////////////////////////////////////////////////////

# Function which will be used to number the title of each plot by extracting the number associated with each waveform
# In this function, we define a regular expression pattern r'_(\d+)_ that matches the first integer between two underscores.
# The re.findall() function is used to find all occurrences of this pattern in the string. We then extract the last match
# (the first integer between two underscores from the end of the string) and convert it to an integer using int().
# If there is no integer between two underscores in the string, the function returns None.
def find_first_integer_between_underscores(s):
    pattern = r'_(\d+)_'
    match = re.search(pattern, s[::-1])
    if match:
        integer_str = match.group(1)[::-1]
        return int(integer_str)
    else:
        return None


# Set the current working directory
current_dir = os.getcwd()

# Path to the raw data folder
raw_data_dir = current_dir

# Path to the processed data folder
processed_data_dir = os.path.join(current_dir, "Waveforms Processed")

# Get a list of raw data folders
raw_data_folders = [f for f in os.listdir(raw_data_dir) if os.path.isdir(os.path.join(raw_data_dir, f))]
raw_data_folders.remove('Waveforms Processed')
raw_data_folders.sort()

# Iterate over each raw data folder
i = 0
for folder in raw_data_folders:
    raw_data_folder = os.path.join(raw_data_dir, folder)
    
    # Get a list of CSV files in the raw data folder
    csv_files = [f for f in os.listdir(raw_data_folder) if f.endswith('.csv')]
    csv_files.sort()
    
    # Process each CSV file
    for file in csv_files:
        csv_file = os.path.join(raw_data_folder, file)
        processed_file = os.path.join(processed_data_dir, new_folder_names[i], "Unfiltered Waveform", file)
        
        # initialize variables to plot
        x = []
        y = []
        
        with open(csv_file, 'r') as f_in, open(processed_file, 'w', newline='') as f_out:
            reader = csv.reader(f_in)
            writer = csv.writer(f_out)
            
            # Skip the first 11 rows, which is just meta data info from the experiment
            for _ in range(11):
                next(reader)
            
            # Modify and write the rows to the processed file
            # Insert time in the first column (multiples of the sampling period) and in the second column write the CSV waveform amplitude data
            rows = []
            header_row = next(reader)
            
            writer.writerow(['Time (us)', 'Voltage (V)'])
            
            j=0
            for row in reader:
                row.insert(0,(j*0.0000002000)*1000000) # converting to micro seconds
                rows.append(row)
                writer.writerow(row)
                j=j+1
        
            # Obtain x and y values to plot from the csv file
            x = [row[0] for row in rows]
            y = [row[1] for row in rows] # y is a list of strings
            y = [eval(i) for i in y] # turn list of strings into list of integers
        
        waveform_num = find_first_integer_between_underscores(csv_file)
        
        # Plot and save the figure for unfiltered waveform
        # NOTE: waveforms here have a pre-trigger of 2k --> 2048 data points per waveform,
        # so time axis plot limits is from 0 to 409.6 us. If pre-trigger is different, modify the code accordingly.
        # Most important information of waveform occurs in the first 120 us of the waveform, so axes limits can be changed to these numbers.
        fig, ax = plt.subplots(figsize=(12, 6))
        ax.plot(x,y,linewidth=0.7, color='tab:blue')
        ax.set_xlim([0, 409.6])
        ax.locator_params(axis='x', nbins=12)
        ax.locator_params(axis='y', nbins=7)
        ax.set_xlabel('Time (us)')
        ax.set_ylabel('Voltage (V)')
        ax.set_title('Unfiltered Waveform '+str(waveform_num), fontsize=16)
        plt.grid() # add grid lines
        plt.savefig(processed_file[:-4]+'.png', dpi=120)
        plt.close()  # Close the current plot before the next iteration
         
    i = i + 1
    
    

# ////////////////////////////////////////////////////// FILTERED WAVEFORM /////////////////////////////////////////////////////////

# Apply digital band pass butterworth filter 50 kHz - 1 MHz

# Create filter
# filter order = 4 --> sharpness of roll-off at cutoff frequencies
# 50 kHz and 1Mhz are low cut and high cut frequencies
# fs is the sampling frequency --> obtained from 1/0.0000002000 = 5000000
# sos parameter specifies that the filter design should be in the "second-order sections" (SOS) format, which is more numerically stable for higher-order filters
sos = butter(8, [50000, 1000000], 'bandpass', fs=5000000, output='sos')

# Set up source and destination folders for filtering the waveforms
unfiltered_data_dir = os.path.join(current_dir, "Waveforms Processed")
filtered_data_dir = os.path.join(current_dir, "Waveforms Processed")

# Get CSV files from unfiltered waveform folders, apply filter and then write new csv file into filtered waveform folders
i = 0
for folder in new_folder_names:
    unfiltered_data_folder = os.path.join(unfiltered_data_dir, folder,"Unfiltered Waveform")
    
    csv_files = [f for f in os.listdir(unfiltered_data_folder) if f.endswith('.csv')]
    csv_files.sort()
    
    for file in csv_files:
        csv_file = os.path.join(unfiltered_data_folder, file)
        filtered_file = os.path.join(filtered_data_dir, new_folder_names[i], "Filtered Waveform", file)

        # initialize variables to plot
        x = []
        y = []

        with open(csv_file, 'r') as f_in, open(filtered_file, 'w', newline='') as f_out:
            reader = csv.reader(f_in)
            writer = csv.writer(f_out)
            
            next(reader) # skip header row
            
            for row in reader:
                x.append(float(row[0]))
                y.append(float(row[1]))
            
            # apply filter to the y values
            filtered = signal.sosfilt(sos, y)
            
            # write header and filtered y values to a new csv file and save it
            writer.writerow(['Time (us)', 'Voltage (V)'])
            for t, v in zip(x, filtered):
                writer.writerow([t, v])   
                
        waveform_num = find_first_integer_between_underscores(csv_file)
                
        # Plot and save the figure for filtered waveform
        fig, ax = plt.subplots(figsize=(12, 6))
        ax.plot(x,filtered,linewidth=0.7, color='tab:red')
        ax.set_xlim([0, 409.6])
        ax.locator_params(axis='x', nbins=12)
        ax.locator_params(axis='y', nbins=7)
        ax.set_xlabel('Time (us)')
        ax.set_ylabel('Voltage (V)')
        ax.set_title('Filtered Waveform '+str(waveform_num), fontsize=16)
        plt.grid() # add grid lines
        plt.savefig(filtered_file[:-4]+'.png', dpi=120)
        plt.close()

    i = i + 1



# //////////////////////////////////////////////////// FAST FOURIER TRANSFORM ////////////////////////////////////////////////////

# Apply Fast Fourier Transform to the filtered waveform

SAMPLE_RATE = 5000000   # Hertz
# DURATION = 0.0004  # Seconds
# N = SAMPLE_RATE * DURATION

# Set up source and destination folders for filtering the waveforms
filtered_data_dir = os.path.join(current_dir, "Waveforms Processed")
FFT_data_dir = os.path.join(current_dir, "Waveforms Processed")

# Get CSV files from filtered waveform folders, apply FFT and then write new csv file into FFT folders
i = 0
for folder in new_folder_names:
    filtered_data_folder = os.path.join(filtered_data_dir, folder,"Filtered Waveform")

    csv_files = [f for f in os.listdir(filtered_data_folder) if f.endswith('.csv')]
    csv_files.sort()

    for file in csv_files:
        csv_file = os.path.join(filtered_data_folder, file)
        FFT_file = os.path.join(FFT_data_dir, new_folder_names[i], "FFT", file)
    
        # initialize variables to plot
        x = []
        y = []
    
        with open(csv_file, 'r') as f_in, open(FFT_file, 'w', newline='') as f_out:
            reader = csv.reader(f_in)
            writer = csv.writer(f_out)
            
            next(reader)  # Skip the header row
            
            for row in reader:
                x.append(float(row[0]))  # Assuming the x-values are in the first column
                y.append(float(row[1]))

            # This will give complex Fourier transform: yf is the amplitudes of the frequencies and xf is the frequencies
            yf = fft(y)
            xf = fftfreq(len(y), 1 / SAMPLE_RATE)
            xf = xf/1000 # convert to kHz so plots are easier to visualize
            
            # Consider only the positive frequency components
            positive_frequencies_mask = xf >= 0
            xf_positive = xf[positive_frequencies_mask]
            magnitude_positive = np.abs(yf[positive_frequencies_mask])
            
            # write header and FFT values to a new csv file and save it
            writer.writerow(['Frequency (kHz)', 'Amplitude (V)'])
            
            for f, a in zip(xf_positive, magnitude_positive):
                writer.writerow([f, a]) 
        
        waveform_num = find_first_integer_between_underscores(csv_file)
                
        # Plot and save the figure for FFT of waveform
        # CSV data files contain full frequency spectrum, but only part of the frequency spectrum is plotted since we're interested in signals between 0.1 MHz to 1.0 MHz
        fig, ax = plt.subplots(figsize=(12, 6))
        ax.plot(xf_positive, magnitude_positive, linewidth=0.7, color='tab:green')  # Plot positive frequencies
        ax.set_xlim([0, 400]) # We only really care about frequencies in this range 50 kHz to 1000 kHz, so plot axes limits accordingly
        ax.locator_params(axis='x', nbins=10)
        ax.locator_params(axis='y', nbins=7)
        ax.set_xlabel('Frequency (kHz)')
        ax.set_ylabel('Amplitude (V)')
        ax.set_title('FFT '+str(waveform_num), fontsize=16)
        plt.grid() # add grid lines
        plt.savefig(FFT_file[:-4]+'.png', dpi=120)
        plt.close()
    
    i = i + 1
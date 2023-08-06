from multiprocessing import Pool
import os
import pandas as pd
import numpy as np
import sys
from glmtools.io.glm import GLMDataset
import time


# Location to focus on
if(len(sys.argv) >= 5):
    area = [int(i) for i in sys.argv[4].split(',')]
else:
    area = [-180,180,90,-90]


# Loads in the GLM data
# Gets the data in the area to focus on
# Creates a dataframe
def getGroups(x):
    # Load glm dataset from file
    temp = GLMDataset(x).dataset
    # Create a mask that's within the area
    mask = np.ones(shape=temp.dims['number_of_groups'],dtype=bool) & ((temp.group_lon >= area[0]) & (temp.group_lon <= area[1]) & (temp.group_lat >= area[3]) & (temp.group_lat <= area[2])).values
    # If there is data, return the dataframe
    if len((compute := temp.group_energy[mask])) != 0:
        groups = compute.to_dataframe('group_energy').drop(['group_parent_flash_id','lightning_wavelength','product_time','group_time_threshold','flash_time_threshold','lat_field_of_view','lon_field_of_view'],axis=1)
        return groups

def getFlashes(x):
        # Load glm dataset from file
        temp = GLMDataset(x).dataset
        # Create a mask that's within the area
        mask = np.ones(shape=temp.dims['number_of_flashes'],dtype=bool) & ((temp.flash_lon >= area[0]) & (temp.flash_lon <= area[1]) & (temp.flash_lat >= area[3]) & (temp.flash_lat <= area[2])).values
        # If there is data, return the dataframe
        if len((compute := temp.flash_energy[mask])) != 0:
            flshs = compute.to_dataframe('flash_energy').drop(['product_time','lightning_wavelength','group_time_threshold','flash_time_threshold','lat_field_of_view','lon_field_of_view'],axis=1)
            flshs['flash_time_ms'] = pd.to_datetime(flshs['flash_time_offset_of_last_event']) - pd.to_datetime(flshs['flash_time_offset_of_first_event'])
            flshs['flash_time_ms'] = flshs['flash_time_ms'].dt.microseconds
            flshs.drop(['flash_time_offset_of_last_event'],axis=1,inplace=True)
            return flshs

def getEvents(x):
    # Load glm dataset from file
    temp = GLMDataset(x).dataset
    # Create a mask that's within the area
    mask = np.ones(shape=temp.dims['number_of_events'],dtype=bool) & ((temp.event_lon >= area[0]) & (temp.event_lon <= area[1]) & (temp.event_lat >= area[3]) & (temp.event_lat <= area[2])).values
    # If there is data, return the dataframe
    if len((compute := temp.event_energy[mask])) != 0:
        evnts = compute.to_dataframe('event_energy').drop(['event_parent_group_id','product_time','lightning_wavelength','group_time_threshold','flash_time_threshold','lat_field_of_view','lon_field_of_view'],axis=1)
        return evnts

# Call this once at start of runtime
def start():
    # Dictionary of records from F_D (File to Date)
    records = {}
    with open('./NCPython/NCPython/F_D.txt') as f:
        for line in f:
            line = line.rstrip('\n')
            key, val = line.split(":")
            records[key] = val

    num = int(sys.argv[1]) # Number of Processes
    folderNum = str(sys.argv[2]) # Which folder to run it on
    baseFolder = f'./NCPython/NCPython/{folderNum}/' # Create path to basefolder
    what = str(sys.argv[3]).lower() # What thing we are searching for

    # Location string
    st = f"{area[0]}_{area[1]}_{area[2]}_{area[3]}_"
    # File output string formatted
    fOut = f"./Data/{records[folderNum].replace('/','_')}_{st}{what}.csv"

    # Determine which function to use
    if what == 'groups':    func = getGroups
    elif what == 'flashes': func = getFlashes
    elif what == 'events':  func = getEvents


    # Make a list of all file paths
    allPaths = []
    for folder in os.listdir(baseFolder):
        for file in os.listdir(baseFolder + folder):
            allPaths.append('{}{}/{}'.format(baseFolder,folder,file))
    # Return the number of processes, which function, the paths, and the output name
    return num, func, allPaths, fOut


# Runs multiple processes on all the paths and puts all the dataframes in a list
# Combines them all into one big csv, outputs as a file
if __name__ == '__main__':
    # Get necessary data
    num, func, allPaths, fOut = start()
    # Start time of process
    starttime = time.time()
    # Create a pool and run the function on all files in paths
    with Pool(processes=num) as p:
        output = p.map_async(func,allPaths).get()
    print("Done with multiple processes",flush=True)
    # Create and concatenate all of the outputs together
    big = pd.concat(output)
    big.to_csv(fOut)
    print(f"took {time.time() - starttime} seconds")

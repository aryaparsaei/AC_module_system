import os
import time
import glob
import shutil
import pandas as pd
import numpy as np
from datetime import datetime

def wait(seconds): #This function simply suspends the code for n number of seconds, n is an input
    time.sleep(seconds)
    return

def create_dummy_data(filename="DummyData.csv", num_samples=10):
    """
    Creates a dummy dataset with specified ranges and saves it as a CSV file.
    """
    data = {
        "SAT": np.round(np.random.uniform(12, 18, num_samples), 2),
        "RAT": np.round(np.random.uniform(18, 26, num_samples), 2),
        "OAT": np.round(np.random.uniform(0, 10, num_samples), 2),
        "HC": np.round(np.random.uniform(0, 100, num_samples), 2),
        "CC": np.round(np.random.uniform(0, 100, num_samples), 2),
        "Hmd": np.round(np.random.uniform(0, 100, num_samples), 2),
        "MB": np.round(np.random.uniform(0, 100, num_samples), 2),
    }
    
    df = pd.DataFrame(data)
    df.to_csv(filename, index=False)
    print(f"Dummy data saved to {filename}")
    return df

def create_zone_data(filename, n, value_range):
    """
    Creates a dummy dataset for zone-level data and saves it as a CSV file.
    """
    prefix = filename.split('.')[0]  # Extract prefix from filename
    columns = [f"{prefix}_{i+1}" for i in range(n)]
    data = {col: [np.round(np.random.uniform(*value_range), 2)] for col in columns}
    df = pd.DataFrame(data)
    df.to_csv(filename, index=False)
    print(f"Zone data saved to {filename}")
    return df

df = create_dummy_data()
for column in df.columns:
    print(f"{column}:")
    print(df[column].tolist(),df.iloc[-1][column])

# Create zone temperature data
zone_tIn_df = create_zone_data("zone_tIn.csv", n=10, value_range=(10, 30))

# Create zone VAV position data
zone_VAV_pos_df = create_zone_data("zone_VAV.csv", n=10, value_range=(0, 100))

SAT = df.iloc[-1]["SAT"]
RAT = df.iloc[-1]["RAT"]
OAT = df.iloc[-1]["OAT"]
HC = df.iloc[-1]["HC"]
CC = df.iloc[-1]["CC"]
Hmd = df.iloc[-1]["Hmd"]
MB = df.iloc[-1]["MB"]

MB_test = []
OAF = []

# Hard Fault Test #1 - Mixing Box
def system_push_AO(HC, CC, Hmd):
    HC = HC
    CC = CC
    Hmd = Hmd

def system_push_MB(MB):
    MB_temp = MB
    MB_test.append(MB_temp)
    

def Calc_OAF():
    OAF_temp = (SAT-RAT)/(OAT-RAT)
    OAF.append(OAF_temp)

def system_observe_1(OAF,MB):
    print("""Compares OAF-MB ratio to AMCA thresholds, 
    and raise error if OAF-MB ratio is outside the threshold""")

#### TEST 1 Implementation ####
system_push_AO(0, 0, 0) # start test, set all actuators to 0
wait(600)

system_push_MB(0)
wait(300)
Calc_OAF()

system_push_MB(25)
wait(300)
Calc_OAF()

system_push_MB(50)
wait(300)
Calc_OAF()

system_push_MB(75)
wait(300)
Calc_OAF()

system_push_MB(100)
wait(300)
Calc_OAF()


def system_observe_1(OAF,MB):
    print("""Compares OAF-MB ratio to AMCA thresholds, 
    and raise error if OAF-MB ratio is outside the threshold""")
    print(f"MB@0%, SAT_expected = {RAT}, SAT_actual = {SAT}")
    print(f"MB@100%, SAT_expected = {OAT}, SAT_actual = {SAT}")


# Hard Fault Test #2 - Heating Coil

def system_observe_2(coil,deltaT):
    print("""Compares deltaT (SAT-RAT) to expected values based on HC/CC settings, 
    and raise error if delta_T is lower than expected""")


#### TEST 2 Implementation ####
deltaT = []
coil = []
system_push_AO(0, 0, 0) # start test, set all actuators to 0
system_push_MB(0)
wait(600) # MAT = RAT
deltaT.append(SAT - RAT) # expected to be 0

heatingSeason = True # based on AHU seasonal operation settings
coolingSeason = False # based on AHU seasonal operation settings

if heatingSeason:
    system_push_AO(50, 0, 0) # set HC to 50
    wait(300)
    deltaT.append(SAT - RAT)

    system_push_AO(100, 0, 0) # set HC to 100
    wait(300)
    deltaT.append(SAT - RAT)

elif coolingSeason:
    system_push_AO(0, 50, 0) # set HC to 50
    wait(300)
    deltaT.append(SAT - RAT)

    system_push_AO(0, 50, 0) # set HC to 100
    wait(300)
    deltaT.append(SAT - RAT)
system_observe_2(deltaT)



# Hard Fault Test #3 - Cooling Coil


# Soft Fault Test #1 - State of Operation


# Soft Fault Test #2 - Mode of Operation


# Soft Fault Test #3 - Supply Air Temperature Setpoint Reset


# Soft Fault Test #4 - Duct Static Pressure Setpoint Reset



#### TEST 1 Mixing BOX ####
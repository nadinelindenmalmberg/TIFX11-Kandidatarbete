import pandas as pd
import numpy as np
import tkinter as tk
from tkinter import filedialog

DATA_FILENAME = '240306_v2_vals_formatted_short.csv'
USE_DATA_FILENAME = False

AXES = ['-x','-y','-z']

if USE_DATA_FILENAME:
    data_file_path = DATA_FILENAME
else:
    root = tk.Tk(); root.withdraw()
    data_file_path = filedialog.askopenfilename(filetypes=[("Formatted qualisys data", "*.csv")])


df = pd.read_csv(data_file_path, header=[0])


def add_avg_new_column(new_name:str, old_names:list, write_over=True,print_info=False):
    if not write_over and new_name+AXES[0] in df:
        return None
    if new_name+AXES[0] not in df:
        print(f'Adding {new_name}')
    for ax in AXES:
        ax_old_names = [s+ax for s in old_names]
        df[new_name+ax] = df[ax_old_names].sum(axis=1)/len(old_names) # adds new column
        if print_info:
            print( df[ax_old_names+[new_name+ax]] )
    
        


add_avg_new_column('LKnee', ['LKneeOut','LKneeIn'])
add_avg_new_column('RKnee', ['RKneeOut','RKneeIn'])

add_avg_new_column('UpperTorso', ['SpineThoracic2', 'Chest'])
add_avg_new_column('NeckBase', ['LShoulderTop', 'RShoulderTop', 'HeadL', 'HeadR'])
add_avg_new_column('CenterHead', ['HeadFront', 'HeadL', 'HeadR'])

add_avg_new_column('RElbow', ['RElbowOut','RElbowIn'])
add_avg_new_column('LElbow', ['LElbowOut','LElbowIn'])

add_avg_new_column('RHand', ['RWristOut','RWristIn'])
add_avg_new_column('LHand', ['LWristOut','LWristIn'])

add_avg_new_column('RForefoot', ['RForefoot2','RForefoot5'])
add_avg_new_column('LForefoot', ['LForefoot2','LForefoot5'])



df.to_csv(data_file_path, index=False)
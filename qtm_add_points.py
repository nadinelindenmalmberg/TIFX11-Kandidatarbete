import pandas as pd
import numpy as np

DATA_FILENAME = '240306_v2_vals_formatted_short.csv'

AXES = ['-x','-y','-z']

df = pd.read_csv(DATA_FILENAME, header=[0])


def add_avg_new_column(new_name:str, old_names:list, write_over=True,print_info=False):
    if not write_over and new_name+AXES[0] in df:
        return None
    if new_name+AXES[0] not in df:
        print(f'Adding {new_name}')
    for ax in AXES:
        ax_old_names = [s+ax for s in old_names]
        df[new_name+ax] = df[ax_old_names].sum(axis=1)/len(old_names)
        if print_info:
            print( df[ax_old_names+[new_name+ax]] )
    
        



add_avg_new_column('RAnkle', ['RAnkleOut','RAnkleIn'])
add_avg_new_column('LAnkle', ['LAnkleOut','LAnkleIn'])
add_avg_new_column('RKnee', ['RKneeOut','RKneeIn'])
add_avg_new_column('LKnee', ['LKneeOut','LKneeIn'])
add_avg_new_column('RWrist', ['RWristOut','RWristIn'])
add_avg_new_column('LWrist', ['LWristOut','LWristIn'])
add_avg_new_column('RElbow', ['RElbowOut','RElbowIn'])
add_avg_new_column('LElbow', ['LElbowOut','LElbowIn'])
add_avg_new_column('RForefoot', ['RForefoot2','RForefoot5'])
add_avg_new_column('LForefoot', ['LForefoot2','LForefoot5'])
add_avg_new_column('RTrochanterMajor', ['RWaistFrontLow','WaistR']) # tänk över så detta är rimligt!!
add_avg_new_column('LTrochanterMajor', ['LWaistFrontLow','WaistL']) # tänk över så detta är rimligt!!



df.to_csv(DATA_FILENAME, index=False)
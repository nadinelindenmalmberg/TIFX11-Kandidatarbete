import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

DATA_FILENAME = 'jonte_labb_fram_output_formatted.csv'

data = pd.read_csv(DATA_FILENAME, header=[0])
NROWS,NCOLS = data.shape
print(data.shape)

row0=data.iloc[0]

ax = plt.axes(projection='3d')
for i in range(1,len(row0),3):
    # plt.plot(row0[i],row0[i+1],'bo')
    ax.plot3D(row0[i],row0[i+1],row0[i+2],'bo') 
    # print(row0[i])
plt.show()

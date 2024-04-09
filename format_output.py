import pandas as pd
import numpy as np


DATA_FILENAME = 'jonte_labb_fram_output.txt'    #måste sluta på .txt
LABEL_FILENAME = 'motionag_labels.txt'

data_array = []
with open(DATA_FILENAME) as f:
    data_array = np.array([float(x) for x in f.read().split(',')])

labels = []
temp_labels = []
with open(LABEL_FILENAME) as f:
    temp_labels = f.readlines()

temp_labels = [x.strip().replace(' ','-') for x in temp_labels]
for label in temp_labels:
    labels.append(label+'-x')
    labels.append(label+'-y')
    labels.append(label+'-z')

data_rows = []
for i in range(0,len(data_array),len(labels)):
    data_rows.append(list(data_array[i:i+len(labels)]))
    # print(data_rows)

data = pd.DataFrame(data_rows, columns=labels)

output_filename = DATA_FILENAME.replace('.txt','_formatted.csv')
data.to_csv(output_filename)

# print(len(labels))
# print(np.array(data_array).shape)
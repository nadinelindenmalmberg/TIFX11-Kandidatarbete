import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.signal import find_peaks

FPS = 100 # frames per second på "kameran"

MARKER_TSV_FILENAME = "240306_v2_vals_formatted.csv"
pos = pd.read_csv(MARKER_TSV_FILENAME, sep=',', header=[0])

TOT_TIME = len(pos.index)  /FPS
START_TIME = 0  *FPS
END_TIME = 10  *FPS


center_of_mass_z = ( np.array(pos['SpineThoracic2-z']) + np.array(pos['SpineThoracic12-z']) + np.array(pos['WaistBack-z']) )/3
# center_of_mass_z = np.array(pos['SpineThoracic12-z'])
peaks = np.array(find_peaks(center_of_mass_z[START_TIME:END_TIME])[0])
inv_peaks = np.array(find_peaks((-1)*center_of_mass_z[START_TIME:END_TIME])[0])


print('CoM freq:', (len(peaks)-1) / ((END_TIME-START_TIME)/FPS)) 

while not len(peaks) == len(inv_peaks):
    if len(peaks) > len(inv_peaks):
        peaks = peaks[:-1]
    elif len(peaks) < len(inv_peaks):
        inv_peaks = inv_peaks[:-1]

print('Average CoM var:',np.average(center_of_mass_z[peaks]-center_of_mass_z[inv_peaks]))
plt.plot(np.array(pos.index)[START_TIME:END_TIME]/FPS,center_of_mass_z[START_TIME:END_TIME])
plt.plot(peaks/FPS,center_of_mass_z[peaks],'or')
plt.plot(inv_peaks/FPS,center_of_mass_z[inv_peaks],'ob')
# plt.savefig('CoM_var.png',dpi=600)
plt.show()

plt.clf()
plt.plot(peaks/FPS,(center_of_mass_z[peaks]-center_of_mass_z[inv_peaks]),'o-')
plt.show()


## Hur man plottar saker fint i python, saxat från M3-kursen
#     plt.clf()
#     plt.plot(YEARS,B3,'brown', label='Mark')
#     plt.plot(YEARS,B1,'lightblue', label='Atmosfär')
#     plt.plot(YEARS,B2,'green', label='Biomassa')
#     plt.plot(YEARS,B4,'darkblue', label='Hav')
#     plt.xlabel('år'); plt.ylabel('Kol-stock'); plt.legend(loc='upper left')
#     plt.title('U7, där β='+str(beta)+' och k='+str(k_const))
#     plt.savefig('U7_beta'+str(int(beta*FPS))+'_k'+str(int(k_const*FPS000))+'.png',dpi=600)
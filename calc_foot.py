import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.signal import find_peaks
from numpy.fft import fft,fftfreq

FPS = 100 # frames per second på "kameran"

MARKER_TSV_FILENAME = "240306_v2_vals_formatted.tsv"
pos = pd.read_csv(MARKER_TSV_FILENAME, sep='\t', header=[0])

TOT_TIME = len(pos.index)  /FPS

########  ÄNDRA DESSA  #########
START_TIME = 0  *FPS
END_TIME = 30  *FPS
################################

TOT_SELECTED_TIME_IN_S = (END_TIME-START_TIME)/FPS

# print(pos)
# pos.to_csv('test.csv')

# print(pos['LForefoot2-z'])
# print(np.array(pos['LForefoot2-z']))

# for x in pos['LForefoot2-z']:
#     if not np.isreal(x):
#         print(x)

# # Minimum för ev. nollnivå
# print(np.min(np.array(pos['LForefoot2-z'])))
# print(np.min(np.array(pos['LForefoot2-z'])))



# plt.plot(np.array(pos.index)[START_TIME:END_TIME]/FPS,np.array(pos['LHeelBack-z'])[START_TIME:END_TIME],label='LHeelBack-z')
# plt.plot(np.array(pos.index)[START_TIME:END_TIME]/FPS,np.array(pos['LForefoot2-z'])[START_TIME:END_TIME],label='LForefoot2-z')

freq = np.array(pos.index)[START_TIME:END_TIME] / (FPS *TOT_SELECTED_TIME_IN_S)
plt.plot(freq,fft(np.array(pos['LHeelBack-z'])[START_TIME:END_TIME]),label='LHeelBack-z-Fourier')

peaks = np.array(find_peaks(pos['LHeelBack-z'][START_TIME:END_TIME], prominence=3)[0])
# plt.plot(peaks/FPS,np.array(pos['LHeelBack-z'])[peaks],'or')
# num_peaks = len(peaks)
print('Strides:',len(peaks))
print(f'Stide freq:  {len(peaks)/(TOT_SELECTED_TIME_IN_S)} st/s     {len(peaks)/(TOT_SELECTED_TIME_IN_S) *60} st/min')

plt.xlabel('sekunder'); plt.ylabel('mm'); plt.legend(loc='upper right')
# plt.savefig('heel_toe_5s.png',dpi=600)
plt.show()




## Hur man plottar saker fint i python, saxat från M3-kursen
#     plt.clf()
#     plt.plot(YEARS,B3,'brown', label='Mark')
#     plt.plot(YEARS,B1,'lightblue', label='Atmosfär')
#     plt.plot(YEARS,B2,'green', label='Biomassa')
#     plt.plot(YEARS,B4,'darkblue', label='Hav')
#     plt.xlabel('år'); plt.ylabel('Kol-stock'); plt.legend(loc='upper left')
#     plt.title('U7, där β='+str(beta)+' och k='+str(k_const))
#     plt.savefig('U7_beta'+str(int(beta*100))+'_k'+str(int(k_const*100000))+'.png',dpi=600)
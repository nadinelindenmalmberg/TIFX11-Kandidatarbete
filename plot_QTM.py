import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import image
import cv2

DATA_FILENAME = '240306_v2_vals_formatted.csv'

data = pd.read_csv(DATA_FILENAME, header=[0])
NROWS,NCOLS = data.shape
print(data.shape)

row0=data.iloc[0]
row0_points = np.array([np.array([row0[i],row0[i+1],row0[i+2]]) for i in range(0,len(row0)-1,3)])

im = image.imread("240306_v2_Miqus_10_28002_frame0.jpg")

Miqus_10_28002_Intrinsic = {"FocalLength": 6.150428,"SensorMinU": 0.000000,"SensorMaxU": 122879.000000,"SensorMinV": 0.000000,"SensorMaxV": 69631.000000,"FocalLengthU": 71559.046875,"FocalLengthV": 71578.187500,"CenterPointU": 60938.535156,"CenterPointV": 34490.714844,"Skew": 0.000000,"RadialDistortion1": -0.001828,"RadialDistortion2": -0.001020,"RadialDistortion3": 0.000000,"TangentalDistortion1": 0.000278,"TangentalDistortion2": 0.000274}
K = np.array([
    [Miqus_10_28002_Intrinsic['FocalLengthU'],0,Miqus_10_28002_Intrinsic['CenterPointU']],
    [0,Miqus_10_28002_Intrinsic['FocalLengthV'],Miqus_10_28002_Intrinsic['CenterPointV']],
    [0,0,1]
])
rvec=np.array([Miqus_10_28002_Intrinsic['RadialDistortion1'],Miqus_10_28002_Intrinsic['RadialDistortion2'],Miqus_10_28002_Intrinsic['RadialDistortion3']])
tvec=np.array([Miqus_10_28002_Intrinsic['TangentalDistortion1'],Miqus_10_28002_Intrinsic['TangentalDistortion2'],0])
distCoeffs = np.zeros((5, 1), np.float32) 
row0_2d = cv2.projectPoints(row0_points,rvec,tvec,cameraMatrix=K,distCoeffs=distCoeffs)
# "Intrinsic": {
#                 "FocalLength": 6.150428,
#                 "SensorMinU": 0.000000,
#                 "SensorMaxU": 122879.000000,
#                 "SensorMinV": 0.000000,
#                 "SensorMaxV": 69631.000000,
#                 "FocalLengthU": 71559.046875,
#                 "FocalLengthV": 71578.187500,
#                 "CenterPointU": 60938.535156,
#                 "CenterPointV": 34490.714844,
#                 "Skew": 0.000000,
#                 "RadialDistortion1": -0.001828,
#                 "RadialDistortion2": -0.001020,
#                 "RadialDistortion3": 0.000000,
#                 "TangentalDistortion1": 0.000278,
#                 "TangentalDistortion2": 0.000274

# plt.imshow(im)
ax = plt.axes(projection='3d')

for px, py, pz in row0_points:
    # plt.plot(row0[i],row0[i+2],'bo')
    ax.plot3D(px,py,pz,'bo') 
    # print(row0[i])
plt.show()
# print(row0_points)
# for point in row0_points:
#     plt.plot(point[0],point[2],'bo')
# plt.show()
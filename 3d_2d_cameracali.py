import numpy as np
import cv2
import csv
import matplotlib.pyplot as plt
import pandas as pd


csv_file = 'jonte-exp.csv'


#inställningarna för kamera 10 när jag springer sista gången 

# Camera matrix
camera_matrix = np.array([
    [71559.046875/64, 0, 60938.535156/64], 
    [0, 71578.187500/64, 34490.714844/64], 
    [0, 0, 1] 
])

# Distortion coefficients
dist_coeffs = np.array([
    -0.001828, -0.001020, 0.000278, 0.000274, 0.0  
])

# Translation vector
t_vec = np.array([996.594238, -1437.977905, 1048.386230])

# Rotation matrix
R = np.array([
    [0.999686, -0.014467, -0.020452],
    [0.021407, 0.069319, 0.997365],
    [-0.013011, -0.997490, 0.069607]
])


# kod för att ta ut en viss frames (rad) projecering

"""
def read_from_csv(file_path, rows=None):
   
    with open(file_path, mode='r', newline='') as file:
        reader = csv.reader(file)
        selected_rows = []
        
        for i, row in enumerate(reader):
            if rows is None or i in rows:
                selected_rows.extend(row) 

        flat_list = [float(item) for item in selected_rows ]
        grouped_list = [flat_list[i:i+3] for i in range(0, len(flat_list), 3)]
        coordinates = np.array(grouped_list, dtype=np.float32)

    return coordinates

"""


# Testade att manuellt ta ut punkterna för frame 1 och se om det blev bättre

points_3d = np.array([
    [869.232,514.902,1126.789],
    [968.763,705.824,1098.568],
    [1245.429,601.803,640.850],
    [971.445,616.964,289.955],
    [997.111,361.619,1085.016],
    [834.924,460.139,558.521],
    [561.038,428.078,218.277],
    [891.158,509.021,1386.855],
    [1023.155,554.592,1504.854],
    [1062.355,555.889,1667.501],
    [1117.334,558.549,1776.278],
    [1110.373,385.665,1546.745],
    [1114.639,224.417,1250.126],
    [1208.994,414.587,1370.150],
    [983.519,728.815,1572.846],
    [688.716,750.973,1397.713],
    [885.149,772.523,1244.889],
    [657.024,466.363,73.483],
    [1096.239,627.014,166.702]
], dtype=np.float32).reshape(-1, 1, 3)




# points_3d = read_from_csv(csv_file, rows=[500])



r_vec, _ = cv2.Rodrigues(R)

points_2d, _ = cv2.projectPoints(points_3d, r_vec, t_vec, camera_matrix, dist_coeffs)

print(points_2d)

points_2d_flat = points_2d.reshape(-1, 2) 

x_coordinates = points_2d_flat[:, 0]
y_coordinates = points_2d_flat[:, 1]

plt.scatter(x_coordinates, y_coordinates, marker='o') 

plt.title('2D Points')
plt.xlabel('X')
plt.ylabel('Y')

plt.grid(True)
plt.axis('equal')
plt.show()
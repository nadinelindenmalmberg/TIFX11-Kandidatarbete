import json
import numpy as np
import matplotlib.pyplot as plt

DATA_FILENAME = 'mmpose_results_240306_v1.json'
FPS = 100

with open(DATA_FILENAME,'r') as f:
    data = json.load(f)
frame = data['instance_info'][15]['instances'][0]['keypoints']
# print(frame)

name2id = data['meta_info']['keypoint_name2id']

ax = plt.axes(projection='3d')

for px,py,pz in frame:
    plt.plot(px,py,pz,'ob')
for i, (a,b) in enumerate(data['meta_info']['skeleton_links']):
    (px,py,pz) = list(zip(frame[a],frame[b]))
    skeleton_color = tuple(np.array(data['meta_info']['skeleton_link_colors']['__ndarray__'][i])/255)
    plt.plot(px,py,pz,color=skeleton_color)
plt.show()

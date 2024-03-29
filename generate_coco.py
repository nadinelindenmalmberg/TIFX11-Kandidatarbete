import pandas as pd
import os
import numpy as np
from pycocotools import pycoco
import json

VIDEO_FILENAME = 'coolvideoname.mp4'

DATA_FILENAME = '240306_v2_vals_formatted_short.csv'
AXES = ['-x','-y','-z']

CATEGORIES = [
   {
        "supercategory": "person",
        "id": 1,
        "name": "person",
        "keypoints": [
            'RAnkle', # 1         #
            'LAnkle', # 2         #
            'RKnee',  # 3
            'LKnee',  # 4
            'RWrist', # 5
            'LWrist', # 6
            'RElbow', # 7
            'LElbow', # 8
            'RForefoot', # 9
            'RTrochanterMajor', # 10       #
            'LForefoot', # 11    
            'LTrochanterMajor', # 12       #
            'WaistBack', # 13
            'RShoulderTop', # 14
            'LShoulderTop', # 15
            'SpineThoracic12', # 16
            'SpineThoracic2', # 17
            'HeadFront' # 18
        ],
        "skeleton": [ # 17 connections in total
            [18, 17], [17, 15], [17, 14], [17, 16], [16, 13], [13, 10], [13, 12], 
            [10, 3], [3, 1], [1, 9], [12, 4], [4, 2], [2, 11], [14, 7], 
            [7, 5], [15, 8], [8, 6]
        ]
    }
]

INFO = {
    "description": "V2 tifx11-vt24-80 Dataset",
    "version": "0.0.1",
    "year": 2024,
    "contributor": "mayeral",
}

LICENSES = [
    {
        "id": 1,
        "name": "Creative Commons Attribution 4.0 International",
        "url": "https://dataworldsupport.atlassian.net/servicedesk/customer/portals"
    }
]





def get_COCO_keypoints(axes=['-x','-z']):
    """
    Loads the formated qtm data for the video (.mp4) and reformats it to 
    COCO format i.e list: [x, y, v, x, y, v, ... x, y, v], where v is a visual 
    parameter (0, 1, 2); whether the keypoint is visual and measured.  
        0 = not measured.
        1 = measured but not visual.
        2 = measured and visual.

    Returns a list of list with keypoints for each frame.
    """
    keypoints = []

    header = CATEGORIES[0]['keypoints']
    header = [x+ax for x in header for ax in axes]
    df = pd.read_csv(DATA_FILENAME)
    df = df[header]
    # print(df.shape[0])

    for i in range(0, df.shape[0]):
        row = np.array(list(df.iloc[i]))
        row = np.insert(row, range(2, df.shape[1]+1, 2), 2) # lägger in 2an i v, W , 2 
        keypoints.append(row)
    return keypoints

get_COCO_keypoints()


VIDEO_EXT = '.avi'
folder_path = r'C:\Users\murmi\Documents\First-test-240306-1\Data\frames\240306_v2_Miqus_10_28002'
video_names = [filename for filename in os.listdir(folder_path) if (VIDEO_EXT in filename and os.path.isfile(os.path.join(folder_path, filename)))]

def generate_coco(video_name):

    # Initialize coco_outputs, annotation id and video id:
    coco_output = {
        "info": INFO,
        "licenses": LICENSES,
        "categories": CATEGORIES,
        "images": [],
        "annotations": []
    }
    print("Processing {}".format(video_name))
    frame_names = [filename for filename in os.listdir(folder_path) if ('.jpg' in filename and video_name.replace(VIDEO_EXT,'') in filename and os.path.isfile(os.path.join(folder_path, filename)))]
        

    keypoints = get_COCO_keypoints()

    if len(frame_names) != len(keypoints):
        raise Exception(f'Number of frames in images {len(frame_names)}st does not match keypoints {len(keypoints)}st')


    quit()
    annotation_id = 1
    for frame_i, im in enumerate(frame_names):
            
        # Create the image section, it contains the complete list 
        # of images in your dataset.
        image_id = video_id + frame_i
        image_info = pycoco.create_image_info(image_id, video_name, im)
        coco_output["images"].append(image_info)

        # Create the annotations in the single person coco-keypoint format. 
        annotation_info = pycoco.create_annotation_info(
            annotation_id, 
            image_id, 
            keypoints=keypoints[frame_i]
        )

        coco_output["annotations"].append(annotation_info)
        annotation_id += 1

        output_name = video_name.replace(".mp4", "").rstrip()

    with open("{}.json".format(output_name), "w") as output_json_file:
        json.dump(coco_output, output_json_file)

    video_id += 1e4

for video in video_names:
    generate_coco(video)

def get_COCO_keypoints_old(video_name):
    """
    Loads the formated qtm data for the video (.mp4) and reformats it to 
    COCO format i.e list: [x, y, v, x, y, v, ... x, y, v], where v is a visual 
    parameter (0, 1, 2); whether the keypoint is visual and measured.  
        0 = not measured.
        1 = measured but not visual.
        2 = measured and visual.

    Returns a list of list with keypoints for each frame.
    """
    file_path = video_name.replace(".mp4", "_2D_keypoints.csv")
    data_2D = pd.read_csv(file_path, index_col=0)

    keypoints = []
    for i in range(0, data_2D.shape[0], 2):
        x_keypoints = list(data_2D.iloc[i, :])
        y_keypoints = list(data_2D.iloc[i+1, :])
        keypoints_one_frame = []
        while(y_keypoints):
            # Remember that pop() reverses the order of the keypoints.
            keypoints_one_frame.append(x_keypoints.pop())
            keypoints_one_frame.append(y_keypoints.pop())
            # Assume v=2 for lack of better way to do it. 
            keypoints_one_frame.append(2)
        
        keypoints.append(keypoints_one_frame)

    return keypoints
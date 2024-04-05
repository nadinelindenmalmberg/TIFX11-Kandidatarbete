import pandas as pd
import os
import numpy as np
import cv2
import json
import tkinter as tk
from tkinter import filedialog

########################
#TODO: Kända "buggar" just nu, i prio-ordning:
# Använder inte pixelkoordinater utan QTM direkt
# Ingen boundry box
# Antar visible/2 hela tiden
# Flera videor i en fil
# 2022 var 0-indexerad i skeleton?...
########################

VIDEO_FILENAME = 'coolvideoname.mp4'
VIDEO_EXT = '.avi'

DATA_FILENAME = '240306_v2_vals_formatted_short.csv'
AXES = ['-x','-y','-z']

CATEGORIES = [
   {
        "supercategory": "person",
        "id": 1,
        "name": "person",
        "keypoints": [                          # 19 keypoints in total
                    "WaistBack",        # 0
                    "WaistL",           # 1
                    "LKnee",            # 2     Avg of: LKneeOut, LKneeIn
                    "LAnkleOut",        # 3
                    "WaistR",           # 4
                    "RKnee",            # 5     Avg of: RKneeOut, RKneeIn
                    "RAnkleOut",        # 6
                    "SpineThoracic12",  # 7
                    "UpperTorso",       # 8     Avg of: SpineThoracic2, Chest
                    "NeckBase",         # 9     Avg of: LShoulderTop, RShoulderTop, HeadL, HeadR
                    "CenterHead",       # 10    Avg of: HeadFront, HeadL, HeadR
                    "RShoulderTop",     # 11
                    "RElbow",           # 12    Avg of: RElbowOut, RElbowIn
                    "RHand",            # 13    Avg of: RWristIn, RWristOut
                    "LShoulderTop",     # 14
                    "LElbow",           # 15    Avg of: LElbowOut, LElbowIn
                    "LHand",             # 16    Avg of: LWristIn, LWristOut
                    "RForefoot",         # 17    Avg of: RForefoot2, RForefoot5.  Not in H36m!
                    "LForefoot"         # 18    Avg of: LForefoot2, LForefoot5.  Not in H36m!
                ],
        "skeleton": [ # 18 connections in total
            [0,1], [0,4], [0,7], [1,2], [2,3], [3,18], [4,5], [5,6], [6,17], [7,8], [8,9],
            [8,11], [8,14], [9,10], [11,12], [12,13], [14,15], [15,16]
        ]
    }
]

INFO = {
    "description": "V2 tifx11-vt24-80 Dataset",
    "version": "0.0.1",
    "year": 2024,
}

LICENSES = [
    {
        "id": 1,
        "name": "Creative Commons Attribution 4.0 International",
        "url": "https://dataworldsupport.atlassian.net/servicedesk/customer/portals"
    }
]



def create_annotation_info_new(annotation_id, image_id, image_size=None, tolerance=2, keypoints=None):
    """
    Returns annotation information as a dictionary for COCO-keypoints in a
    JSON style format.
    """
    annotation_info = {
       "image_id": image_id,
       "num_keypoints": int(len(keypoints)/3),  # 18
       "keypoints": keypoints,
       "iscrowd": 0,
       "category_id": 1,
       "id": annotation_id,
    }
    return annotation_info

def create_image_info(
        image_id, file_name, image,
        license_id=1):
    """Returns the image information in JSON style format."""
    image_info = {
        "id": image_id,
        "file_name": file_name,
        "width": image.shape[1],
        "height": image.shape[0],
        "license": license_id,
    }
    return image_info


def get_QTM_keypoints(data_filepath,axes):
    """
    Loads the formated qtm data and reformats it to 
    COCO format i.e list: [x, y, v, x, y, v, ... x, y, v], where v is a visual 
    parameter (0, 1, 2); whether the keypoint is visual and measured.  
        0 = not measured.
        1 = measured but not visual.
        2 = measured and visual.
    Axes should be a two lenght tuple in the style ('-x','-y')

    Returns a list of list with keypoints for each frame.
    """

    if not len(axes)==2 or not axes[0] in AXES or not axes[1] in AXES:
        raise Exception('ERROR: get_get_QTM_keypoints needs two axes in the style (\'-x\',\'-y\'), you selected: '+str(axes))
    if not os.path.exists(data_filepath):
        raise Exception('Couldnt find data file: '+str(data_filepath))

    keypoints = []

    header = CATEGORIES[0]['keypoints']     # the poins we want to use
    header = [x+ax for x in header for ax  in axes]
    df = pd.read_csv(data_filepath)
    df = df[header] # new dataframe which only contains the poins we use, in the right order
    # print(df.shape[0])

    for i in range(0, df.shape[0]):
        row = np.array(list(df.iloc[i]))
        row = np.insert(row, range(2, df.shape[1]+1, 2), 2) # adds the "2" in [..., v, w, 2, ...] 
        keypoints.append(list(row))
    return keypoints


def generate_coco(video_name,frames_folder_path):

    # Initialize coco_outputs, annotation id and video id:
    coco_output = {
        "info": INFO,
        "licenses": LICENSES,
        "categories": CATEGORIES,
        "images": [],
        "annotations": []
    }
    print(f"Generating coco-file for {os.path.basename(video_name)}")
    frame_names = [filename for filename in os.listdir(frames_folder_path) if ('.jpg' in filename and os.path.basename(video_name).replace(VIDEO_EXT,'') in filename)]

    print('Choose two axis, with a space as a separator between:')  # choose which two QTM axes to use
    axes = ['-'+x.lower() for x in input('> ').strip().split(' ')]
    data_filename = video_name.split('Miqus')[0]+'formatted.csv'
    # data_filepath = os.path.join(os.path.dirname(video_name) , data_filename)
    keypoints = get_QTM_keypoints(data_filename,axes) 

    if len(frame_names) != len(keypoints):
        # raise Exception(f'Number of frames in images {len(frame_names)}st does not match keypoints {len(keypoints)}st')
        print(f'NOTICE: Potential error! Number of frames in images ({len(frame_names)}st) does not match keypoints ({len(keypoints)}st). Only the {len(frame_names)} first keypoints will be used.')

    annotation_id = 1
    video_id = 1
    for frame_i, im_name in enumerate(frame_names):

        im = cv2.imread(os.path.join(frames_folder_path, im_name))

        # Create the image section, it contains the complete list 
        # of images in your dataset.
        image_id = video_id + frame_i
        image_info = create_image_info(image_id, im_name, im)
        coco_output["images"].append(image_info)

        # Create the annotations in the single person coco-keypoint format. 
        annotation_info = create_annotation_info_new(
            annotation_id, 
            image_id, 
            keypoints=keypoints[frame_i]
        )

        coco_output["annotations"].append(annotation_info)
        annotation_id += 1

        output_name = video_name.replace(VIDEO_EXT, "").rstrip()+'_coco.json'

    # print(type(coco_output))
    with open(output_name, "w") as output_json_file:
        json.dump(coco_output, output_json_file)
    
    print(f'Successfully generated {os.path.basename(output_name)}')

    video_id += 1e4


def split_video_into_frames(video_filepath, frames_foldername, show_progressbar=True):
    """
    Splits a video into a series of images, for all its frames.
    Images will be saved in a child folder named videoname_FRAMES.
    """
    vid_cap = cv2.VideoCapture(video_filepath)
    fps = int(vid_cap.get(cv2.CAP_PROP_FPS))
    n_frames = int(vid_cap.get(cv2.CAP_PROP_FRAME_COUNT))

    if show_progressbar:
        from tqdm import tqdm
        pbar = tqdm(total=n_frames, desc='Frames generated')


    if not os.path.exists(frames_foldername):
        os.mkdir(frames_foldername)

    
    video_filename_no_prefix = os.path.basename(video_filepath).replace('.avi','').replace('.mp4','')

    vidcap = cv2.VideoCapture(video_filepath)
    success,image = vidcap.read()
    count = 0
    while success:
        cv2.imwrite(os.path.join(frames_foldername, f"{video_filename_no_prefix}_frame{count}.jpg") , image)     # save frame as JPEG file      
        success,image = vidcap.read()
        count += 1
        if show_progressbar:
            pbar.update(1)

    if show_progressbar:
        pbar.close()
    print('Frame splitting completed for video ',video_filename_no_prefix)
    


def main():

    # select videos to generate files for
    root = tk.Tk(); root.withdraw()
    video_filepath_list = filedialog.askopenfilenames(filetypes=[("Video file", "*.avi"),("Video file", "*.mp4")], title='Select video file(s)')
    
    if not video_filepath_list:
        print('No files selected!')
        quit()
    
    for video_filepath in video_filepath_list:
        VIDEO_EXT = '.' + os.path.basename(video_filepath).split('.')[1]
        video_filename = os.path.basename(video_filepath).replace('.avi','').replace('.mp4','')
        video_folderpath = os.path.dirname(video_filepath)
        frames_folderpath = os.path.join(video_folderpath, video_filename+'_FRAMES')

        # option to generate frames
        print(f'Split frames for video {os.path.basename(video_filepath)} ? (y/n)')
        if input('> ').strip().lower() == 'y':
            split_video_into_frames(video_filepath, frames_folderpath, show_progressbar=True)

        # generates the coco-file!
        generate_coco(video_filepath, frames_folderpath)

if __name__ == '__main__':
    main()

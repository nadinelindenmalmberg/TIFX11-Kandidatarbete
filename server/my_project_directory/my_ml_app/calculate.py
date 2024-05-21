import math
import os
import json
from django.conf import settings    
import glob
from django.http import JsonResponse
from django.views.decorators.http import require_GET

json_files_dir = os.path.join(os.path.dirname(__file__), '..', 'json_files')



def calculate_from_json(filename):
    file_path = os.path.join(json_files_dir, filename)

    if not os.path.exists(file_path):
        return None

    with open(file_path, 'r') as file:
        data = json.load(file)
        # Perform your calculations here
        # For instance, count the number of items in the "images" list
        result = len(data["images"])
        return result

""" class RunFrequency:
    def __init__(self, directory):
        self.directory = directory
"""
def get_files():
    if not os.path.exists(json_files_dir):
        print(f"Directory does not exist: {json_files_dir}")
        return []
    
    files = glob.glob(os.path.join(json_files_dir, '*.json'))
    print(f"Looking for files in: {json_files_dir}")
    print(f"Found files: {files}")
    return files

def get_frequence_data(filename):
    file_path = os.path.join(json_files_dir, filename)

    with open(file_path, 'r') as file:
        data = json.load(file)

    min_value = float('inf')
    for frame in data:
        if 'instances' in frame and len(frame['instances']) > 0:
            instance = frame['instances'][0]  
            keypoints = instance['keypoints']
            if len(keypoints) > 6:  # Ensure there are enough keypoints
                keypoints_values = [keypoints[3][2], keypoints[6][2]] 
                current_min = min(keypoints_values)
                if current_min < min_value:
                    min_value = current_min

    print(f"Min value for {file_path}: {min_value}")

    frequence_limit =  0.1
    frequence_right_foot = []
    for frame in data:
        if 'instances' in frame and len(frame['instances']) > 0:
            instance = frame['instances'][0]  # Only consider the first instance
            keypoints = instance['keypoints']
            if len(keypoints) > 6:  # Ensure there are enough keypoints
                if keypoints[6][2] <= frequence_limit:
                    frequence_right_foot.append(1)
                else:
                    frequence_right_foot.append(0)
    
    print(f"Frequence right foot for {file_path}: {frequence_right_foot}")
    return frequence_right_foot

def transitions(binary_list):
    transitions = 0
    for i in range(1, len(binary_list)):
        if binary_list[i-1] == 1 and binary_list[i] == 0:
            transitions += 1      
    return transitions

def process_all_files(file_path):

    total_transitions = 0
    for file_path in get_files():
        binary_list = get_frequence_data(file_path)
        transition_count = transitions(binary_list)
        print(f"Transitions for {file_path}: {transition_count}")
        total_transitions += transition_count
    return total_transitions

def get_frequency_two_legs(filename):
    file_path = os.path.join(json_files_dir, filename)

    return process_all_files(file_path)

def calculate_angle(p1, p2, p3):
    AB = [p1[i] - p2[i] for i in range(3)]
    BC = [p3[i] - p2[i] for i in range(3)]

    dot_product = sum(AB[i] * BC[i] for i in range(3))
    magnitude_AB = math.sqrt(sum(AB[i]**2 for i in range(3)))
    magnitude_BC = math.sqrt(sum(BC[i]**2 for i in range(3)))

    if magnitude_AB * magnitude_BC == 0:
        return 0.0

    angle_rad = math.acos(dot_product / (magnitude_AB * magnitude_BC))
    angle_deg = math.degrees(angle_rad)

    return angle_deg

def get_angles(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)

    angles = []
    for frame in data:
        frame_id = frame['frame_id']
        if not frame['instances']:
            continue

        instance = frame['instances'][0]
        keypoints = instance['keypoints']

        if len(keypoints) >= 6 and all(len(kp) >= 3 for kp in keypoints[:6]):
            p1, p2, p3 = keypoints[1], keypoints[2], keypoints[3]
            p4, p5, p6 = keypoints[4], keypoints[5], keypoints[6]

            angle1 = calculate_angle(p1, p2, p3)
            angle2 = calculate_angle(p4, p5, p6)

            angles.append({
                'frame_id': frame_id,
                'angle1': angle1,
                'angle2': angle2
            })

    return angles

def process_all_files_angles(filename):
    file_path = os.path.join(json_files_dir, filename)

    all_angles = []
    ##for file_path in get_files():
    angles = get_angles(file_path)
    all_angles.append({
        #'file_path': file_path,
        'angles': angles
    })
    return all_angles

@require_GET
def calculate(request, filename):
    file_path = os.path.join(json_files_dir, filename)

    if not os.path.exists(file_path):
        return JsonResponse({'success': False, 'error': 'File not found'})

    angles_data = process_all_files_angles()

    return JsonResponse({'success': True, 'angles_data': angles_data})
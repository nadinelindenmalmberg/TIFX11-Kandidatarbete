import json
import math
import glob

def distance_2d(point1, point2):
    x1, y1 = point1
    x2, y2 = point2
    return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)

def stride_length(foot_positions):
    strides = []
    total_distance = 0
    for i in range(1, len(foot_positions)):
        stride = distance_2d(foot_positions[i-1], foot_positions[i])
        strides.append(stride)
        total_distance += stride
    return total_distance

def is_contact_point(current_foot_position, last_foot_position):
    if last_foot_position is None:
        return False
    
    movement_magnitude = math.sqrt((current_foot_position[0] - last_foot_position[0])**2 + 
                                   (current_foot_position[1] - last_foot_position[1])**2)
    
    minimal_movement_threshold = 0.05 
    
    return movement_magnitude < minimal_movement_threshold
def process_file(filepath):
    with open(filepath, 'r') as file:
        data = json.load(file)

    left_foot_positions = []
    right_foot_positions = []
    last_left_foot_position = None
    last_right_foot_position = None

    for frame in data:
        for instance in frame['instances']:
            keypoints = instance['keypoints']
            left_foot = keypoints[3][:2]  
            right_foot = keypoints[6][:2]  

            if is_contact_point(left_foot, last_left_foot_position):
                left_foot_positions.append(left_foot)
            if is_contact_point(right_foot, last_right_foot_position):
                right_foot_positions.append(right_foot)
            
            last_left_foot_position = left_foot
            last_right_foot_position = right_foot

    left_total_distance = stride_length(left_foot_positions)
    right_total_distance = stride_length(right_foot_positions)

    print(f"File: {filepath}")
    print("Left foot total stride distance:", left_total_distance)
    print("Right foot total stride distance:", right_total_distance)
    print()

# File path
directory_path = 'output_cal/'
file_pattern = "*.json"

for filepath in glob.glob(directory_path + file_pattern):
    process_file(filepath)
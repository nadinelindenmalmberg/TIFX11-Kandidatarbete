import glob
import json
import os

class RunFrequency:
    def __init__(self, directory):
        self.directory = directory

    def get_files(self):
        if not os.path.exists(self.directory):
            print(f"Directory does not exist: {self.directory}")
            return []
        
        files = glob.glob(os.path.join(self.directory, '*.json'))
        print(f"Looking for files in: {self.directory}")
        print(f"Found files: {files}")
        return files

    def get_frequence_data(self, file_path):
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

    def transitions(self, binary_list):
        transitions = 0
        for i in range(1, len(binary_list)):
            if binary_list[i-1] == 1 and binary_list[i] == 0:
                transitions += 1      
        return transitions

    def process_all_files(self):
        total_transitions = 0
        for file_path in self.get_files():
            binary_list = self.get_frequence_data(file_path)
            transition_count = self.transitions(binary_list)
            print(f"Transitions for {file_path}: {transition_count}")
            total_transitions += transition_count
        return total_transitions
    
def get_frequency_two_legs():
    rf = RunFrequency("jsonfiles")
    return 2 * rf.process_all_files()

print(get_frequency_two_legs())

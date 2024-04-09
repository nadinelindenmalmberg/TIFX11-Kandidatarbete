import json
import glob

class RunFrequency:
    def __init__(self, directory):
        self.directory = directory

    def get_files(self):
        return glob.glob(self.directory + '/*.json')

    def get_frequence_data(self, file_path):
        with open(file_path, 'r') as file:
            data = json.load(file)

        min_value = 0
        for frame in data:
            for instance in frame['instances']:
                keypoints = instance['keypoints']
                keypoints_values = [keypoints[3][2], keypoints[6][2]] 
                current_min = min(keypoints_values)
                if current_min < min_value:
                    min_value = current_min

        frequence_limit = min_value + 0.1
        frequence_right_foot = []
        for frame in data:
            for instance in frame['instances']:
                keypoints = instance['keypoints']
                if keypoints[6][2] <= frequence_limit:
                    frequence_right_foot.append(1)
                else:
                    frequence_right_foot.append(0)
        return frequence_right_foot

    def transitions(self, binary_list):
        transitions = 0
        for i in range(1, len(binary_list)):
            if binary_list[i-1] == 1 and binary_list[i] == 0:
                transitions += 1      
        return transitions

    def process_all_files(self):
        for file_path in self.get_files():
            binary_list = self.get_frequence_data(file_path)
            transition_count = self.transitions(binary_list)
            return transition_count
    
    
def get_frequency_two_legs():
        rf = RunFrequency("output_cal")  
        return 2* rf.process_all_files()


print(get_frequency_two_legs())


















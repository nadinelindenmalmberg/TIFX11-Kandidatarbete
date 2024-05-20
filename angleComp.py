import glob
import json
import os
import math

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

    def calculate_angle(self, p1, p2, p3):
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

    def get_angles(self, file_path):
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
                # First set of keypoints
                p1, p2, p3 = keypoints[1], keypoints[2], keypoints[3]
                # Second set of keypoints
                p4, p5, p6 = keypoints[4], keypoints[5], keypoints[6]

                # Calculate angles
                angle1 = self.calculate_angle(p1, p2, p3)
                angle2 = self.calculate_angle(p4, p5, p6)

                angles.append((frame_id, angle1, angle2))
            else:
                print(f"Not enough keypoints or keypoints do not have enough coordinates in frame {frame_id} of {file_path}")

        return angles

    def process_all_files(self):
        all_angles = []
        for file_path in self.get_files():
            angles = self.get_angles(file_path)
            all_angles.append((file_path, angles))
        return all_angles
    
def get_angles_from_directory():
    rf = RunFrequency("jsonfiles")
    return rf.process_all_files()

all_angles = get_angles_from_directory()

# Print the angles with more details
for file_path, angles in all_angles:
    print(f"File: {file_path}")
    for frame_id, angle1, angle2 in angles:
        print(f"  Frame ID: {frame_id}, Angle1 (Keypoints 0,1,2): {angle1:.2f} degrees, Angle2 (Keypoints 3,4,5): {angle2:.2f} degrees")

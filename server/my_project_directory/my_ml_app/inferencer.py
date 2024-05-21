import subprocess
import cv2
from mmpose.apis import MMPoseInferencer


def Inferencer(file_path, output):
    #img_path = './my_project_directory/media/videos/431090375_7611704718888664_5861720536947366731_n.mp4'   # replace this with your own image path
    input_file = file_path
    output_file = output

    # instantiate the inferencer using the model alias
    # build the inferencer with 3d model alias
    inferencer = MMPoseInferencer(pose3d="human3d", device='cpu')

    # The MMPoseInferencer API employs a lazy inference approach,
    # creating a prediction generator when given input
    result_generator= inferencer(input_file, show=False, vis_out_dir=output_file, pred_out_dir='json_files')
    

    #result = next(result_generator)

    results = [result for result in result_generator]


    
    
    
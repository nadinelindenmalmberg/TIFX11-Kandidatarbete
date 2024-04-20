from mmpose.apis import MMPoseInferencer

img_path = './my_project_directory/media/videos/431090375_7611704718888664_5861720536947366731_n.mp4'   # replace this with your own image path

# instantiate the inferencer using the model alias
# build the inferencer with 3d model alias
inferencer = MMPoseInferencer(pose3d="human3d", device='cpu')

# The MMPoseInferencer API employs a lazy inference approach,
# creating a prediction generator when given input
result_generator = inferencer(img_path, show=False, vis_out_dir='results')
results = [result for result in result_generator]
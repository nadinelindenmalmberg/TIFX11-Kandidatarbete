import cv2, os

VIDEO_FILEPATH = '240306_v2_Miqus_10_28002.avi'

SHOW_PROGRESSBAR = False
NFRAMES = 3000 # only needed for progress bar visualization
if SHOW_PROGRESSBAR:
    from tqdm import tqdm # only needed for progress bar visualization

        
def split_video_into_frames(video_filepath, show_progressbar=True):
    """
    Splits a video into a series of images, for all its frames.
    Images will be saved in a child folder named videoname_FRAMES.
    """

    video_filename = os.path.basename(video_filepath).replace('.avi','').replace('.mp4','')
    frames_folderpath = os.path.join('/'.join(os.path.abspath(video_filepath).split('/')[:-2]), 'frames', video_filename+'_frames')
    
    vid_cap = cv2.VideoCapture(video_filepath)
    fps = int(vid_cap.get(cv2.CAP_PROP_FPS))
    n_frames = int(vid_cap.get(cv2.CAP_PROP_FRAME_COUNT))

    if show_progressbar:
        from tqdm import tqdm
        pbar = tqdm(total=n_frames, desc='Frames generated')


    if not os.path.exists(frames_folderpath):
        os.mkdir(frames_folderpath)

    
    video_filename_no_prefix = os.path.basename(video_filepath).replace('.avi','').replace('.mp4','')

    vidcap = cv2.VideoCapture(video_filepath)
    success,image = vidcap.read()
    count = 0
    while success:
        cv2.imwrite(os.path.join(frames_folderpath, f"{video_filename_no_prefix}_frame{count}.jpg") , image)     # save frame as JPEG file      
        success,image = vidcap.read()
        count += 1
        if show_progressbar:
            pbar.update(1)

    if show_progressbar:
        pbar.close()
    print('Frame splitting completed for video ',video_filename_no_prefix)
    

if __name__ == '__main__':
    split_video_into_frames(video_filepath=VIDEO_FILEPATH, show_progressbar=SHOW_PROGRESSBAR)
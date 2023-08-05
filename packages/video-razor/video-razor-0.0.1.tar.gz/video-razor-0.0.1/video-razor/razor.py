import os
import numpy as np

import cv2


class VideoRazor:
    """
    Slices videos into N sections.
    """
    def __init__(self, input_path, output_path, splits):
        self.input_path = input_path
        if not isinstance(self.input_path, str):
            raise TypeError("Output must be a string")
        self.output_path = output_path
        if not isinstance(self.output_path, str):
            raise TypeError("Output must be a string")
        self.splits = splits
        if not isinstance(self.splits, int):
            raise TypeError("Splits must be a int")
        self.fps = None

    def get_frames(self):
        """
        Extracts each frame of the video to a list.
        :return:
        -------
        frames : list
            Frames which make up a video
        """
        # Read video
        cap = cv2.VideoCapture(self.input_path)
        # Get fps
        self.fps = cap.get(cv2.CAP_PROP_FPS)
        # Make sure video is being read
        if cap.isOpened():
            success, frame = cap.read()
            frames = []
            while success:
                frames.append(frame)
                # Read new frame
                success, frame = cap.read()
            return frames

    def get_roi_measurements(self):
        """
        Gets the height and width each output video will be.
        :return:
        -------
        images : list
            Images which make up a video
        """
        return map(lambda x: x / self.splits, self.get_frames()[0].shape[:2])

    def get_roi(self):
        """
        Gets region of interest for each frame in the list of frames
        and appends it to a new list of frames.
        :return:
        -------
        frames : list
            A list of frames
        """
        # Get h, w of video sections
        roi_h, roi_w = self.get_roi_measurements()
        # split frames into sections
        frames = list()
        # For each horizontal section
        for i in range(0, self.splits):
            # For each vertical section
            for j in range(0, self.splits):
                # For each frame in frames
                for frame in self.get_frames():
                    # Get roi from frame
                    frame = frame[int(i * roi_h): int(i * roi_h) + int(roi_h),
                                  int(j * roi_w): int(j * roi_w) + int(roi_w)]
                    frames.append(frame)
        return frames

    def create_output_path(self):
        """
        Creates file path, for video, which does not already exist.

        :return:
        ----------
        output_path : str
            Output directory
        """
        filename = self.output_path + '{}.mp4'
        counter = 0
        while os.path.isfile(filename.format(counter)):
            counter += 1
        # Apply counter to filename
        return filename.format(counter)

    def slice(self):
        # Get h, w of video sections
        roi_h, roi_w = self.get_roi_measurements()
        # Get number of videos to be output
        num_videos = self.splits ** 2
        # Input frames from video to list
        frames = self.get_roi()
        # Init list of Nones length of list
        out_videos = [None] * num_videos
        # Split list into list of lists
        frames_split = np.array_split(frames, num_videos)
        # For each videos worth of frames
        for i in range(len(frames_split)):
            # Create output path
            output_path = self.create_output_path()
            # Set up fourcc
            four_cc = cv2.VideoWriter_fourcc(*'MJPG')
            # Create video writer for each i-th in list
            out_videos[i] = cv2.VideoWriter(output_path,
                                            four_cc,
                                            self.fps,
                                            (int(roi_w), int(roi_h)))
            # Get inner list
            video_frames = frames_split[i]
            # Write frames to file
            for frame in video_frames:
                out_videos[i].write(frame)
            # Release video writer
            out_videos[i].release()

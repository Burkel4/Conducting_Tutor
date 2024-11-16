from name import initializeVideo, videoBeatPlotName
from graphs import *
from mp_declaration import mediaPipeDeclaration
import cv2
import numpy as np
from scipy.signal import find_peaks
from process import process_video


class cycleOne: 

    def __init__(self):
        self.detector = mediaPipeDeclaration.get_pose_landmarker() # get mediapipe dector
        self.videoFileName = initializeVideo() # get file name of video being processed
        
        self.cap = cv2.VideoCapture(self.videoFileName) # set video as out cap
        if not self.cap.isOpened(): # see is video opens, if not print out error message
            print("Error: Could not open video file.")
            exit()

        #variables shared among cycleOne and cycleTwo
        self.frame_array = []  # Stores coordinates for the entire video
        self.processed_frame_array = []  # Stores coordinates only during active processing intervals
        self.processing_intervals = []  # List to store multiple processing intervals

        # Initialize VideoWriter for output video
        self.frame_width = int( self.cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        self.frame_height = int( self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        self.fps = int( self.cap.get(cv2.CAP_PROP_FPS))        
        self.out = cv2.VideoWriter(videoBeatPlotName() + '.avi', cv2.VideoWriter_fourcc(*'MJPG'), self.fps, (self.frame_width, self.frame_height))

        process_video(self.cap, self.out, self.detector, self.frame_array, self.processed_frame_array, self.processing_intervals)

        print ("made it to the very end of the program")

if __name__ == "__main__":
    cycle_one_instance = cycleOne()

#   # Initialize variables for beat detection and BPM calculation
#     bpm_window = 30  # Time window in seconds for BPM calculation
#     fps = int(cap.get(cv2.CAP_PROP_FPS))
#     frames_per_window = bpm_window * fps
#     beats = []  # List to store frames where beats occur
#         # Text properties for beat display
#     font = cv2.FONT_HERSHEY_SIMPLEX
#     font_scale = 2
#     font_thickness = 2
#     font_color = (255, 255, 255)
#     text_display_duration = 3  # Number of frames to display "Beat!" text
#     text_display_counter = 0
# class cycleTwo: 

#     def __init__(self):
#         self.detector = mediaPipeDeclaration.get_pose_landmarker() # get mediapipe dector

#     x = [coord[0] for coord in cycleOne.frame_array]
#     y = [coord[1] for coord in cycleOne.frame_array]

#     # Find peaks and valleys in x and y coordinates
#     x_peaks, _ = find_peaks(x)
#     x_valleys, _ = find_peaks([-val for val in x])
#     y_peaks, _ = find_peaks(y)
#     y_valleys, _ = find_peaks([-val for val in y])

#     # Convert x_proc and y_proc to numpy arrays for proper arithmetic operations
#     x_proc = np.array([coord[0] for coord in processed_frame_array])
#     y_proc = np.array([coord[1] for coord in processed_frame_array])

#     # Directly apply find_peaks to x_proc and y_proc as numpy arrays
#     x_peaks_proc, _ = find_peaks(x_proc)
#     x_valleys_proc, _ = find_peaks(-x_proc)  # Now valid with numpy arrays
#     y_peaks_proc, _ = find_peaks(y_proc)
#     y_valleys_proc, _ = find_peaks(-y_proc)

#     # Ensure each peaks/valleys array is a list of indices
#     x_peaks_proc = list(x_peaks_proc)
#     x_valleys_proc = list(x_valleys_proc)
#     y_peaks_proc = list(y_peaks_proc)
#     y_valleys_proc = list(y_valleys_proc)

#     # Filter peaks based on a frame threshold
#     def filter_significant_points(points, threshold):
#         if len(points) == 0:
#             return []
#         filtered_points = [points[0]]
#         for i in range(1, len(points)):
#             if points[i] - filtered_points[-1] > threshold:
#                 filtered_points.append(points[i])
#         return filtered_points

#     threshold = 10  # Define a threshold in number of frames

#     significant_beats = sorted(set(x_peaks_proc + x_valleys_proc + y_peaks_proc + y_valleys_proc))
#     filtered_significant_beats = filter_significant_points(significant_beats, threshold)
#     frame_index = 0

#     # Initialize for second video capture loop
#     cap = cv2.VideoCapture(videoFileName)
#     frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
#     frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
#     size = (frame_width, frame_height)
#     fps = int(cap.get(cv2.CAP_PROP_FPS))  

#     # Change codec if necessary
#     out = cv2.VideoWriter(videoOutputFileName + '.avi', cv2.VideoWriter_fourcc(*'MJPG'), fps, size)

#     # Initialize text properties
#     font = cv2.FONT_HERSHEY_SIMPLEX
#     font_scale = 2  
#     font_thickness = 2
#     font_color = (255, 255, 255)
#     text_display_duration = 3  
#     text_display_counter = 0

#     def is_within_intervals(frame_idx, intervals):
#         return any(start <= frame_idx <= end for start, end in intervals)

#     # Function to calculate BPM based on beats within the last time window
#     def calculate_bpm(current_frame, beats, fps, window_duration):
#         # Filter out beats that fall outside the time window
#         beats_in_window = [beat for beat in beats if current_frame - beat <= window_duration * fps]
#         bpm = len(beats_in_window) * (60 / window_duration)
#         return bpm

#     # Second loop: Use stored results to annotate the output video
#     while cap.isOpened():
#         success, image = cap.read()
#         if not success:
#             print("Ending processing.")
#             break

#         image_bgr = image

#         total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
#         frame_timestamp_ms = round(cap.get(cv2.CAP_PROP_POS_MSEC))

#         image_rgb = cv2.cvtColor(image_bgr, cv2.COLOR_BGR2RGB)
#         mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=image_rgb)

#         detection_result = detector.detect_for_video(mp_image, frame_timestamp_ms)
#         annotated_image = draw_landmarks_on_image(image_rgb, detection_result)
#         annotated_image_bgr = cv2.cvtColor(annotated_image, cv2.COLOR_RGB2BGR)

#     # Check if current frame is within processing intervals and handle beat text
#         if is_within_intervals(frame_index, processing_intervals):
#             # Display "Beat!" text and calculate BPM if frame is a beat
#             if frame_index in filtered_significant_beats:
#                 # Calculate text position and draw text
#                 text = "Beat!"
#                 text_size = cv2.getTextSize(text, font, font_scale, font_thickness)[0]
#                 text_x = (annotated_image_bgr.shape[1] - text_size[0]) // 2
#                 text_y = (annotated_image_bgr.shape[0] + text_size[1]) // 2
#                 cv2.putText(annotated_image_bgr, text, (text_x, text_y), font, font_scale, font_color, font_thickness)

#                 # Record the current beat and calculate BPM
#                 beats.append(frame_index)
#                 bpm = calculate_bpm(frame_index, beats, fps, bpm_window)

#                 # Save BPM information to file
#                 bpm_info = f'Beats per minute (BPM) at frame {frame_index}: {bpm}\n'
#                 output_file = '4-4stacatto(2).mp4_auto_BPM.txt'
#                 with open(output_file, 'a') as file:
#                     print(bpm_info, end='')
#                     file.write(bpm_info)

#                 # Reset display counter for beat text duration
#                 text_display_counter = text_display_duration
#             else:
#                 # Only display "Beat!" text if counter is active
#                 if text_display_counter > 0:
#                     cv2.putText(annotated_image_bgr, "Beat!", (text_x, text_y), font, font_scale, font_color, font_thickness)
#                     text_display_counter -= 1  # Decrement counter

#         # Swaying
#         if frame_index < len(midpoints_x):
#             midpoint_x = midpoints_x[frame_index]
#             if midpoint_x > default_midpoint_x + sway_threshold or midpoint_x < default_midpoint_x - sway_threshold:
#                 cv2.putText(annotated_image_bgr, "Swaying", (50, 100), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 255), 2)

#         cv2.putText(annotated_image_bgr, f'Frame: {frame_index}', (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 255, 255), 2)
#         cv2.imshow('Annotated Frames', annotated_image_bgr)
#         out.write(annotated_image_bgr)

#         key = cv2.waitKey(5) & 0xFF
#         if key == 27:
#             break

#         frame_index += 1

#     cap.release()
#     out.release()
#     cv2.destroyAllWindows()

#     beatPlotGraph(processing_intervals, filtered_significant_beats, x_valleys, y_peaks, y_valleys, x, y)

#     handPathGraph(x_proc, y_proc)

#     swayingGraph(midpoints_x, default_midpoint_x, sway_threshold)

#     mirrorXCoordinateGraph(left_hand_x, right_hand_x)

#     mirrorYCoordinateGraph(left_hand_y, right_hand_y)

#     cv2.destroyAllWindows()

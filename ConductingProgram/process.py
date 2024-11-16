import numpy as np
import mediapipe as mp
import cv2
from mp_declaration import mediaPipeDeclaration
from mirror import mirrorDetection
from sway import swayingDetection

# Process a single frame: Capture, convert, and get detection results
def process_frame(cap, detector):

    success, image = cap.read()
    if not success:
        return None, None

    frame_timestamp_ms = round(cap.get(cv2.CAP_PROP_POS_MSEC))
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=image_rgb)
    detection_result = detector.detect_for_video(mp_image, frame_timestamp_ms)
    annotated_image = mediaPipeDeclaration.draw_landmarks_on_image(image_rgb, detection_result)
    annotated_image_bgr = cv2.cvtColor(annotated_image, cv2.COLOR_RGB2BGR)

    return annotated_image_bgr, detection_result


# Process landmarks in each frame
def process_landmarks(detection_result, frame_array, processed_frame_array, processing_active, swaying_detector, mirror_dectector):
    pose_landmarks_list = detection_result.pose_landmarks
    if pose_landmarks_list:
        for landmarks in pose_landmarks_list:
            if len(landmarks) > 16:

                x16 = landmarks[16].x,
                y16 = landmarks[16].y
                
                frame_array.append((x16, y16))
                processed_frame_array.append((np.nan, np.nan))

                mirror_dectector.mirror_calculation(landmarks[15].x, landmarks[15].y, landmarks[16].x, landmarks[16].y)
                swaying_detector.midpoint_calculation(landmarks[12].x, landmarks[11].x)                
                # If processing is active, apply swaying and mirror detection
                if processing_active:
                    swaying_detector.set_midpoint()

    return


# Handle user input for start/stop processing and exit
def handle_user_input(key, frame_number, processing_active, current_start_frame, swaying_detector, processing_intervals):
    if key == ord('s'):
        swaying_detector.set_midpoint_flag_true()
        print(f"Processing started at frame {current_start_frame}")
        return True, frame_number  # Return processing_intervals as well
    
    elif key == ord('e'):
        processing_intervals.append((current_start_frame, frame_number))  # Update intervals
        swaying_detector.set_midpoint_flag_false()
        print(f"Processing stopped at frame {frame_number}")
        return False, frame_number  # Return updated intervals
    
    elif key == 27:  # ESC key
        if processing_active:
            processing_intervals.append((current_start_frame, frame_number))  # Mark interval end
            print(f"Processing stopped at frame {frame_number}")
        return None, frame_number  # Indicate to stop processing and return intervals

    return processing_active, frame_number  # Default return when no key is pressed  return processing_active, frame_number


# Main function to process the video
def process_video(cap, out, detector, frame_array, processed_frame_array, processing_intervals):
    
    # Initialize flags and variables
    swaying_detector = swayingDetection()
    mirror_dectector = mirrorDetection()
    frame_number = 0
    processing_active = False
    current_start_frame = None

    while cap.isOpened():

        success, image = cap.read()
        if not success:
            if processing_active:
                processing_intervals.append((current_start_frame, frame_number - 1))
                print(f"Processing stopped because video ended at frame {frame_number}")
            break

        annotated_image_bgr, detection_result = process_frame(cap, detector)

        # Display the annotated frame
        if annotated_image_bgr is not None:
            cv2.imshow('Video Feed - Selection Mode', annotated_image_bgr)

            # Process landmarks if they exist
            process_landmarks(detection_result, frame_array, processed_frame_array, 
                              processing_active, swaying_detector, mirror_dectector)

            # Display frame number
            cv2.putText(annotated_image_bgr, f'Frame: {frame_number}', (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 255, 255), 2)
            
            # Write the frame to the output video
            out.write(annotated_image_bgr)

        # Handle user input
        key = cv2.waitKey(5) & 0xFF
        processing_active, current_start_frame = handle_user_input(key, frame_number, processing_active, current_start_frame, swaying_detector, processing_intervals)

        # Exit loop if ESC key is pressed
        if processing_active is None:
            break

        frame_number += 1

    # Release resources
    cap.release()
    out.release()
    cv2.destroyAllWindows()

    return frame_array, processed_frame_array, processing_intervals
    


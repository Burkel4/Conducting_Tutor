from imports import *

# processes a single frame and returns the annotated image and detection results
def process_frame(cap, detector):
    success, image = cap.read()
    if not success:
        return None, None

    # process image through mediapipe
    frame_timestamp_ms = round(cap.get(cv2.CAP_PROP_POS_MSEC))
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=image_rgb)
    detection_result = detector.detect_for_video(mp_image, frame_timestamp_ms)
    
    # convert back to bgr for display
    annotated_image = mediaPipeDeclaration.draw_landmarks_on_image(image_rgb, detection_result)
    annotated_image_bgr = cv2.cvtColor(annotated_image, cv2.COLOR_RGB2BGR)

    return annotated_image_bgr, detection_result

# processes landmarks for each frame, tracking hand positions and movement
def process_landmarks(detection_result, frame_array, processed_frame_array, processing_active, swaying_detector, mirror_dectector):
    pose_landmarks_list = detection_result.pose_landmarks
    if pose_landmarks_list:
        for landmarks in pose_landmarks_list:
            if len(landmarks) > 16:
                # get right hand coordinates
                x16 = landmarks[16].x
                y16 = landmarks[16].y
                
                # store coordinates
                frame_array.append((x16, y16))
                if processing_active:
                    processed_frame_array.append((x16, y16))
                else:
                    processed_frame_array.append((np.nan, np.nan))

                # update movement detectors
                mirror_dectector.mirror_calculation(landmarks[15].x, landmarks[15].y, landmarks[16].x, landmarks[16].y)
                swaying_detector.midpoint_calculation(landmarks[12].x, landmarks[11].x)
                
                if processing_active:
                    swaying_detector.set_midpoint()
    return

# handles keyboard input for starting/stopping processing and exiting
def handle_user_input(key, frame_number, processing_active, current_start_frame, swaying_detector, processing_intervals):
    # start processing on 's' key
    if key == ord('s'):
        if not processing_active:
            current_start_frame = frame_number
            swaying_detector.set_midpoint_flag_true()
            print(f"Started processing at frame: {frame_number}")
            return True, current_start_frame
    
    # end processing on 'e' key
    elif key == ord('e'):
        if processing_active:
            processing_intervals.append((current_start_frame, frame_number))
            swaying_detector.set_midpoint_flag_false()
            print(f"Ended processing at frame: {frame_number}")
            return False, None
    
    # exit on ESC key
    elif key == 27:
        if processing_active:
            processing_intervals.append((current_start_frame, frame_number))
            print(f"Ended processing at frame: {frame_number}")
        return None, None

    return processing_active, current_start_frame

# main video processing loop for the first pass through the video
def process_video(cap, out, detector, frame_array, processed_frame_array, processing_intervals, swaying_detector, mirror_detector):
    # initialize processing variables
    frame_number = 0
    processing_active = False
    current_start_frame = None

    while cap.isOpened():
        success, image = cap.read()
        if not success:
            # save final interval if processing was active
            if processing_active and current_start_frame is not None:
                processing_intervals.append((current_start_frame, frame_number - 1))
                print(f"Ended processing at frame: {frame_number - 1}")
            break

        # verify frame is valid
        if image is None:
            continue

        # process current frame
        annotated_image_bgr, detection_result = process_frame(cap, detector)

        if annotated_image_bgr is not None:
            # display and process frame
            cv2.imshow('Video Feed - Selection Mode', annotated_image_bgr)
            process_landmarks(detection_result, frame_array, processed_frame_array, 
                           processing_active, swaying_detector, mirror_detector)

            # add frame number and save frame
            cv2.putText(annotated_image_bgr, f'Frame: {frame_number}', (10, 50), 
                       cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 255, 255), 2)
            out.write(annotated_image_bgr)

        # handle user input
        key = cv2.waitKey(5) & 0xFF
        processing_active, current_start_frame = handle_user_input(
            key, frame_number, processing_active, current_start_frame, 
            swaying_detector, processing_intervals)

        # exit if ESC pressed
        if processing_active is None:
            break

        frame_number += 1

    # cleanup resources
    cap.release()
    out.release()
    cv2.destroyAllWindows()

    return frame_array, processed_frame_array, processing_intervals
    


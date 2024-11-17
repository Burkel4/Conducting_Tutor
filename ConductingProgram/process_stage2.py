from imports import *

# processes a single frame and returns the annotated image
def process_frame(cap, detector):
    success, image = cap.read()
    if not success:
        return None

    image_bgr = image
    frame_timestamp_ms = round(cap.get(cv2.CAP_PROP_POS_MSEC))
    image_rgb = cv2.cvtColor(image_bgr, cv2.COLOR_BGR2RGB)
    mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=image_rgb)
    detection_result = detector.detect_for_video(mp_image, frame_timestamp_ms)
    annotated_image = mediaPipeDeclaration.draw_landmarks_on_image(image_rgb, detection_result)
    annotated_image_bgr = cv2.cvtColor(annotated_image, cv2.COLOR_RGB2BGR)

    return annotated_image_bgr

# checks if a frame index falls within any of the specified intervals
def is_within_intervals(frame_idx, intervals):
    return any(start <= frame_idx <= end for start, end in intervals)

# calculates bpm based on beats within the specified time window
def calculate_bpm(current_frame, beats, fps, window_duration):
    if len(beats) < 2:
        return 0
    
    # convert frames to seconds
    current_time = current_frame / fps
    beat_times = [beat / fps for beat in beats]
    
    # get recent beats within window
    recent_beats = [time for time in beat_times if current_time - time <= window_duration]
    
    if len(recent_beats) < 2:
        return 0
    
    # calculate time between first and last beat
    total_time = recent_beats[-1] - recent_beats[0]
    num_intervals = len(recent_beats) - 1
    
    # calculate and round bpm
    if total_time > 0:
        bpm = (num_intervals * 60) / total_time
    else:
        bpm = 0
    
    return round(bpm, 1)

# displays beat indicator and records bpm data
def print_beats(frame_index, annotated_image_bgr, filtered_significant_beats, beats, fps, bpm_window, text_display_counter):
   
    # setup text display parameters
    font = cv2.FONT_HERSHEY_SIMPLEX
    font_scale = 2
    font_thickness = 2
    font_color = (255, 255, 255)
    text = "Beat!"
    text_size = cv2.getTextSize(text, font, font_scale, font_thickness)[0]
    text_x = (annotated_image_bgr.shape[1] - text_size[0]) // 2
    text_y = (annotated_image_bgr.shape[0] + text_size[1]) // 2

    if frame_index in filtered_significant_beats:
        cv2.putText(annotated_image_bgr, text, (text_x, text_y), font, font_scale, font_color, font_thickness)

        beats.append(frame_index)
        bpm = calculate_bpm(frame_index, beats, fps, bpm_window)

        # save and display bpm data
        bpm_info = f'Beats per minute (BPM) at frame {frame_index}: {bpm}\n'
        print(bpm_info)
        output_file = video_bpm_output_name()
        with open(output_file, 'a') as file:
            file.write(bpm_info)

        text_display_counter = 3
    elif text_display_counter > 0:
        cv2.putText(annotated_image_bgr, text, (text_x, text_y), font, font_scale, font_color, font_thickness)
        text_display_counter -= 1

    return text_display_counter

# processes video for second pass, displaying beats and generating analysis
def output_process_video(cap, out, detector, filtered_significant_beats, processing_intervals, swaying_detector):
    
    # initialize parameters
    bpm_window = 5
    fps = int(cap.get(cv2.CAP_PROP_FPS))
    beats = []
    text_display_counter = 0
    frame_index = 0

    while cap.isOpened():
        success, image = cap.read()
        if not success:
            break

        annotated_image_bgr = process_frame(cap, detector)

        if is_within_intervals(frame_index, processing_intervals):
            text_display_counter = print_beats(frame_index, annotated_image_bgr, 
                                            filtered_significant_beats, beats, 
                                            fps, bpm_window, text_display_counter)

        swaying_detector.swaying_print(frame_index, annotated_image_bgr)

        # display frame number and update display
        cv2.putText(annotated_image_bgr, f'Frame: {frame_index}', (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 255, 255), 2)
        cv2.imshow('Annotated Frames', annotated_image_bgr)
        out.write(annotated_image_bgr)

        key = cv2.waitKey(5) & 0xFF
        if key == 27:
            break

        frame_index += 1

    # cleanup
    cap.release()
    out.release()
    cv2.destroyAllWindows()

    return
# This file includes the logic for beat detection information
# including x and y coords, peaks, vallys, etc..


from imports import *

# filters points based on minimum distance threshold
def filter_significant_points(points, threshold):
    if len(points) == 0:
        return []
        
    filtered_points = [points[0]]
    for i in range(1, len(points)):
        if points[i] - filtered_points[-1] > threshold:
            filtered_points.append(points[i])
            
    return filtered_points

# analyzes movement data to detect conducting beats
def filter_beats(frame_array, processed_frame_array):
    print("\n=== Beat Filter Debug Information ===")
    print(f"Input frame array length: {len(frame_array)}")
    print(f"Processed frame array length: {len(processed_frame_array)}")

    # extract x and y coordinates from frame arrays
    x = [coord[0] for coord in frame_array]
    y = [coord[1] for coord in frame_array]
    
    # convert to numpy arrays for processing
    x = np.array(x).flatten()
    y = np.array(y).flatten()

    # Invert y-coordinates once
    y_inverted = -y

    # find peaks and valleys in raw coordinates using inverted y
    y_peaks, _ = find_peaks(y_inverted, prominence=0.005, distance=5)
    y_valleys, _ = find_peaks(-y_inverted, prominence=0.005, distance=5)

    # process user-selected coordinates
    y_proc = np.array([coord[1] for coord in processed_frame_array]).flatten()
    y_proc_inverted = -y_proc  # Invert processed y-coordinates

    # find peaks and valleys in processed coordinates
    y_peaks_proc, _ = find_peaks(y_proc_inverted, prominence=0.005)
    y_valleys_proc, _ = find_peaks(-y_proc_inverted, prominence=0.005)

    # convert peak/valley indices to lists
    y_peaks_proc = list(y_peaks_proc)
    y_valleys_proc = list(y_valleys_proc)

    # combine all detected beats and filter by threshold
    filtered_significant_beats = list(y_peaks)
    # Get the x,y coordinates for each beat using inverted y-coordinates
    beat_coord_list = list(y_valleys)
    beat_coordinates = [(x[i], y_inverted[i]) for i in beat_coord_list]

    # Debugging output to verify structure
    print("Beat Coordinates:", beat_coordinates)

    # Before return, add debug info
    print(f"Number of y peaks: {len(y_peaks)}")
    print(f"Number of y valleys: {len(y_valleys)}")
    print(f"Number of filtered beats: {len(filtered_significant_beats)}")
    print("==================================\n")

    return filtered_significant_beats, beat_coordinates, y_peaks, y_valleys, y_inverted, y, x
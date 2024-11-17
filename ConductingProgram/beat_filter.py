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
    # extract x and y coordinates from frame arrays
    x = [coord[0] for coord in frame_array]
    y = [coord[1] for coord in frame_array]
    
    # convert to numpy arrays for processing
    x = np.array(x).flatten()
    y = np.array(y).flatten()

    # find peaks and valleys in raw coordinates
    x_peaks, _ = find_peaks(x)
    x_valleys, _ = find_peaks(-x)  # negate x for valleys
    y_peaks, _ = find_peaks(y)
    y_valleys, _ = find_peaks(-y)  # negate y for valleys

    # process filtered coordinates
    x_proc = np.array([coord[0] for coord in processed_frame_array]).flatten()
    y_proc = np.array([coord[1] for coord in processed_frame_array]).flatten()

    # find peaks and valleys in processed coordinates
    x_peaks_proc, _ = find_peaks(x_proc)
    x_valleys_proc, _ = find_peaks(-x_proc)
    y_peaks_proc, _ = find_peaks(y_proc)
    y_valleys_proc, _ = find_peaks(-y_proc)

    # convert peak/valley indices to lists
    x_peaks_proc = list(x_peaks_proc)
    x_valleys_proc = list(x_valleys_proc)
    y_peaks_proc = list(y_peaks_proc)
    y_valleys_proc = list(y_valleys_proc)

    # combine all detected beats and filter by threshold
    threshold = 5  # minimum frames between beats can be adjusted, but 5 works well
    significant_beats = sorted(set(x_peaks_proc + x_valleys_proc + y_peaks_proc + y_valleys_proc))
    filtered_significant_beats = filter_significant_points(significant_beats, threshold)

    return filtered_significant_beats, x_peaks, x_valleys, y_peaks, y_valleys, x, y

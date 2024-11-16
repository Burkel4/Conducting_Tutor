from matplotlib import pyplot as plt
from matplotlib.collections import LineCollection
from matplotlib.colors import LinearSegmentedColormap
import numpy as np
from name import *

def beatPlotGraph(intervals, beats, x_valleys, y_peaks, y_valleys, x, y):
    plt.figure(figsize=(12, 6))
    plt.plot(range(len(x)), x, label='X Coordinates', color='b', alpha=0.7)
    plt.plot(range(len(y)), y, label='Y Coordinates', color='g', alpha=0.7)

    # Highlight each processing interval individually on the plot
    if intervals:  # Ensure there are intervals to process
        for start, end in intervals:
            plt.axvspan(start, end, color='yellow', alpha=0.3, label="Processed Range" if start == intervals[0][0] else None)

    # Plot uniform beat markers for all filtered peaks and valleys
    all_beats = sorted(beats)
    all_beat_values = [x[i] if i < len(x) else y[i - len(x)] for i in all_beats]
    # Plot vertical lines for all filtered peaks and valleys
    for beat in all_beats:
        plt.axvline(x=beat, color='purple', linestyle='--', label="Beats" if beat == all_beats[0] else None)
    plt.plot(x_valleys, [x[i] for i in x_valleys], "x", label="X Valleys")
    plt.plot(y_peaks, [y[i] for i in y_peaks], "o", label="Y Peaks")
    plt.plot(y_valleys, [y[i] for i in y_valleys], "o", label="Y Valleys")
    plt.title('X and Y Coordinates Over Frame Number')
    plt.xlabel('Frame Number')
    plt.ylabel('Coordinate Value')
    plt.legend()
    plt.grid(True)
    plt.savefig(videoBeatPlotName +'.png')
    plt.show()

def handPathGraph(x_proc, y_proc): 
    plt.figure(figsize=(12, 6))
    valid_mask = ~(np.isnan(x_proc) | np.isnan(y_proc))
    x_valid = x_proc[valid_mask]
    y_valid = y_proc[valid_mask]
    y_valid = -y_valid  
    points = np.array([x_valid, y_valid]).T.reshape(-1, 1, 2)
    segments = np.concatenate([points[:-1], points[1:]], axis=1)
    colors = ['blue', 'red']
    n_bins = len(x_valid)
    custom_cmap = LinearSegmentedColormap.from_list("custom", colors, N=n_bins)
    norm = plt.Normalize(0, len(x_valid))
    lc = LineCollection(segments, cmap=custom_cmap, norm=norm)
    lc.set_array(np.arange(len(x_valid)))
    plt.gca().add_collection(lc)
    plt.xlim(np.nanmin(x_valid), np.nanmax(x_valid))
    plt.ylim(np.nanmin(y_valid), np.nanmax(y_valid))
    cbar = plt.colorbar(lc)
    cbar.set_label('Frame Number')
    plt.xlabel("X-Coords")
    plt.ylabel("Y-Coords")
    plt.title("Conducting Pattern")
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.savefig(videoConductPathName + '.png', bbox_inches='tight')
    plt.show()

def swayingGraph(mid, defualt_mid, threshold):
    plt.figure(figsize=(12, 6))
    plt.plot(range(len(mid)), mid, label='Current Midpoint X', color='b', alpha=0.7)
    plt.axhline(y=defualt_mid, color='k', linestyle='-', label='Default Midpoint X')
    plt.axhline(y=defualt_mid + threshold, color='r', linestyle='--', label='Upper Threshold X')
    plt.axhline(y=defualt_mid - threshold, color='r', linestyle='--', label='Lower Threshold X')
    plt.title('Swaying Detection Over Frame Number')
    plt.xlabel('Frame Number')
    plt.ylabel('Midpoint X Value')
    plt.legend()
    plt.grid(True)
    plt.savefig(videoSwayPlotName + '.png')
    plt.show()

def mirrorXCoordinateGraph(left_hand_x, right_hand_x): # Plot the hand coordinates graph x 
    plt.figure(figsize=(12, 6))
    plt.plot(range(len(left_hand_x)), [x - left_hand_x[0] for x in left_hand_x], label='Left Hand X', color='b', alpha=0.7)
    plt.plot(range(len(right_hand_x)), [x - right_hand_x[0] for x in right_hand_x], label='Right Hand X', color='g', alpha=0.7)
    plt.axhline(y=0, color='k', linestyle='-', label='Default Line')
    plt.title('Hands X Coordinates Over Frame Number')
    plt.xlabel('Frame Number')
    plt.ylabel('Coordinate Value')
    plt.legend()
    plt.grid(True)
    plt.savefig(videoHandsPlot_XName + '.png')
    plt.show()

def mirrorYCoordinateGraph(left_hand_y, right_hand_y): # Plot the hand coordinates graph y 
    plt.figure(figsize=(12, 6))
    plt.plot(range(len(left_hand_y)), [y - left_hand_y[0] for y in left_hand_y], label='Left Hand Y', color='r', alpha=0.7)
    plt.plot(range(len(right_hand_y)), [y - right_hand_y[0] for y in right_hand_y], label='Right Hand Y', color='m', alpha=0.7)
    plt.axhline(y=0, color='k', linestyle='-', label='Default Line')
    plt.title('Hands Y Coordinates Over Frame Number')
    plt.xlabel('Frame Number')
    plt.ylabel('Coordinate Value')
    plt.legend()
    plt.grid(True)
    plt.savefig(videohandsPlotName_YName + '.png')
    plt.show()


# Standard library imports
import numpy as np
import cv2
from matplotlib import pyplot as plt
from matplotlib.collections import LineCollection
from matplotlib.colors import LinearSegmentedColormap
from scipy.signal import find_peaks
import time
import sys
#PyGame
import pygame
from numpy import mean

# Mediapipe imports
import mediapipe as mp
from mediapipe.framework.formats import landmark_pb2

# Local imports
from names import *
from pattern import *
from mp_declaration import mediaPipeDeclaration
from p_stage1 import process_video
from p_stage2 import output_process_video
from beat_filter import filter_beats
from sway import swayingDetection
from mirror import mirrorDetection
from graphs import generate_all_graphs
from interface import display_frame, get_screen, get_window_size
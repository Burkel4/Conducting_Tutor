# This file stores all imports into one place
from names import *

# Standard library imports
import numpy as np
import cv2
from matplotlib import pyplot as plt
from matplotlib.collections import LineCollection
from matplotlib.colors import LinearSegmentedColormap
from scipy.signal import find_peaks
from numpy import mean
from sklearn.cluster import KMeans # type: ignore 

# Mediapipe imports
import mediapipe as mp
from mediapipe.framework.formats import landmark_pb2

# Local imports
from beat_filter import *
from cueing import *
from elbow import *
from graphs import *
from main import *
from mirror import* 
from mp_declaration import *
from names import *
from p_stage1 import *
from p_stage2 import *
from start_end import *
from sway import *
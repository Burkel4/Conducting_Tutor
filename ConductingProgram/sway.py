import cv2

class swayingDetection:

    def __init__(self):
        self.default_midpoint_x = 0
        self.sway_threshold = 0.025  # Threshold for swaying detection
        self.midpoints_x = []
        self.midpoints_z = []
        self.midpointflag = False


    def midpoint_calculation(self, x12, x11):
        self.midpoint_x = abs(x12 - x11) * 0.5 + x12
        self.midpoints_x.append(self.midpoint_x)
        return


    def set_midpoint(self):
        if self.midpointflag:
            self.default_midpoint_x = self.midpoint_x
            self.set_midpoint_flag_false()
            return
    

    def set_midpoint_flag_true(self):
        self.midpointflag = True
        return
    

    def set_midpoint_flag_false(self):
        self.midpointflag = False
        return
    
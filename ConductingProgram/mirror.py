

class mirrorDetection:

    # Lists to store hand coordinates
    def __init__(self):
        self.left_hand_x = []
        self.left_hand_y = []
        self.right_hand_x = []
        self.right_hand_y = []

    def mirror_calculation(self, left_x, left_y, right_x, right_y):
        self.left_hand_x.append(left_x)
        self.left_hand_y.append(left_y)
        self.right_hand_x.append(right_x)
        self.right_hand_y.append(right_y)

        return
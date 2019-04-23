"""
Collection of constants over the BSTLD Tensorflow sample detection
"""

WIDTH = 960
HEIGHT = 720

SIMPLIFIED_CLASSES = {
    'Green': 'Green',
    'GreenLeft': 'Green',
    'GreenRight': 'Green',
    'GreenStraight': 'Green',
    'GreenStraightRight': 'Green',
    'GreenStraightLeft': 'Green',
    'Yellow': 'Yellow',
    'Red': 'Red',
    'RedLeft': 'Red',
    'RedRight': 'Red',
    'RedStraight': 'Red',
    'RedStraightLeft': 'Red',
    'Off': 'Off',
    'off': 'Off',
}

CLASS_COLORS = {
    # BGR
    1: (0, 255, 0),      # GREEN
    2: (0, 0, 255),      # RED
    3: (0, 255, 255),    # YELLOW
    4: (255, 255, 255),  # Off currently set to white for visibility
}

# 1 based class indices as requested by tf object detection
TF_CATEGORIES = {
    1: 'Green',
    2: 'Red',
    3: 'Yellow',
    4: 'Off',
}
# zero based class indices
EVAL_CATEGORIES = {key - 1: val for key, val in TF_CATEGORIES.items()}

# Label string to tf label id
TF_ID_MAP = {val: key for key, val in TF_CATEGORIES.items()}

# Label string to evaluation label id ('Green': 1
EVAL_ID_MAP = {val: key for key, val in EVAL_CATEGORIES.items()}

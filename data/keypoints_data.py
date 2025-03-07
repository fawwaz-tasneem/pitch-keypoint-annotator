from PyQt6 import QtGui

# (keypoint_no, keypoint_x, keypoint_y, keypoint_name)
KEYPOINTS_DATA = [
    (1, 0, 0, "far_left_corner"),
    (2, 52.5, 0, "far_center_line_end"),
    (3, 105, 0, "far_right_corner"),
    (4, 0, 13.84, "left_outer_box_far_left"),
    (5, 16.5, 13.84, "left_outer_box_far_right"),
    (6, 88.5, 13.84, "right_outer_box_far_left"),
    (7, 105, 13.84, "right_outer_box_far_right"),
    (8, 0, 24.84, "left_inner_box_far_left"),
    (9, 5.5, 24.84, "left_inner_box_far_right"),
    (10, 99.5, 24.84, "right_inner_box_far_left"),
    (11, 105, 24.84, "right_inner_box_far_right"),
    (12, 52.5, 24.85, "center_circle_far_point"),
    (13, 16.5, 26.69, "left_arc_far_point"),
    (14, 88.5, 26.69, "right_arc_far_point"),
    (15, 0, 30.34, "left_goal_far_post"),
    (16, 105, 30.34, "right_goal_far_post"),
    (17, 11, 34, "left_penalty_spot"),
    (18, 52.5, 34, "center_circle_center"),
    (19, 94, 34, "right_penalty_spot"),
    (20, 0, 37.66, "left_goal_near_post"),
    (21, 105, 37.66, "right_goal_near_post"),
    (22, 16.5, 41.31, "left_arc_near_point"),
    (23, 88.5, 41.31, "right_arc_near_point"),
    (24, 52.5, 43.15, "center_circle_near_point"),
    (25, 0, 43.16, "left_inner_box_near_left"),
    (26, 5.5, 43.16, "left_inner_box_near_right"),
    (27, 99.5, 43.16, "right_inner_box_near_left"),
    (28, 105, 43.16, "right_inner_box_near_right"),
    (29, 0, 54.16, "left_outer_box_near_left"),
    (30, 16.5, 54.16, "left_outer_box_near_right"),
    (31, 88.5, 54.16, "right_outer_box_near_left"),
    (32, 105, 54.16, "right_outer_box_near_right"),
    (33, 0, 68, "near_left_corner"),
    (34, 52.5, 68, "near_center_line_end"),
    (35, 105, 68, "near_right_corner"),
]

# Pairs of keypoint numbers to connect with lines
CONNECTIONS = [
    (33, 35),
    (33, 1),
    (1, 3),
    (35, 3),
    (29, 30),
    (30, 5),
    (4, 5),
    (34, 2),
    (32, 31),
    (31, 6),
    (6, 7),
    (25, 26),
    (26, 9),
    (9, 8),
    (28, 27),
    (27, 10),
    (10, 11),
    (16, 21),
    (20, 15),
]

def generate_unique_colors(n):
    """
    Generate n distinct colors by distributing hues around the color wheel.
    Returns a list of QColor objects.
    """
    colors = []
    for i in range(n):
        hue = int((i / n) * 360)  # from 0 to 359
        color = QtGui.QColor.fromHsv(hue, 255, 255)
        colors.append(color)
    return colors

def build_keypoint_dict():
    """
    Build a dictionary:
      key:   keypoint_name (e.g. "far_left_corner")
      value: { "number": int, "x": float, "y": float, "color": QColor }
    """
    all_colors = generate_unique_colors(len(KEYPOINTS_DATA))
    kp_dict = {}
    for i, (no, x, y, name) in enumerate(KEYPOINTS_DATA):
        kp_dict[name] = {
            "number": no,
            "x": x,
            "y": y,
            "color": all_colors[i]
        }
    return kp_dict

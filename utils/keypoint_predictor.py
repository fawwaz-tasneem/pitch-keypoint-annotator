# utils/keypoint_predictor.py
import cv2
import numpy as np
import logging

def predict_keypoints(prev_frame, next_frame, prev_points):
    """
    Predict keypoints in the next frame using Lucas-Kanade optical flow.
    
    Args:
        prev_frame (np.array): Grayscale image of frame N.
        next_frame (np.array): Grayscale image of frame N+1.
        prev_points (np.array): Array of shape (N, 1, 2) containing keypoint positions in frame N.
    
    Returns:
        next_points (np.array): Predicted keypoint positions in frame N+1.
        status (np.array): Array indicating success (1) or failure (0) for each keypoint.
    
    Raises:
        ValueError: If input images or keypoint array is invalid.
    """
    try:
        if prev_frame is None or next_frame is None:
            raise ValueError("Input frames cannot be None.")
        if prev_points is None or len(prev_points) == 0:
            raise ValueError("No previous keypoint positions provided.")

        # Ensure the frames are 2D (grayscale)
        if len(prev_frame.shape) != 2 or len(next_frame.shape) != 2:
            raise ValueError("Input frames must be grayscale images (2D arrays).")
        
        lk_params = dict(
            winSize  = (15, 15),
            maxLevel = 2,
            criteria = (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 0.03)
        )
        
        next_points, status, _ = cv2.calcOpticalFlowPyrLK(prev_frame, next_frame, prev_points, None, **lk_params)
        return next_points, status
    except Exception as e:
        logging.exception("Error in predict_keypoints: %s", e)
        raise

def convert_annotations_to_array(annotations, keypoint_names):
    """
    Convert an annotation dictionary into a NumPy array for optical flow.
    
    Args:
        annotations (dict): { keypoint_name: {"visible": 1, "x": int, "y": int} }
        keypoint_names (list): List of keypoint names in desired order.
    
    Returns:
        np.array: Array of shape (N, 1, 2) of type np.float32.
    """
    points = []
    for name in keypoint_names:
        data = annotations.get(name, None)
        if data and data.get("visible") == 1:
            points.append([float(data["x"]), float(data["y"])])
        else:
            # If not annotated, use a placeholder (NaN) that can be handled later.
            points.append([np.nan, np.nan])
    arr = np.array(points, dtype=np.float32).reshape(-1, 1, 2)
    return arr

def update_annotations_with_predictions(keypoint_names, predicted_points, status):
    """
    Update a dictionary of annotations using predicted keypoint positions.
    
    For each keypoint in keypoint_names, if the corresponding optical flow was found,
    set its annotation to {"visible": 1, "x": int, "y": int}. Otherwise, mark it not visible.
    
    Args:
        keypoint_names (list): List of keypoint names.
        predicted_points (np.array): Array of shape (N, 1, 2) containing predicted positions.
        status (np.array): Status array indicating if prediction succeeded (1) or not (0).
    
    Returns:
        dict: Updated annotations.
    """
    updated_annotations = {}
    for i, name in enumerate(keypoint_names):
        st = status[i][0]
        if st == 1:
            x, y = predicted_points[i][0]
            # Check for valid numbers (in case optical flow returned NaN)
            if np.isnan(x) or np.isnan(y):
                updated_annotations[name] = {"visible": 0}
            else:
                updated_annotations[name] = {"visible": 1, "x": int(x), "y": int(y)}
        else:
            updated_annotations[name] = {"visible": 0}
    return updated_annotations

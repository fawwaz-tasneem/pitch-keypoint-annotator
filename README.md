Pitch Keypoint Annotation Tool
===============================

Overview
--------
The Pitch Keypoint Annotation Tool is a Python-based application that allows users to annotate keypoints on video frames of a football pitch. Users can label 35 predefined keypoints, navigate between frames, and save annotations in a JSON format. The tool also features an optical flow-based predictor (using the Lucas-Kanade algorithm) to automatically estimate keypoint positions in the next frame, which can then be manually adjusted if needed.

Features
--------
- **Video Frame Extraction:**  
  Extract frames from a video using OpenCV.

- **Frame Annotation:**  
  Annotate 35 unique keypoints on each frame with unique colors.

- **Graphical User Interface:**  
  A PyQt6-based GUI featuring:
  - A central display for the current frame.
  - A pitch reference panel showing a scaled football pitch with keypoints and connection lines.
  - Menus, toolbars, and keyboard shortcuts for rapid keypoint selection and navigation.

- **Keyboard Shortcuts:**  
  Type keypoint numbers and use the spacebar to select keypoints quickly.

- **Optical Flow Prediction:**  
  Predict keypoint locations in the next frame using optical flow, speeding up the annotation process.

- **Session Management:**  
  Save and load annotation sessions in JSON format.

Installation
------------
1. **Prerequisites:**  
   - Python 3.x

2. **Install Required Packages:**  
   Run the following command to install dependencies:
   ```
   pip install PyQt6 opencv-python numpy
   ```

3. **Download the Project:**  
   Clone or download the project repository.

Directory Structure
-------------------
The project is organized as follows:

```
pitch_annotation_tool/
├── main.py               - Entry point of the application.
├── gui/
│   ├── __init__.py
│   ├── annotation_tool.py  - Main window and GUI integration.
│   ├── annotation_scene.py - Custom QGraphicsScene for frame annotation.
│   └── pitch_reference.py  - Displays the reference football pitch.
├── data/
│   ├── __init__.py
│   └── keypoints_data.py   - Defines the 35 keypoints and their connections.
└── utils/
    ├── __init__.py
    ├── frame_extractor.py  - Extracts frames from a video.
    └── keypoint_predictor.py - Optical flow prediction of keypoints.
```

Usage
-----
1. **Run the Application:**  
   Execute the following command in the project root:
   ```
   python main.py
   ```

2. **Load a Video:**  
   Use the "Load Video" option in the menu or toolbar to select and load a video file.

3. **Annotate Frames:**  
   - Select a keypoint via the menu or by typing its number and pressing the spacebar.
   - Click on the frame to place or update the keypoint marker.
   - Only one marker per keypoint is allowed; re-clicking updates the marker.

4. **Navigate Frames:**  
   Use the "Next Frame" and "Prev Frame" buttons to move through frames.

5. **Predict Keypoints:**  
   Click "Predict Next Frame Keypoints" to use optical flow and automatically annotate the next frame based on current frame annotations. The predictions can be manually adjusted.

6. **Session Management:**  
   Save your work with "Save Session" and reload it later with "Load Session".

Customization
-------------
- **Keypoint Data:**  
  Modify `data/keypoints_data.py` to change keypoint definitions or connections.

- **Optical Flow Parameters:**  
  Adjust the prediction settings in `utils/keypoint_predictor.py` if needed.

- **GUI Layout:**  
  Customize the appearance and layout by editing the files in the `gui/` directory.

Troubleshooting
---------------
- Ensure that your video is in a supported format (e.g., MP4, AVI).
- If the frame or annotations do not display correctly, verify that the frame extraction process is working.
- For issues with keypoint prediction, check the conversion of video frames to grayscale images.

License
-------
(Include license details if applicable, e.g., MIT License.)

Contact
-------
For questions or support, please contact Fawwaz Bin Tasneem at tasneemfawwaz@gmail.com.

---

This README provides an overview of the project, installation instructions, usage details, and a breakdown of the code structure, making it easy for any user or developer to understand and work with the project.

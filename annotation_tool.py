import os
import json
from PyQt6 import QtWidgets, QtGui, QtCore
from .annotation_scene import AnnotationScene
from .pitch_reference import PitchReference
from utils.frame_extractor import extract_frames
from data.keypoints_data import build_keypoint_dict

class AnnotationTool(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Pitch Keypoint Annotation Tool")
        self.resize(1300, 900)
        # Ensure the main window gets key events.
        self.setFocusPolicy(QtCore.Qt.FocusPolicy.StrongFocus)
        
        # Build keypoint dictionary.
        self.keypoints_dict = build_keypoint_dict()
        self.session_annotations = {}
        self.current_frame_index = 0
        self.frames = []
        self.shortcut_buffer = ""  # Buffer to store typed digits.
        
        self.create_widgets()
        self.create_menus()
        self.create_toolbar()
        
        # Set up QShortcut for Space key.
        # We use the default context (which is ApplicationShortcut) so that
        # even if some child widget has focus, the shortcut still triggers.
        self.space_shortcut = QtGui.QShortcut(QtGui.QKeySequence("Space"), self)
        self.space_shortcut.activated.connect(self.space_pressed)
        
        # Force focus to the main window.
        self.setFocus()

    def create_widgets(self):
        # Shortcut label (shows typed digits)
        self.shortcut_label = QtWidgets.QLabel("Shortcut: ")
        font = QtGui.QFont()
        font.setPointSize(9)
        self.shortcut_label.setFont(font)
        self.shortcut_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignLeft)
        
        # Frame label above the image (smaller font)
        self.frame_label = QtWidgets.QLabel("Frame: 0")
        self.frame_label.setFont(font)
        self.frame_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        
        # GraphicsView for annotation.
        self.graphics_view = QtWidgets.QGraphicsView()
        # Ensure the QGraphicsView does not capture key events.
        self.graphics_view.setFocusPolicy(QtCore.Qt.FocusPolicy.NoFocus)
        self.scene = AnnotationScene(self.keypoints_dict, parent=self)
        self.graphics_view.setScene(self.scene)
        self.graphics_view.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing)
        self.graphics_view.setRenderHint(QtGui.QPainter.RenderHint.SmoothPixmapTransform)
        
        # Layout for the top labels.
        top_label_layout = QtWidgets.QHBoxLayout()
        top_label_layout.addWidget(self.frame_label, stretch=1)
        top_label_layout.addWidget(self.shortcut_label, stretch=2)
        
        # Vertical layout: labels on top, then the graphics view.
        self.central_frame_layout = QtWidgets.QVBoxLayout()
        self.central_frame_layout.addLayout(top_label_layout)
        self.central_frame_layout.addWidget(self.graphics_view)
        
        # Right panel: pitch reference.
        self.pitch_reference = PitchReference(self.keypoints_dict, parent=self)
        
        # Main horizontal layout.
        central_widget = QtWidgets.QWidget()
        h_layout = QtWidgets.QHBoxLayout(central_widget)
        h_layout.addLayout(self.central_frame_layout, stretch=4)
        h_layout.addWidget(self.pitch_reference, stretch=2)
        
        self.setCentralWidget(central_widget)

    def create_menus(self):
        menu = self.menuBar()
        
        session_menu = menu.addMenu("Session")
        load_session_action = QtGui.QAction("Load Session", self)
        load_session_action.triggered.connect(self.load_session)
        session_menu.addAction(load_session_action)
        
        save_session_action = QtGui.QAction("Save Session", self)
        save_session_action.triggered.connect(self.save_session)
        session_menu.addAction(save_session_action)
        
        video_menu = menu.addMenu("Video")
        load_video_action = QtGui.QAction("Load Video", self)
        load_video_action.triggered.connect(self.load_video)
        video_menu.addAction(load_video_action)
        
        nav_menu = menu.addMenu("Navigation")
        prev_frame_action = QtGui.QAction("Previous Frame", self)
        prev_frame_action.triggered.connect(self.prev_frame)
        nav_menu.addAction(prev_frame_action)
        
        next_frame_action = QtGui.QAction("Next Frame", self)
        next_frame_action.triggered.connect(self.next_frame)
        nav_menu.addAction(next_frame_action)
        
        keypoint_menu = menu.addMenu("Keypoints")
        for kp_name, info in self.keypoints_dict.items():
            action = QtGui.QAction(kp_name, self)
            action.triggered.connect(lambda checked, n=kp_name: self.set_active_keypoint(n))
            keypoint_menu.addAction(action)

    def create_toolbar(self):
        toolbar = self.addToolBar("Main Toolbar")
        load_video_btn = QtGui.QAction("Load Video", self)
        load_video_btn.triggered.connect(self.load_video)
        toolbar.addAction(load_video_btn)
        
        prev_btn = QtGui.QAction("Prev Frame", self)
        prev_btn.triggered.connect(self.prev_frame)
        toolbar.addAction(prev_btn)
        
        next_btn = QtGui.QAction("Next Frame", self)
        next_btn.triggered.connect(self.next_frame)
        toolbar.addAction(next_btn)
        
        load_session_btn = QtGui.QAction("Load Session", self)
        load_session_btn.triggered.connect(self.load_session)
        toolbar.addAction(load_session_btn)
        
        save_session_btn = QtGui.QAction("Save Session", self)
        save_session_btn.triggered.connect(self.save_session)
        toolbar.addAction(save_session_btn)

    def keyPressEvent(self, event):
        """
        Capture digit key presses using event.text() and Backspace.
        (Space is handled via QShortcut.)
        """
        text = event.text()
        if text.isdigit():
            self.shortcut_buffer += text
            self.shortcut_label.setText(f"Shortcut: {self.shortcut_buffer}")
        elif event.key() == QtCore.Qt.Key_Backspace:
            self.shortcut_buffer = self.shortcut_buffer[:-1]
            self.shortcut_label.setText(f"Shortcut: {self.shortcut_buffer}")
        else:
            super().keyPressEvent(event)

    def space_pressed(self):
        """
        Slot called when Space is pressed (via QShortcut).
        Parse the shortcut buffer and, if valid, select the keypoint.
        """
        if self.shortcut_buffer:
            try:
                no = int(self.shortcut_buffer)
            except ValueError:
                no = -1
            self.shortcut_buffer = ""
            self.shortcut_label.setText("Shortcut: ")
            if no > 0:
                found_name = None
                for name, info in self.keypoints_dict.items():
                    if info["number"] == no:
                        found_name = name
                        break
                if found_name:
                    self.set_active_keypoint(found_name)
                else:
                    self.statusBar().showMessage(f"No keypoint #{no} found.")

    def load_video(self):
        video_path, _ = QtWidgets.QFileDialog.getOpenFileName(
            self, "Select Video File", "", "Video Files (*.mp4 *.avi)"
        )
        if video_path:
            output_folder = "frames"
            extract_frames(video_path, output_folder)
            self.frames = sorted(
                os.path.join(output_folder, f)
                for f in os.listdir(output_folder)
                if f.endswith(".jpg")
            )
            self.current_frame_index = 0
            self.load_frame()

    def load_frame(self):
        if not self.frames:
            return
        frame_path = self.frames[self.current_frame_index]
        pixmap = QtGui.QPixmap(frame_path)
        self.scene.clear_annotations()
        self.scene.addPixmap(pixmap)
        self.scene.setSceneRect(0, 0, pixmap.width(), pixmap.height())
        self.graphics_view.fitInView(self.scene.sceneRect(), QtCore.Qt.AspectRatioMode.KeepAspectRatio)
        self.frame_label.setText(f"Frame: {self.current_frame_index + 1}")
        frame_name = os.path.basename(frame_path)
        if frame_name in self.session_annotations:
            ann = self.session_annotations[frame_name]
            self.scene.load_annotations(ann)

    def next_frame(self):
        self.save_current_annotations()
        if self.current_frame_index < len(self.frames) - 1:
            self.current_frame_index += 1
            self.load_frame()

    def prev_frame(self):
        self.save_current_annotations()
        if self.current_frame_index > 0:
            self.current_frame_index -= 1
            self.load_frame()

    def save_current_annotations(self):
        if not self.frames:
            return
        frame_name = os.path.basename(self.frames[self.current_frame_index])
        self.session_annotations[frame_name] = self.scene.get_annotations()

    def set_active_keypoint(self, keypoint_name):
        """
        Called either from the menu or via keyboard shortcut.
        Highlights the keypoint in the pitch reference and sets it as active in the annotation scene.
        """
        keypoint_no = self.keypoints_dict[keypoint_name]["number"]
        self.pitch_reference.highlight_keypoint_by_number(keypoint_no)
        self.scene.set_active_keypoint(keypoint_name)
        self.statusBar().showMessage(f"Selected keypoint: {keypoint_no} - {keypoint_name}")

    def save_session(self):
        self.save_current_annotations()
        fname, _ = QtWidgets.QFileDialog.getSaveFileName(self, "Save Session", "", "JSON Files (*.json)")
        if fname:
            with open(fname, "w") as f:
                json.dump(self.session_annotations, f, indent=2)
            self.statusBar().showMessage("Session saved.")

    def load_session(self):
        fname, _ = QtWidgets.QFileDialog.getOpenFileName(self, "Load Session", "", "JSON Files (*.json)")
        if fname:
            with open(fname, "r") as f:
                self.session_annotations = json.load(f)
            self.load_frame()
            self.statusBar().showMessage("Session loaded.")

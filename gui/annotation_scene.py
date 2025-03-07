from PyQt6 import QtWidgets, QtGui, QtCore

class AnnotationScene(QtWidgets.QGraphicsScene):
    def __init__(self, keypoints_dict, parent=None):
        super().__init__(parent)
        self.keypoints_dict = keypoints_dict  # name -> { "color": QColor, ... }
        self.active_keypoint = None
        self.annotations = {}

    def clear_annotations(self):
        self.clear()
        self.annotations = {}

    def mousePressEvent(self, event):
        if self.active_keypoint is None:
            return
        pos = event.scenePos()
        
        self.annotations[self.active_keypoint] = {
            "visible": 1,
            "x": int(pos.x()),
            "y": int(pos.y())
        }
        
        color = self.keypoints_dict[self.active_keypoint]["color"]
        brush = QtGui.QBrush(color)
        radius = 5
        self.addEllipse(pos.x()-radius, pos.y()-radius, radius*2, radius*2,
                        QtGui.QPen(QtCore.Qt.PenStyle.NoPen), brush)
        super().mousePressEvent(event)

    def set_active_keypoint(self, keypoint_name):
        self.active_keypoint = keypoint_name

    def load_annotations(self, annotations):
        # Redraw any existing annotations for this frame
        for kp_name, data in annotations.items():
            if data.get("visible"):
                color = self.keypoints_dict[kp_name]["color"]
                brush = QtGui.QBrush(color)
                radius = 5
                self.addEllipse(data["x"]-radius, data["y"]-radius, radius*2, radius*2,
                                QtGui.QPen(QtCore.Qt.PenStyle.NoPen), brush)
        self.annotations = annotations

    def get_annotations(self):
        return self.annotations

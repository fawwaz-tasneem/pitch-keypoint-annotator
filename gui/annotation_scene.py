from PyQt6 import QtWidgets, QtGui, QtCore

class AnnotationScene(QtWidgets.QGraphicsScene):
    def __init__(self, keypoints_dict, parent=None):
        super().__init__(parent)
        self.keypoints_dict = keypoints_dict  # name -> { "color": QColor, ... }
        self.active_keypoint = None
        self.annotations = {}
        # Track drawn ellipse items per keypoint to avoid duplicates
        self.annotation_items = {}

    def clear_annotations(self):
        self.clear()
        self.annotations = {}
        self.annotation_items = {}

    def mousePressEvent(self, event):
        if self.active_keypoint is None:
            return
        pos = event.scenePos()
        
        self.annotations[self.active_keypoint] = {
            "visible": 1,
            "x": int(pos.x()),
            "y": int(pos.y())
        }
        
        # Remove previous marker for this keypoint, if any
        if self.active_keypoint in self.annotation_items:
            self.removeItem(self.annotation_items[self.active_keypoint])

        color = self.keypoints_dict[self.active_keypoint]["color"]
        brush = QtGui.QBrush(color)
        radius = 5
        ellipse = self.addEllipse(
            pos.x()-radius, pos.y()-radius, radius*2, radius*2,
            QtGui.QPen(QtCore.Qt.PenStyle.NoPen), brush
        )
        self.annotation_items[self.active_keypoint] = ellipse
        super().mousePressEvent(event)

    def set_active_keypoint(self, keypoint_name):
        self.active_keypoint = keypoint_name

    def load_annotations(self, annotations):
        # Clear existing markers only (keep background)
        for item in self.annotation_items.values():
            self.removeItem(item)
        self.annotation_items = {}

        # Redraw markers from provided annotations
        for kp_name, data in annotations.items():
            if data.get("visible"):
                color = self.keypoints_dict[kp_name]["color"]
                brush = QtGui.QBrush(color)
                radius = 5
                ellipse = self.addEllipse(
                    data["x"]-radius, data["y"]-radius, radius*2, radius*2,
                    QtGui.QPen(QtCore.Qt.PenStyle.NoPen), brush
                )
                self.annotation_items[kp_name] = ellipse
        # Replace annotations dict
        self.annotations = dict(annotations)

    def get_annotations(self):
        return self.annotations

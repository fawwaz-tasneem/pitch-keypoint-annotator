from PyQt6 import QtWidgets, QtGui, QtCore
from data.keypoints_data import KEYPOINTS_DATA, CONNECTIONS

class PitchReference(QtWidgets.QGraphicsView):
    """
    A QGraphicsView showing a scaled 2D pitch (105m x 68m)
    with 35 keypoints (displaying their number by default)
    and lines connecting them. When a keypoint is highlighted,
    its marker and text double in size and the text changes to show the name.
    """
    def __init__(self, keypoints_dict, parent=None):
        super().__init__(parent)
        # keypoints_dict: name -> { "number": int, "x": float, "y": float, "color": QColor }
        self.keypoints_dict = keypoints_dict
        # Map keypoint_number -> keypoint_name
        self.num_to_name = {info["number"]: name for name, info in self.keypoints_dict.items()}
        # Store (circle_item, text_item) for each keypoint (keyed by number)
        self.keypoint_items = {}
        self.current_highlight = None  # currently highlighted keypoint number

        self.scene = QtWidgets.QGraphicsScene(self)
        self.setScene(self.scene)

        self.PITCH_WIDTH = 105.0
        self.PITCH_HEIGHT = 68.0
        self.PADDING = 10.0  # 10px padding on each side
        self.SCALE = 5.0     # scale factor for pitch

        self.draw_pitch()

    def draw_pitch(self):
        self.scene.clear()
        self.keypoint_items.clear()

        total_width = self.PADDING * 2 + self.PITCH_WIDTH * self.SCALE
        total_height = self.PADDING * 2 + self.PITCH_HEIGHT * self.SCALE

        # Draw pitch boundary
        boundary_rect = QtCore.QRectF(0, 0, total_width, total_height)
        self.scene.addRect(boundary_rect, QtGui.QPen(QtGui.QColor("black"), 2))

        font = QtGui.QFont("Arial", 8)

        # Draw each keypoint (showing only the number by default)
        for name, info in self.keypoints_dict.items():
            no = info["number"]
            color = info["color"]
            x_px = self.PADDING + info["x"] * self.SCALE
            y_px = self.PADDING + info["y"] * self.SCALE

            circle_radius = 4
            circle_brush = QtGui.QBrush(color)
            circle_item = self.scene.addEllipse(
                x_px - circle_radius,
                y_px - circle_radius,
                circle_radius * 2,
                circle_radius * 2,
                QtGui.QPen(QtCore.Qt.PenStyle.NoPen),
                circle_brush
            )
            # Set the transform origin to the center so scaling preserves position
            circle_item.setTransformOriginPoint(circle_item.boundingRect().center())

            # Default text: only the number
            text_item = self.scene.addText(str(no), font)
            text_item.setDefaultTextColor(color)
            text_item.setPos(x_px + 5, y_px + 5)
            text_item.setTransformOriginPoint(text_item.boundingRect().center())

            self.keypoint_items[no] = (circle_item, text_item)

        # Draw connection lines
        pen = QtGui.QPen(QtGui.QColor("black"), 2)
        for (start_no, end_no) in CONNECTIONS:
            if start_no in self.num_to_name and end_no in self.num_to_name:
                s_name = self.num_to_name[start_no]
                e_name = self.num_to_name[end_no]
                sx = self.PADDING + self.keypoints_dict[s_name]["x"] * self.SCALE
                sy = self.PADDING + self.keypoints_dict[s_name]["y"] * self.SCALE
                ex = self.PADDING + self.keypoints_dict[e_name]["x"] * self.SCALE
                ey = self.PADDING + self.keypoints_dict[e_name]["y"] * self.SCALE
                self.scene.addLine(sx, sy, ex, ey, pen)

        self.scene.setSceneRect(0, 0, total_width, total_height)

    def highlight_keypoint_by_number(self, no):
        # Unhighlight previous keypoint if any
        if self.current_highlight is not None and self.current_highlight in self.keypoint_items:
            old_circle, old_text = self.keypoint_items[self.current_highlight]
            old_circle.setScale(1.0)
            old_text.setScale(1.0)
            # Revert text back to the number
            old_text.setPlainText(str(self.current_highlight))
        # Highlight the new keypoint
        if no in self.keypoint_items:
            circle_item, text_item = self.keypoint_items[no]
            circle_item.setScale(2.0)
            text_item.setScale(2.0)
            # When highlighted, display the name instead of the number
            for name, info in self.keypoints_dict.items():
                if info["number"] == no:
                    text_item.setPlainText(name)
                    break
            self.current_highlight = no
        else:
            self.current_highlight = None

    def unhighlight_keypoint(self):
        if self.current_highlight is not None and self.current_highlight in self.keypoint_items:
            circle_item, text_item = self.keypoint_items[self.current_highlight]
            circle_item.setScale(1.0)
            text_item.setScale(1.0)
            text_item.setPlainText(str(self.current_highlight))
        self.current_highlight = None

from matplotlib.backends.qt_compat import QtWidgets
from typing import Callable


class CustomWidget(QtWidgets.QWidget):
    def __init__(self, widget: QtWidgets.QWidget, parent=None):
        super().__init__(parent)
        layout = QtWidgets.QVBoxLayout()
        layout.setSpacing(0)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(widget, stretch=1)
        self.setLayout(layout)

        def callback(idx: int = 0) -> None:
            return

        self.update_widget = callback

    def register_animation_callback(self, callback: Callable[[int], None]) -> None:
        """
        Registers a callback function for how to update the custom widget.

        Args:
            callback (Callable): A function specifying how to update the widget.
        """
        self.update_widget = callback

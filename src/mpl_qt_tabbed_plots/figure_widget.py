from matplotlib.backends.qt_compat import QtWidgets
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt import NavigationToolbar2QT as NavigationToolbar


class FigureWidget(QtWidgets.QWidget):
    """
    A Qt widget that contains a matplotlib figure canvas with an optional toolbar.
    """
    def __init__(self, blit: bool = False, include_toolbar: bool = True, parent = None):
        """
        Initializes the FigureWidget. This creates a matplotlib figure canvas
        and optionally includes a navigation toolbar.

        Args:
            blit (bool): If True, enables blitting for faster rendering.
                Default is False.
            include_toolbar (bool): If True, includes a navigation toolbar
                with the canvas. Default is True.
            parent: The parent widget for this widget. Default is None.
        """
        super().__init__(parent)
        self.blit = blit
        layout = QtWidgets.QVBoxLayout()
        self.canvas = FigureCanvas()
        self.figure = self.canvas.figure
        # self.figure.set_layout_engine('tight') # slows down rendering ~2x
        # self.figure.tight_layout() # does not seem to do anything here
        layout.addWidget(self.canvas)

        if include_toolbar:
            toolbar = NavigationToolbar(self.canvas, self)
            layout.addWidget(toolbar)

        self.setLayout(layout)

    def update_figure(self) -> None:
        if not self.figure.stale:
            return
        if self.blit:
            self.canvas.blit()
            # self.canvas.blit(self.figure.bbox)
        else:
            self.canvas.draw_idle()
        self.canvas.flush_events()

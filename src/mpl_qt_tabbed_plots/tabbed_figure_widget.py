from matplotlib.figure import Figure
from matplotlib.backends.qt_compat import QtWidgets

from .figure_widget import FigureWidget


class TabbedFigureWidget(QtWidgets.QTabWidget):
    """
    A Qt widget that can contains multiple tabs, each with a matplotlib Figure.
    This class inherits from QTabWidget in order to create a tabbed interface.
    """
    def __init__(self):
        """
        Initializes the TabbedFigureWidget.
        """
        super().__init__()
        self.figure_wigets: dict[str, FigureWidget] = {}

    def add_figure_tab(self, identifier: str|int, blit: bool = False,
                     include_toolbar: bool = True) -> Figure:
        """
        Adds a new tab to the widget with the given title/identifier, which
        creates and returns a matplotlib Figure. Tabs are displayed in the
        order they are added.

        Args:
            identifier (str|int): The title of the tab. If the identifier already
                exists, the existing Figure from that tab will be returned.
            blit (bool): If True, enables blitting for faster rendering on the
                Figure in this tab.
            include_toolbar (bool): If True, includes a navigation toolbar
                with the Figure in this tab. Default is True.
        """
        new_tab = FigureWidget(blit, include_toolbar)
        id_ = str(identifier)
        if id_ in self.figure_wigets:
            return self.figure_wigets[id_].figure
        self.figure_wigets[id_] = new_tab
        idx = self.currentIndex()
        super().addTab(new_tab, id_)
        return new_tab.figure

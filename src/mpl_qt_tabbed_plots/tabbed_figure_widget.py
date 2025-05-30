from matplotlib.figure import Figure
from matplotlib.backends.qt_compat import QtWidgets

from .figure_widget import FigureWidget


class TabbedFigureWidget(QtWidgets.QTabWidget):
    """
    A Qt widget that can contains multiple tabs, each with a matplotlib Figure.
    This class inherits from QTabWidget in order to create a tabbed interface.
    """
    def __init__(self, autohide: bool, position: str = 'top'):
        """
        Initializes the TabbedFigureWidget.

        Args:
            autohide (bool): If True, the tab bar will auto-hide when there is
                only one tab.
            position (str): The position of the tab bar. Can be 'top', 'bottom',
                'left', or 'right' as well as 'north', 'south', 'east', or
                'west' (only first character is checked).
        """
        super().__init__()
        self.set_tab_position(position)
        tabbar = self.tabBar()
        tabbar.setAutoHide(autohide)
        font = tabbar.font()
        font.setPointSize(8)
        tabbar.setFont(font)
        tabbar.setContentsMargins(0, 0, 0, 0)
        self.figure_wigets: dict[str, FigureWidget] = {}

    def add_figure_tab(self, tab_id: str|int, blit: bool = False,
                       include_toolbar: bool = True) -> Figure:
        """
        Adds a new tab to the widget with the given title/tab_id, which
        creates and returns a matplotlib Figure. Tabs are displayed in the
        order they are added.

        Args:
            tab_id (str|int): The title/ID of the tab. If the tab ID already
                exists, the existing Figure from that tab will be returned.
            blit (bool): If True, enables blitting for faster rendering on the
                Figure in this tab.
            include_toolbar (bool): If True, includes a navigation toolbar
                with the Figure in this tab.
        """
        new_tab = FigureWidget(blit, include_toolbar)
        id_ = str(tab_id)
        if id_ in self.figure_wigets:
            return self.figure_wigets[id_].figure
        self.figure_wigets[id_] = new_tab
        idx = self.currentIndex()
        super().addTab(new_tab, id_)
        self.setCurrentWidget(new_tab) # activate tab to auto size figure
        self.setCurrentIndex(idx) # switch back to original tab
        return new_tab.figure

    def set_tab_position(self, position: str = 'top') -> None:
        """
        Sets the position of the tab bar.

        Args:
            position (str): The position of the tab bar. Can be 'top', 'bottom',
                'left', or 'right' as well as 'north', 'south', 'east', or
                'west' (only first character is checked).
        """
        char = position[0].lower()
        if char in ['b', 's']:
            self.setTabPosition(QtWidgets.QTabWidget.South)
        elif char in ['l', 'w']:
            self.setTabPosition(QtWidgets.QTabWidget.West)
        elif char in ['r', 'e']:
            self.setTabPosition(QtWidgets.QTabWidget.East)
        else:
            self.setTabPosition(QtWidgets.QTabWidget.North)

# system imports
import signal
import sys
import time
if sys.version_info < (3, 11):
    from typing_extensions import Self
else:
    from typing import Self

from matplotlib.figure import Figure
from matplotlib.backends.qt_compat import QtWidgets, QtGui

# Fix plot font types to work in paper sumbissions (Don't use type 3 fonts)
import matplotlib
matplotlib.rcParams['pdf.fonttype'] = 42
matplotlib.rcParams['ps.fonttype'] = 42

from .figure_widget import FigureWidget
from .tabbed_figure_widget import TabbedFigureWidget

# if sys.modules.get('IPython') is not None:
try:
    from IPython.core.getipython import get_ipython
    from IPython.utils.capture import capture_output
    _in_ipython = get_ipython()
except ImportError:
    _in_ipython = None

if _in_ipython:
    with capture_output() as captured: # suppress output
        # register IPython event loop to Qt - prevents need to call app.exec()
        _in_ipython.run_line_magic('gui', 'qt')

    # SIGINT handles ctrl+c. The following lines allow it to kill without errors.
    # Using sys.exit(0) in IPython stops script execution, but not the kernel.
    signal.signal(signal.SIGINT, lambda sig, frame: sys.exit(0))
else:
    # Use SIG_DFL (default) rather than letting Qt handle ctrl+c.
    # Qt throws a KeyboardInterrupt exception, but only when the mouse hovers
    # over the window or some other Qt action causes events to process.
    signal.signal(signal.SIGINT, signal.SIG_DFL)


class TabbedPlotWindow(QtWidgets.QMainWindow):
    """
    A class to create a tabbed plot window where the tabs are matplotlib
    figures.
    """
    _app = QtWidgets.QApplication(sys.argv)
    _registry: dict[str, Self] = {}
    _latest_id = None
    _count = 0

    def __new__(cls, window_id: str|int|None = None,
                size: tuple[int,int] = (1280, 900),
                open_window: bool = False):
        if window_id is None:
            # Generate a unique identifier if none is provided
            id_ = str(len(cls._registry) + 1)
            while id_ in cls._registry:
                id_ = str(int(id_) + 1)
        else:
            id_ = str(window_id)

        # Return instance if it exists
        if id_ in cls._registry:
            return cls._registry[id_]

        # Create a new instance if it does not exist
        instance = super().__new__(cls)
        cls._registry[id_] = instance
        cls._latest_id = id_
        cls._count += 1
        return instance

    def __init__(self, window_id: str|int|None = None,
                 size: tuple[int,int] = (1280, 900),
                 open_window: bool = True):
        """
        Creates a new tabbed plot window with the given ID and size. If a window
        with the same ID already exists, it will return that instance instead of
        creating a new one.

        Args:
            window_id (str|int|None): The ID of the window. If None, a unique ID
                will be created based on the number of existing windows.
            size (tuple[int,int]): The size of the window in pixels.
            open_window (bool): If True, the window will be displayed
                immediately after creation. Otherwise, it will be hidden until
                another method is called to show it.
        """
        if hasattr(self, 'id'):
            return
        super().__init__()
        self.id = str(self._latest_id)
        self.setWindowTitle(f'Plot Window: {self.id}')
        self.resize(*size)
        self.tabs = TabbedFigureWidget()
        self.setCentralWidget(self.tabs)
        if open_window:
            self.show()

    def add_figure_tab(self, tab_id: str, blit: bool = False,
               include_toolbar: bool = True) -> Figure:
        """
        Adds a new tab to the window with the given ID and returns the Figure
        created for that tab. If a tab with the same ID already exists, the
        existing Figure will be returned instead of creating a new one.

        Args:
            tab_id (str): The ID of the tab.
            blit (bool): Whether blitting will be used with the Figure in this tab.
            include_toolbar (bool): Whether to include a matplotlib toolbar
                with the Figure in this tab.
        Returns:
            figure (Figure): The matplotlib figure in this tab.
        """
        figure = self.tabs.add_figure_tab(tab_id, blit, include_toolbar)
        return figure

    def update(self) -> None:
        """
        This will update the figure on the active (visible) tab. Similar to
        pyplot.pause(), but for the current tab on this window. No additional time
        delay is added to the function, so it will return immediately after
        updating the figure.
        """
        if not self.isVisible():
            self.show()
        active_tab = self.tabs.currentIndex()
        active_widget = self.tabs.widget(active_tab)
        if isinstance(active_widget, FigureWidget):
            active_widget.update_figure()

    def closeEvent(self, event: QtGui.QCloseEvent) -> None:
        """
        Qt event function - DO NOT CALL DIRECTLY.

        This method is called when the window is closed. It will remove the
        window from the list of windows and check if there are any other windows
        open. If not, it will exit the application.
        """
        event.accept()
        super().closeEvent(event)
        del TabbedPlotWindow._registry[self.id]
        TabbedPlotWindow._count -= 1
        if TabbedPlotWindow._count == 0:
            self._app.quit()

    def apply_tight_layout(self):
        """
        Applies a tight layout to the figure in each tab of the window, even if
        they are not the active Figure. Same as calling figure.tight_layout()
        directly on each Figure.
        """
        current_index = self.tabs.currentIndex()
        for i in range(self.tabs.count()):
            tab = self.tabs.widget(i)
            if not isinstance(tab, FigureWidget):
                continue
            self.tabs.setCurrentIndex(i) # tab has to be active to apply tight layout
            tab.update_figure()
            tab.figure.tight_layout()
            tab.canvas.draw_idle()
        self.tabs.setCurrentIndex(current_index)

    @staticmethod
    def show_all(tight_layout: bool = True, block: bool = True) -> None:
        """
        Shows all created windows. Each window will stay open until individually
        closed or else <ctrl+c> is pressed in the terminal that launched the
        application.

        Args:
            tight_layout (bool): If True, apply tight layout to all figures
                before showing them.
            block (bool): If True, the function will block until all windows
                are closed. If False, the function will return immediately after
                showing the windows.
        """
        for key in list(TabbedPlotWindow._registry.keys()):
            if not key in TabbedPlotWindow._registry:
                continue # in case window was closed during iteration
            window = TabbedPlotWindow._registry[key]
            if not window.isVisible():
                window.show()
            if tight_layout:
                window.apply_tight_layout()
        if not block:
            return
        if TabbedPlotWindow._count > 0 and TabbedPlotWindow._app is not None:
            try:
                TabbedPlotWindow._app.exec()
            except:
                TabbedPlotWindow._app.exec_() # for compatibility with Qt5

    @staticmethod
    def update_all(delay_seconds: float) -> float:
        """
        Updates all created windows. This is similar to pyplot.pause().

        Args:
            delay_seconds (float): The amount of time to wait before returning,
                accounting for the time taken to update the windows. If the plot
                update time is greater than this value, no extra delay will be
                added, but the function will take longer than this value to
                return.
        Returns:
            update_time (float): The amount of time (seconds) taken to update
                the windows. If less than delay_seconds, the function will wait
                for the remaining time before returning.
        """
        start = time.perf_counter()
        for key in list(TabbedPlotWindow._registry.keys()):
            if not key in TabbedPlotWindow._registry:
                continue # in case window was closed during iteration
            window = TabbedPlotWindow._registry[key]
            window.update()
        update_time = time.perf_counter() - start
        if TabbedPlotWindow._count > 0:
            remaining_delay = max(delay_seconds - update_time, 0.0)
            time.sleep(remaining_delay)
        return update_time

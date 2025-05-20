# system imports
import signal
import sys
import time

# Qt imports
from PySide6 import QtWidgets, QtGui

# matplotlib imports
import matplotlib
# Fix plot font types to work in paper sumbissions (Don't use type 3 fonts)
matplotlib.rcParams['pdf.fonttype'] = 42
matplotlib.rcParams['ps.fonttype'] = 42
# prevent NoneType error for versions of matplotlib 3.1.0rc1+ by calling matplotlib.use()
# For more on why it's nececessary, see
# https://stackoverflow.com/questions/59656632/using-qt5agg-backend-with-matplotlib-3-1-2-get-backend-changes-behavior
matplotlib.use('qtagg')
from matplotlib.figure import Figure
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt import NavigationToolbar2QT as NavigationToolbar
import matplotlib.pyplot as plt
plt.ioff()


class TabbedPlotWindow(QtWidgets.QMainWindow):
    """
    A class to create a tabbed plot window where the tabs are matplotlib
    figures. When using this class, DO NOT USE plt.show() or plt.pause() as they
    will cause issues with the plot window. Instead, use the methods provided
    by this class.
    """
    app = QtWidgets.QApplication(sys.argv)
    windows = []
    win_ids = []
    figures = {}
    count = 0

    def __init__(self, win_id: int|None = None, window_title: str = 'Plot Window',
                 size: tuple[int,int] = (1280, 900), open_window: bool = False):
        """
        Creates a new tabbed plot window with the given title and size. The
        window will be displayed immediately after creation.

        Args:
            window_title (str): The title of the window.
            size (tuple[int,int]): The size of the window in pixels. Default is
                (1280, 900).
            open_window (bool): If True, the window will be displayed
                immediately after creation. Otherwise, it will be hidden until
                another method is called to show it. Default is False.
        """
        if win_id in TabbedPlotWindow.win_ids:
            self = TabbedPlotWindow.windows[TabbedPlotWindow.win_ids.index(win_id)]
            return
        if win_id is None:
            win_id = max(TabbedPlotWindow.win_ids, default=0) + 1
        super().__init__()
        self.id = win_id
        self.setWindowTitle(window_title)
        self.resize(*size)
        self.canvases: list[FigureCanvas] = []
        self.figure_handles: list[Figure] = []
        self.toolbar_handles: list[NavigationToolbar] = []
        self.tab_handles: list[QtWidgets.QWidget] = []
        self.tabs = QtWidgets.QTabWidget()
        self.tabs.setTabBarAutoHide(True)
        self.tabs.setMovable(True)
        self.setCentralWidget(self.tabs)
        if open_window:
            self.show()
        TabbedPlotWindow.windows.append(self)
        TabbedPlotWindow.win_ids.append(self.id)
        TabbedPlotWindow.count += 1
        # self.figs: list[Figure] = []
        # Allow Ctrl+C to kill without errors
        signal.signal(signal.SIGINT, lambda sig,frame: sys.exit(0))

    def addTab(self, tab_title: str, figure: Figure) -> None:
    # def addTab(self, tab_title: str, figure: Figure|None) -> Figure:
        """
        Adds a new tab to the window with the given title and figure. The figure
        should be a matplotlib figure object. Window properties, such as size,
        will be determined by this class rather than the figure itself.

        Args:
            tab_title (str): The title of the tab.
            figure (Figure): The matplotlib figure to be displayed in the tab.
        """
        if figure.number in TabbedPlotWindow.figures.keys():
            return

        new_tab = QtWidgets.QWidget()
        layout = QtWidgets.QVBoxLayout()
        new_tab.setLayout(layout)

        # if figure is None:
        #     figure = Figure()
        self._resizeFigure(figure)
        new_canvas = FigureCanvas(figure)
        new_toolbar = NavigationToolbar(new_canvas, new_tab)
        layout.addWidget(new_canvas)
        layout.addWidget(new_toolbar)

        self.tabs.addTab(new_tab, tab_title)

        # self.toolbar_handles.append(new_toolbar)
        self.canvases.append(new_canvas)
        self.figure_handles.append(figure)
        TabbedPlotWindow.figures[figure.number] = figure
        # self.tab_handles.append(new_tab)

        if plt.isinteractive():
            print("Closing detected pyplot figure window because interactive mode is on.")
            plt.close(figure) # plt will open separate windows for each figure

        # return figure

    def _resizeFigure(self, figure: Figure) -> None:
        """
        Resizes the figure to fit the window size. This is called when the
        window is resized.

        Args:
            figure (Figure): The matplotlib figure to be resized.
        """
        width = self.width() / figure.dpi
        height = self.height() / figure.dpi
        figure.set_size_inches(width, height)
        layout_engine = figure.get_layout_engine()
        if layout_engine is None:
            layout_engine = 'tight'
        figure.set_layout_engine(layout_engine)

        # figure.canvas.draw()

    def update(self) -> None:
        """
        This will draw data updates for the figure on the active tab. Similar to
        plt.pause(), but for the current tab on this window. No additional time
        delay is added to the function, so it will return immediately after
        updating the figure.
        """
        if not self.isVisible():
            self.show()
        active_tab = self.tabs.currentIndex()
        canvas = self.canvases[active_tab]
        canvas.draw()
        canvas.flush_events()

    def closeEvent(self, event: QtGui.QCloseEvent) -> None:
        """
        This method is called when the window is closed. It will remove the
        window from the list of windows and check if there are any other windows
        open. If not, it will exit the application.
        """
        event.accept()
        super().closeEvent(event)
        for figure in self.figure_handles:
            num = figure.number
            TabbedPlotWindow.figures.pop(num)
        # idx = TabbedPlotWindow.windows.index(self)
        TabbedPlotWindow.windows.remove(self)
        TabbedPlotWindow.win_ids.remove(self.id)
        # TabbedPlotWindow.windows.pop(self.id)
        TabbedPlotWindow.count -= 1
        if TabbedPlotWindow.count == 0:
            self.app.quit()

    def applyTightLayout(self):
        """
        Applies a tight layout to the figure in each tab of the window.
        """
        current_index = self.tabs.currentIndex()
        for i,fig in enumerate(self.figure_handles):
            self.tabs.setCurrentIndex(i) # tab has to be active to apply tight layout
            fig.tight_layout()
            canvas = self.canvases[i]
            canvas.draw()
        self.tabs.setCurrentIndex(current_index)

    @staticmethod
    def show_all(tight_layout: bool = True, block: bool = True) -> None:
        """
        Shows all open windows. Each window will stay open until individually
        closed or else <ctrl+c> is pressed in the terminal that launched the
        application. This is a replacement for plt.show()...plt.show() should
        not be used with this class as it will cause issues.

        Args:
            tight_layout (bool): If True, apply tight layout to all figures
                before showing them.
            block (bool): If True, the function will block until all windows
                are closed. If False, the function will return immediately after
                showing the windows.
        """
        for window in TabbedPlotWindow.windows:
            win: TabbedPlotWindow = window # satisfy LSP
            if not win.isVisible():
                win.show()
            if tight_layout:
                win.applyTightLayout()
        if not block:
            return
        if TabbedPlotWindow.count > 0 and TabbedPlotWindow.app is not None:
            TabbedPlotWindow.app.exec()

    @staticmethod
    def update_all(delay_seconds: float) -> float:
        """
        Updates all open windows. This is a replacement for plt.pause() and
        should be used when the plot data is changing over time. If not, use
        show_all() instead.

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
        start = time.time()
        for window in TabbedPlotWindow.windows:
            win: TabbedPlotWindow = window # satisfy LSP
            win.update()
        update_time = time.time() - start
        if TabbedPlotWindow.count > 0:
            remaining_delay = max(delay_seconds - update_time, 0.0)
            time.sleep(remaining_delay)

        # open_windows = [w for w in QApplication.topLevelWidgets() if w.isVisible()]
        # if len(open_windows) == 0:
        #     print("No open windows. Exiting...")
        #     sys.exit(0)
        return update_time

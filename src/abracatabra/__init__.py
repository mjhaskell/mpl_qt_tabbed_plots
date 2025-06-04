"""
abracatabra
===========
A library for creating tabbed plot windows with matplotlib in a Qt environment.

Windows can be created with one or more tab groups. Each tab group can contain
one or more tabs, where is tab is a matplotlib Figure. The library provides
functions to show all open windows, update them, and a fun `abracatabra` function
to display all windows with a magical touch.

This package provides:
- `TabbedPlotWindow`: The main class for creating and managing tabbed plot windows.
- `show_all_windows`: Displays all open tabbed plot windows.
- `update_all_windows`: Updates all open tabbed plot windows.
- `abracatabra`: A fun function to display all open tabbed plot windows.
- `is_interactive`: Checks if the current environment is interactive (e.g., IPython or Jupyter).
- `__version__`: The version of the abracatabra package.
"""

from .tabbed_plot_window import TabbedPlotWindow, _in_ipython
from .__about__ import __version__


def show_all_windows(tight_layout: bool = False, block: bool = True) -> None:
    """
    Displays all open tabbed plot windows if they are not already open.

    Args:
        tight_layout (bool): If True, applies a tight layout to all figures.
        block (bool): If True, blocks the execution until all windows are closed.
    """
    TabbedPlotWindow.show_all(tight_layout, block)

def update_all_windows(delay: float = 0.0) -> float:
    """
    Updates all open tabbed plot windows. This is similar to pyplot.pause()
    and should be used when the plot data is changing over time. If not, use
    show_all_windows() instead.

    Args:
        delay (float): The delay in seconds before the next update.

    Returns:
        update_time (float): How long it took to update all matplotlib Figures,
            not including the delay.
    """
    return TabbedPlotWindow.update_all(delay)

def abracatabra(tight_layout: bool = False, block: bool = True,
                verbose: bool = True) -> None:
    """
    A more fun equivalent to `show_all_windows()`. Displays all open tabbed plot
    windows if they are not already open.

    Args:
        tight_layout (bool): If True, applies a tight layout to all figures.
        block (bool): If True, blocks the execution until all windows are closed.
        verbose (bool): If True, prints a message when showing windows.
    """
    if verbose:
        print("Abracatabra! 🪄✨")
    for window in TabbedPlotWindow._registry.values():
        window.setWindowIcon(window._icon2)
    TabbedPlotWindow.show_all(tight_layout, block)

def is_interactive() -> bool:
    """
    Returns True if the current environment is interactive (e.g., IPython or Jupyter).
    """
    return bool(_in_ipython)


__all__ = [
    'TabbedPlotWindow',
    'show_all_windows',
    'update_all_windows',
    'abracatabra',
    'is_interactive',
    '__version__',
]

from .tabbed_plot_window import TabbedPlotWindow

def show_all_windows(tight_layout: bool = False, block: bool = True) -> None:
    """
    Displays all open tabbed plot windows if they are not already open. Replaces
    plt.show().

    Args:
        tight_layout (bool): If True, applies a tight layout to all figures.
            Default is False.
        block (bool): If True, blocks the execution until all windows are closed.
            Default is True.
    """
    TabbedPlotWindow.show_all(tight_layout, block)

def update_all_windows(delay: float = 0.0) -> float:
    """
    Updates all open tabbed plot windows. This is a replacement for plt.pause()
    and should be used when the plot data is changing over time. If not, use
    TabbedPlotWindow.show_all() instead.

    Args:
        delay (float): The delay in seconds before the next update. Default is 0.0.

    Returns:
        update_time (float): How long it took to update all matplotlib Figures,
            not including the delay.
    """
    return TabbedPlotWindow.update_all(delay)

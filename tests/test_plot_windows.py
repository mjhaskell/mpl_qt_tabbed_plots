import numpy as np
import matplotlib.pyplot as plt
from mpl_qt_tabbed_plots import TabbedPlotWindow


def test_tabbed_plot_window():
    window1 = TabbedPlotWindow('test')
    window2 = TabbedPlotWindow(size=(500,400))

    # data
    t = np.arange(0, 10, 0.001)
    ysin = np.sin(t)
    ycos = np.cos(t)


    f = window1.add_figure_tab("sin")
    ax = f.add_subplot()
    line1, = ax.plot(t, ysin, '--')
    ax.set_xlabel('time')
    ax.set_ylabel('sin(t)')
    ax.set_title('Plot of sin(t)')


    f = window1.add_figure_tab("time")
    ax = f.add_subplot()
    ax.plot(t, t)
    ax.set_xlabel('time')
    ax.set_ylabel('t')
    ax.set_title('Plot of t')

    f = window2.add_figure_tab("cos")
    ax = f.add_subplot()
    line2, = ax.plot(t, ycos, '--')
    ax.set_xlabel('time')
    ax.set_ylabel('cos(t)')
    ax.set_title('Plot of cos(t)')

    f = window2.add_figure_tab("time")
    ax = f.add_subplot()
    ax.plot(t, t)
    ax.set_xlabel('time')
    ax.set_ylabel('t')
    ax.set_title('Plot of t', fontsize=20)

    # animate
    dt = 0.1
    for k in range(100):
        t += dt
        ysin = np.sin(t)
        line1.set_ydata(ysin)
        ycos = np.cos(t)
        line2.set_ydata(ycos)
        # window1.update()
        TabbedPlotWindow.update_all(0.01)

    TabbedPlotWindow.show_all(block=False)


if __name__ == "__main__":
    test_tabbed_plot_window()

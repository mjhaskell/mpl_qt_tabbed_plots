import numpy as np
import matplotlib.pyplot as plt
from mpl_qt_tabbed_plots import TabbedPlotWindow


def test_tabbed_plot_window():
    window1 = TabbedPlotWindow(1,window_title='Plot Window 1', open_window=True)
    window2 = TabbedPlotWindow(2,size=(500,400), open_window=True)

    # data
    t = np.arange(0, 10, 0.001)
    ysin = np.sin(t)
    ycos = np.cos(t)


    f = plt.figure(1, layout='tight')
    ax = f.add_subplot()
    line1, = ax.plot(t, ysin, '--')
    ax.set_xlabel('time')
    ax.set_ylabel('sin(t)')
    ax.set_title('Plot of sin(t)')
    window1.addTab("sin", f)

    f = plt.figure(2)
    ax = f.add_subplot()
    ax.plot(t, t)
    ax.set_xlabel('time')
    ax.set_ylabel('t')
    ax.set_title('Plot of t')
    window1.addTab("time", f)

    f = plt.figure(3)
    ax = f.add_subplot()
    line2, = ax.plot(t, ycos, '--')
    ax.set_xlabel('time')
    ax.set_ylabel('cos(t)')
    ax.set_title('Plot of cos(t)')
    window2.addTab("cos", f)

    f = plt.figure(5)
    ax = f.add_subplot()
    ax.plot(t, t)
    ax.set_xlabel('time')
    ax.set_ylabel('t')
    ax.set_title('Plot of t', fontsize=20)
    window2.addTab("time", f)

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

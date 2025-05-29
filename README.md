# MPL Qt Tabbed Plots

This repository is basically a matplotlib extension using the Qt backend to create plot windows with groups of tabs, where the contents of each tab is a matplotlib figure.
This package is essentially a replacement for pyplot; it creates and manages figures separately from pyplot, so calling `plt.show()` or `plt.pause()` will not do anything with windows created from this package.
This package provides the functions `show_all_windows()` and `update_all_windows(delay)`, which are very similar in behavior to `show()` and `pause(interval)`, respectively, from pyplot.

## Dependencies

- matplotlib
- One of the following Qt bindings for Python (this is the order matplotlib looks for them):
    - PyQt6
    - PySide6 (preferred option)
    - PyQt5
    - PySide2

## Installation

This will install the package as well as matplotlib, if it isn't installed:

```
pip install mpt_qt_tabbed_plots
```

Qt bindings are an optional dependency of the package.
A PyQt package is required for functionality, but there is no good way to have a default optional dependency with pip...so you have to install separately or manually specify one of the following optional dependencies:

- [qt-pyside6]
- [qt-pyqt6]
- [qt-pyqt5]
- [qt-pyside2]

For example, run this to install PySide6 along with this package:
```
pip install "mpt_qt_tabbed_plots[qt-pyside6]"
```

## Usage

```python
import numpy as np
import mpl_qt_tabbed_plots as tabby


window1 = tabby.TabbedPlotWindow(window_id='test', ncols=2)
window2 = tabby.TabbedPlotWindow(size=(500,400))

# data
t = np.arange(0, 10, 0.001)
ysin = np.sin(t)
ycos = np.cos(t)


f = window1.add_figure_tab("sin", col=0)
ax = f.add_subplot()
line1, = ax.plot(t, ysin, '--')
ax.set_xlabel('time')
ax.set_ylabel('sin(t)')
ax.set_title('Plot of sin(t)')

f = window1.add_figure_tab("time", col=1)
ax = f.add_subplot()
ax.plot(t, t)
ax.set_xlabel('time')
ax.set_ylabel('t')
ax.set_title('Plot of t')

window1.apply_tight_layout()

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

window2.apply_tight_layout()

# animate
dt = 0.1
for k in range(100):
    t += dt
    ysin = np.sin(t)
    line1.set_ydata(ysin)
    ycos = np.cos(t)
    line2.set_ydata(ycos)
    tabby.update_all_windows(0.01)

tabby.show_all_windows(block=True)
```

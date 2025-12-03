from typing import Callable, Optional
from matplotlib.backends.qt_compat import QtCore, QtWidgets

# from PySide6 import QtWidgets, QtCore


class AnimationPlayer(QtWidgets.QMainWindow):
    def __init__(
        self, frames: int, update_callback: Optional[Callable[[int], None]] = None
    ):
        super().__init__()

        self.paused = True
        self.current_frame = 0
        self.update_callback = update_callback or (lambda i: None)

        self.setWindowTitle("Animation Player")
        self.resize(400, 100)
        central_widget = QtWidgets.QWidget()
        self.setCentralWidget(central_widget)
        layout = QtWidgets.QVBoxLayout(central_widget)

        # add buttons
        # self.play_button = QtWidgets.QPushButton(" Play")
        self.play_button = QtWidgets.QPushButton()
        icon = self.style().standardIcon(QtWidgets.QStyle.StandardPixmap.SP_MediaPlay)
        self.play_button.setIcon(icon)
        self.play_button.clicked.connect(self._on_play_clicked)

        self.restart_button = QtWidgets.QPushButton(" Restart")
        icon = self.style().standardIcon(
            QtWidgets.QStyle.StandardPixmap.SP_MediaSkipBackward
        )
        self.restart_button.setIcon(icon)
        self.restart_button.clicked.connect(self._on_restart_clicked)

        self.end_button = QtWidgets.QPushButton(" End")
        icon = self.style().standardIcon(
            QtWidgets.QStyle.StandardPixmap.SP_MediaSkipForward
        )
        self.end_button.setIcon(icon)
        self.end_button.clicked.connect(self._on_end_clicked)

        # self.prev_button = QtWidgets.QPushButton("Previous Frame")
        self.prev_button = QtWidgets.QPushButton()
        icon = self.style().standardIcon(
            QtWidgets.QStyle.StandardPixmap.SP_ArrowBack
            # QtWidgets.QStyle.StandardPixmap.SP_MediaSeekBackward
        )
        self.prev_button.setIcon(icon)
        self.prev_button.clicked.connect(self._on_prev_clicked)

        # self.next_button = QtWidgets.QPushButton("Next Frame")
        self.next_button = QtWidgets.QPushButton()
        icon = self.style().standardIcon(
            QtWidgets.QStyle.StandardPixmap.SP_ArrowForward
            # QtWidgets.QStyle.StandardPixmap.SP_MediaSeekForward
        )
        self.next_button.setIcon(icon)
        self.next_button.clicked.connect(self._on_next_clicked)

        button_row = QtWidgets.QHBoxLayout()
        button_row.addWidget(self.play_button)
        button_row.addWidget(self.restart_button)
        button_row.addWidget(self.end_button)
        layout.addLayout(button_row)

        # add slider
        slider_row = QtWidgets.QHBoxLayout()
        self.slider = QtWidgets.QSlider(QtCore.Qt.Orientation.Horizontal)
        self.slider.setMinimum(0)
        self.slider.setMaximum(frames - 1)
        self.slider.setValue(0)
        self.slider.valueChanged.connect(self._on_slider_changed)
        slider_row.addWidget(self.prev_button)
        slider_row.addWidget(self.slider)
        slider_row.addWidget(self.next_button)
        layout.addLayout(slider_row)
        # layout.addWidget(self.slider)

        # add label
        self.label = QtWidgets.QLabel()
        self._set_label()
        layout.addWidget(self.label)

        self.show()
        self.raise_()

    def set_frame(self, frame: int):
        self.current_frame = min(frame, self.slider.maximum())
        # self.slider.blockSignals(True)
        self.slider.setValue(self.current_frame)
        # self.slider.blockSignals(False)
        # self._set_label()
        # self.update_callback(self.current_frame)

    def _on_play_clicked(self):
        if self.paused:
            self.paused = False
            # self.play_button.setText("Pause")
            icon = self.style().standardIcon(
                QtWidgets.QStyle.StandardPixmap.SP_MediaPause
            )
            self.play_button.setIcon(icon)
            self.prev_button.setEnabled(False)
            self.next_button.setEnabled(False)
        else:
            self.paused = True
            # self.play_button.setText("Play")
            icon = self.style().standardIcon(
                QtWidgets.QStyle.StandardPixmap.SP_MediaPlay
            )
            self.play_button.setIcon(icon)
            self.prev_button.setEnabled(True)
            self.next_button.setEnabled(True)

    def _on_restart_clicked(self):
        self.current_frame = 0
        self.slider.setValue(self.current_frame)
        self.update_callback(self.current_frame)

    def _on_end_clicked(self):
        self.current_frame = self.slider.maximum()
        self.slider.setValue(self.current_frame)
        self.update_callback(self.current_frame)

    def _on_prev_clicked(self):
        if not self.paused:
            return
        if self.current_frame > 0:
            self.current_frame -= 1
            self.slider.setValue(self.current_frame)

    def _on_next_clicked(self):
        if not self.paused:
            return
        if self.current_frame < self.slider.maximum() - 1:
            self.current_frame += 1
            self.slider.setValue(self.current_frame)
            self.update_callback(self.current_frame)

    def _on_slider_changed(self, value: int):
        self.current_frame = value
        self._set_label()
        self.update_callback(self.current_frame)

    def _set_label(self):
        max = self.slider.maximum()
        cur = self.current_frame
        digits = len(str(max))
        self.label.setText(f"Frame: {cur:>{digits}}/{max}")

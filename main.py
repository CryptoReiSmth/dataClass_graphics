import sys
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import QCheckBox, QDialog, QVBoxLayout, QHBoxLayout, QMainWindow
import pyqtgraph as pg
from dataclasses import dataclass


@dataclass
class KZPowerREG:
    UC: float = 0
    UC_raw : int = 0
    I1: float = 0
    I1_raw : int = 0
    UL: float = 0
    UL_raw : int = 0
    IL: float = 0
    IL_raw : int = 0
    _27V: float = 0
    _27V_raw : int = 0
    U1: float = 0
    U1_raw : int = 0


@dataclass
class KZTelemetryREG:
    IR: KZPowerREG
    UV: KZPowerREG
    uptime: int = 0
    temperature: float = 0


class MainWindow(QDialog):
    def __init__(self, data_class_dict: dict):
        super(QDialog, self).__init__()

        # Create cool window
        self.graphWidget = pg.PlotWidget()
        self.graphWidget.setBackground('w')
        self.graphWidget.setTitle("Position", color="b", size="25pt")
        styles = {"color": "#f00", "font-size": "20px"}
        self.graphWidget.setLabel("left", "y", **styles)
        self.graphWidget.setLabel("bottom", "x", **styles)
        self.graphWidget.addLegend()
        self.graphWidget.showGrid(x=True, y=True)
        self.setWindowTitle("dataClass_graphics")


        # Структура, данные которой отображаются на графике
        self.data_line = []

        # Массив чек боксов
        self.choice_button = []
        self.dictionary = data_class_dict
        # Заполняет массив кнопок
        for key in self.dictionary.keys():
            if type(self.dictionary.get(key)) == type(0):
                self.choice_button.append(QCheckBox(key))
            else:
                key_values = self.dictionary.get(key).__dict__
                for key_item in key_values:
                    self.choice_button.append(QCheckBox(f"{key}: {key_item}"))

        # Add elements to layout
        layout_v = QVBoxLayout()
        for button in self.choice_button:
            layout_v.addWidget(button)

        self.setLayout(layout_v)


if __name__ == '__main__':
    test = KZTelemetryREG(KZPowerREG(), KZPowerREG())
    app = QtWidgets.QApplication(sys.argv)
    d = test.__dict__

    w = MainWindow(test.__dict__)
    w.show()
    sys.exit(app.exec_())



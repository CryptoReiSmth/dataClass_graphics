import sys
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import QCheckBox, QDialog, QVBoxLayout, QHBoxLayout, QMainWindow
from PyQt5.QtGui import QColor
import pyqtgraph as pg
from dataclasses import dataclass
from random import randint

# TODO: Заполнить списком цветов
colors = ["r"] * 100
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
        self.pen = []

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

        num_of_lines = 0
        layout_h = QHBoxLayout()
        layout_v = QVBoxLayout()
        # Добавляем кнопки на экран
        # и хорошо считаем количество выводимых параметров (aka линий aka кнопок)
        for button in self.choice_button:
            layout_v.addWidget(button)
            num_of_lines += 1

        # Делаем разные (нет) цвета линий и маркеров
        for i in range(num_of_lines):
            line_color = colors[i]
            self.pen.append(pg.mkPen(color = line_color))
            self.data_line.append(self.graphWidget.plot([i], [i+2], pen = self.pen[i], symbol='+', symbolSize=10, symbolBrush=line_color))

        layout_h.addWidget(self.graphWidget)
        layout_h.addLayout(layout_v)
        self.setLayout(layout_h)


if __name__ == '__main__':
    test = KZTelemetryREG(KZPowerREG(), KZPowerREG())
    app = QtWidgets.QApplication(sys.argv)
    dataClass_dict = test.__dict__
    test.temperature = 1111111111

    """print(dataClass_dict)
    count = 0
    for key in dataClass_dict.keys():
        if isinstance(dataClass_dict.get(key), int):
            print(f"key = {key}, value = {dataClass_dict.get(key)}")
            count += 1
        else:
            dataclass_key_dict = dataClass_dict.get(key).__dict__
            print(f"\n\n\ndataclass_key_dict  = {dataclass_key_dict}\n")
            for k in dataclass_key_dict.keys():
                print(f"dataclass: {dataClass_dict.get(key)}, key: {key}_{k}, value: {dataclass_key_dict.get(k)}")
                count += 1
    print(f"count = {count}")"""
    w = MainWindow(dataClass_dict)
    w.show()
    sys.exit(app.exec_())

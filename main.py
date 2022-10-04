import sys
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import QCheckBox, QDialog, QVBoxLayout, QHBoxLayout, QMainWindow
import pyqtgraph as pg
from dataclasses import dataclass
from random import randint

# TODO: Заполнить списком цветов
colors = ["aqua", "orange", "hotpink", "lightslategray", "yellow", "springgreen", "blueviolet", "orangered", "royalblue", "green", "plum", "paleturquoise", "palegreen", "navy", "turquoise", "mediumvioletred", "darkgoldenrod", "fuchsia", "steelblue", "lightcoral", "thistle", "khaki", "chartreuse", "teal", "saddlebrown", "violet", "lemonchiffon", "blue", "olive", "red"]
@dataclass
class KZPowerREG:
    UC: float = 0
    UC_raw: int = 0
    I1: float = 0
    I1_raw: int = 0
    UL: float = 0
    UL_raw: int = 0
    IL: float = 0
    IL_raw: int = 0
    _27V: float = 0
    _27V_raw: int = 0
    U1: float = 0
    U1_raw: int = 0


@dataclass
class KZTelemetryREG:
    IR: KZPowerREG = KZPowerREG()
    UV: KZPowerREG = KZPowerREG()
    uptime: int = 0
    temperature: float = 0


class MainWindow(QDialog):
    def __init__(self, data_class_name: str):
        data_class_dict = None
        if data_class_name in globals():
            data_class_dict = eval(data_class_name + "().__dict__")
        else:
            sys.exit(1)
        super(QDialog, self).__init__()
        self.setGeometry(150, 50, 1600, 950)
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


        # Данные для графика
        # Массив с массивом значений (длина y = num_of_lines)
        #                            (длина каждого y[i] = число значений)
        self.y = []         # - двумерный
        self.x = []         # - одномерный
        # Отображаемые значения
        self.shown_x = []    # - двумерный
        self.shown_y = []    # - двумерный

        # Структура, данные которой отображаются на графике
        self.data_lines = []
        self.pen = []

        # Массив чек боксов
        self.choice_buttons = []
        self.dictionary = data_class_dict

        # Заполняет массив кнопок
        for key in self.dictionary.keys():
            if isinstance(self.dictionary.get(key), (int, float)):
                self.choice_buttons.append(QCheckBox(key))
            else:
                key_values = self.dictionary.get(key).__dict__
                for key_item in key_values:
                    self.choice_buttons.append(QCheckBox(f"{key}: {key_item}"))

        self.num_of_lines = 0
        layout_h = QHBoxLayout()
        layout_v = QVBoxLayout()
        # Добавляем кнопки на экран
        # и хорошо считаем количество выводимых параметров (aka линий aka кнопок)
        for button in self.choice_buttons:
            button.setChecked(False)
            layout_v.addWidget(button)
            self.num_of_lines += 1

        # Делаем разные цвета линий и маркеров
        for i in range(self.num_of_lines):
            line_color = colors[i]
            self.pen.append(pg.mkPen(color = line_color))
            self.data_lines.append(self.graphWidget.plot([i], [i+2], pen = self.pen[i], symbol='+', symbolSize=10, symbolBrush=line_color))

        layout_h.addWidget(self.graphWidget)
        layout_h.addLayout(layout_v)
        self.setLayout(layout_h)

        # TODO: записать данные из data-Class
        self.y = [] # - двумерный
        self.x = [i for i in range(50)]  # - одномерный
        for i in range(self.num_of_lines):
            self.y.append(self.x)
            self.shown_x.append(self.x)
        self.shown_y = self.y.copy()

        # Set update settings
        self.timer = QtCore.QTimer()
        self.timer.setInterval(100)
        self.timer.timeout.connect(self.update_plot_data)
        self.timer.start()

    # Удаляет самые левые точки из графика
    def delete_point(self):
        self.x = self.x[1:]
        for i in range(len(self.y)):
            self.y[i] = self.y[i][1:]

    # Добавляет точки со значениями new_values в каждую линию
    def add_point(self, new_values: list):
        if len(new_values) != self.num_of_lines:
            sys.exit(2)
        self.x.append(self.x[-1] + 1)
        for i in range(len(new_values)):
            self.y[i].append(new_values[i])

    # Обновляет данные для графика
    def update_plot_data(self):
        self.delete_point()
        self.add_point([randint(0, 20) for _ in range(self.num_of_lines)])  # TODO: добавлять значения из data-Class
        for i in range(len(self.choice_buttons)):
            button = self.choice_buttons[i]
            if button.isChecked():
                self.shown_x[i] = self.x.copy()
                self.shown_y[i] = self.y[i].copy()
            else:
                self.shown_x[i] = []
                self.shown_y[i] = []

        for i in range(len(self.data_lines)):
            self.data_lines[i].setData(self.shown_x[i], self.shown_y[i])


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)

    count = 0
    """for key in dataClass_dict.keys():
        if isinstance(dataClass_dict.get(key), int) or isinstance(dataClass_dict.get(key), float):
            print(f"key = {key}, value = {dataClass_dict.get(key)}")
            count += 1
        else:
            dataclass_key_dict = dataClass_dict.get(key).__dict__
            print(f"\n\n\ndataclass_key_dict  = {dataclass_key_dict}\n")
            for k in dataclass_key_dict.keys():
                print(f"key: {key}_{k}, value: {dataclass_key_dict.get(k)}")
                count += 1
    print(f"count = {count}")"""

    class_name = "KZTelemetryREG"
    w = MainWindow(class_name)
    w.show()
    sys.exit(app.exec_())

import sys
import time
from typing import Union
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import QCheckBox, QDialog, QVBoxLayout, QHBoxLayout
import pyqtgraph as pg
from dataclasses import dataclass
from random import randint

COLORS = ["aqua", "orange", "hotpink", "lightslategray", "yellow", "springgreen", "blueviolet", "orangered",
          "royalblue", "green", "plum", "paleturquoise", "palegreen", "navy", "turquoise", "mediumvioletred",
          "darkgoldenrod", "fuchsia", "steelblue", "lightcoral", "thistle", "khaki", "chartreuse", "teal",
          "saddlebrown", "violet", "lemonchiffon", "blue", "olive", "red"]
COLORS_RGB = ["rgb( 0, 255, 255)", "rgb(255, 165, 0)", "rgb(255, 105, 180)", "rgb(119, 136, 153)", "rgb(255, 255, 0)",
              "rgb( 0, 255, 127)", "rgb(138, 43, 226)", "rgb(255, 69, 0)", "rgb( 65, 105, 225)", "rgb( 0, 128, 0)",
              "rgb(221, 160, 221)", "rgb(175, 238, 238)", "rgb(152, 251, 152)", "rgb( 0, 0, 128)", "rgb( 64, 224, 208)",
              "rgb(199, 21, 133)", "rgb(184, 134, 11)", "rgb(255, 0, 255)", "rgb( 70, 130, 180)", "rgb(240, 128, 128)",
              "rgb(216, 191, 216)", "rgb(240, 230, 140)", "rgb(127, 255, 0)", "rgb( 0, 128, 128)", "rgb(139, 69, 19)",
              "rgb(238, 130, 238)", "rgb(255, 250, 205)", "rgb( 0, 0, 255)", "rgb(128, 128, 0)", "rgb(255, 0, 0)"]


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


def dict_into_list(data_class_object_dict: dict):
    new_values_list = []
    for key in data_class_object_dict.keys():
        if isinstance(data_class_object_dict.get(key), (int, float)):
            new_values_list.append(data_class_object_dict.get(key))
        else:
            dataclass_key_dict = data_class_object_dict.get(key).__dict__
            for k in dataclass_key_dict.keys():
                new_values_list.append(dataclass_key_dict.get(k))
    return new_values_list


class MainWindow(QDialog):
    def __init__(self, data_class_name: str, num_of_point_to_show: int = 50):
        if data_class_name in globals():
            self.dictionary = eval(data_class_name + "().__dict__")
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

        # Структура, данные которой отображаются на графике
        self.data_lines = []
        self.pen = []

        # Заполняет массив кнопок
        self.choice_buttons = []
        color_iterator = 0
        for key in self.dictionary.keys():
            if isinstance(self.dictionary.get(key), (int, float)):
                current_button = QCheckBox(f"{key}")
                current_style = "QCheckBox::indicator:checked {background-color: " +  COLORS_RGB[color_iterator] + ";}"
                current_button.setStyleSheet(current_style)
                self.choice_buttons.append(current_button)
                color_iterator += 1
            else:
                key_values = self.dictionary.get(key).__dict__
                for key_item in key_values:
                    current_button = QCheckBox(f"{key}: {key_item}")
                    current_style = "QCheckBox::indicator:checked {background-color: " + COLORS_RGB[color_iterator] + ";}"
                    current_button.setStyleSheet(current_style)
                    self.choice_buttons.append(current_button)
                    color_iterator += 1

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
            line_color = COLORS[i]
            self.pen.append(pg.mkPen(color = line_color))
            self.data_lines.append(self.graphWidget.plot([i], [i+2], pen = self.pen[i], symbol='+', symbolSize=10, symbolBrush=line_color))

        layout_h.addWidget(self.graphWidget)
        layout_h.addLayout(layout_v)
        self.setLayout(layout_h)

        # Данные для графика
        # Массив с массивом значений (длина y = num_of_lines)
        #                            (длина каждого y[i] = число значений)
        self.y = []  # - двумерный
        self.x = [0]  # - одномерный
        # Значения последних точек линий
        self.last_y = []  # - одномерный
        # Отображаемые значения
        self.shown_x = []  # - двумерный
        self.shown_y = []  # - двумерный
        self.num_of_point_to_show = num_of_point_to_show
        # Записываем данные для первых точек каждой линии из data-Class
        data_class_value_list = dict_into_list(self.dictionary)
        for i in range(len(data_class_value_list)):
            self.y.append([data_class_value_list[i]])


        # Заполняем данные для отображения
        for i in range(self.num_of_lines):
            self.shown_x.append(self.x)
        self.shown_y = self.y.copy()

        # Выставляем настройки для обновления графика
        self.timer = QtCore.QTimer()
        self.timer.setInterval(100)
        self.timer.timeout.connect(self.update_plot_data)
        self.timer.start()


    # Удаляет самые левые точки каждой линии из графика
    def delete_point(self):
        self.x = self.x[1:]
        for i in range(len(self.y)):
            self.y[i] = self.y[i][1:]

    # Добавляет точки со значениями new_values в каждую линию
    def add_point(self, data_class_values: Union[dict, list] = None):
        current_time = time.time() - self.start_time
        self.x.append(int(current_time))
        if isinstance(data_class_values, list):
            new_values = data_class_values.copy()
        else:
            new_values = dict_into_list(data_class_values)

        if data_class_values is None:
            self.add_point(self.last_y)
        else:
            self.last_y = []
            for i in range(len(new_values)):
                self.last_y.append(self.y[i][-1])
                self.y[i].append(new_values[i])

    # Обновляет данные для графика
    def update_plot_data(self):
        if len(self.x) == self.num_of_point_to_show:
            self.delete_point()
        self.add_point(KZTelemetryREG().__dict__)   # TODO: добавлять значения из data-Class
                                                    # (вместо KZTelemetryREG() нужно подставить новый объект dataClass)
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
    class_name = "KZTelemetryREG"
    w = MainWindow(class_name)
    w.show()
    sys.exit(app.exec_())

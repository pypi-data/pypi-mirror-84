from PyQt5 import QtWidgets, QtCore
import numpy as np
import warnings
import matplotlib.cbook
warnings.filterwarnings("ignore", category=matplotlib.cbook.mplDeprecation)

from nndesigndemos.nndesign_layout import NNDLayout
from nndesigndemos.get_package_path import PACKAGE_PATH


class PoslinNetworkFunction(NNDLayout):
    def __init__(self, w_ratio, h_ratio, dpi):
        super(PoslinNetworkFunction, self).__init__(w_ratio, h_ratio, dpi, main_menu=2)

        self.fill_chapter("Poslin Network Function", 2, "\nAlter the network's\nparameters by dragging\nthe slide bars.\n\n"
                                                        "Choose the output transfer\nfunction f below.\n\n"
                                                        "Click on [Random] to\nset each parameter\nto a random value.",
                          PACKAGE_PATH + "Chapters/2_D/Logo_Ch_2.svg",
                          PACKAGE_PATH + "Figures/PoslinNetSimple.svg", icon_move_left=120, icon_coords=(130, 160, 500, 200))

        self.make_plot(1, (10, 415, 500, 270))

        self.comboBox1_functions = [self.poslin, self.purelin, self.hardlim, self.hardlims, self.satlin, self.satlins, self.logsig, self.tansig]
        self.comboBox1_functions_str = ["poslin", "purelin", "hardlim", "hardlims", "satlin", "satlins", "logsig", 'tansig']
        self.make_combobox(1, self.comboBox1_functions_str, (self.x_chapter_button - 8, 330, self.w_chapter_button + 16, 50), self.change_transfer_function, "label_f", "f")
        self.func1 = self.poslin
        self.idx = 0

        self.make_button("random_button", "Random", (self.x_chapter_button, 380, self.w_chapter_button, self.h_chapter_button), self.on_random)

        self.make_slider("slider_w1_1", QtCore.Qt.Horizontal, (-100, 100), QtWidgets.QSlider.TicksAbove, 10, 10,
                         (10, 115, 150, 50), self.graph, "label_w1_1", "W1(1,1):", (50, 115 - 25, 100, 50))

        self.make_slider("slider_w1_2", QtCore.Qt.Horizontal, (-100, 100), QtWidgets.QSlider.TicksAbove, 10, 10,
                         (10, 380, 150, 50), self.graph, "label_w1_2", "W1(2,1):", (50, 380 - 25, 100, 50))

        self.make_slider("slider_b1_1", QtCore.Qt.Horizontal, (-100, 100), QtWidgets.QSlider.TicksAbove, 10, -10,
                         (170, 115, 150, 50), self.graph, "label_b1_1", "b1(1):", (210, 115 - 25, 100, 50))

        self.make_slider("slider_b1_2", QtCore.Qt.Horizontal, (-100, 100), QtWidgets.QSlider.TicksAbove, 10, 10,
                         (170, 380, 150, 50), self.graph, "label_b1_2", "b1(2):", (210, 380 - 25, 100, 50))

        self.make_slider("slider_w2_1", QtCore.Qt.Horizontal, (-20, 20), QtWidgets.QSlider.TicksAbove, 1, -10,
                         (330, 115, 150, 50), self.graph, "label_w2_1", "W2(1,1):", (370, 115 - 25, 100, 50))

        self.make_slider("slider_w2_2", QtCore.Qt.Horizontal, (-20, 20), QtWidgets.QSlider.TicksAbove, 1, 10,
                         (330, 380, 150, 50), self.graph, "label_w2_2", "W2(1,2):", (370, 380 - 25, 100, 50))

        self.make_slider("slider_b2", QtCore.Qt.Horizontal, (-20, 20), QtWidgets.QSlider.TicksAbove, 1, 0,
                         (360, 180, 150, 50), self.graph, "label_b2", "b2:", (400, 180 - 25, 100, 50))

        self.graph()

    def graph(self):

        a = self.figure.add_subplot(1, 1, 1)
        a.clear()
        a.set_xlim(-2, 2)
        # a.set_ylim(-2, 2)
        # a.plot([0] * 10, np.linspace(-2, 2, 10), color="black", linestyle="--", linewidth=0.2)
        a.plot(np.linspace(-2, 2, 10), [0] * 10, color="black", linestyle="--", linewidth=0.2)
        a.set_title("a = purelin(w2 * {}(w1 * p + b1) + b2))".format(self.comboBox1_functions_str[self.idx]))

        weight1_1 = self.slider_w1_1.value() / 10
        weight1_2 = self.slider_w1_2.value() / 10
        bias1_1 = self.slider_b1_1.value() / 10
        bias1_2 = self.slider_b1_2.value() / 10
        weight2_1 = self.slider_w2_1.value() / 10
        weight2_2 = self.slider_w2_2.value() / 10
        bias2 = self.slider_b2.value() / 10

        self.label_w1_1.setText("W1(1,1): " + str(weight1_1))
        self.label_w1_2.setText("W1(2,1): " + str(weight1_2))
        self.label_b1_1.setText("b1(1): " + str(bias1_1))
        self.label_b1_2.setText("b1(2): " + str(bias1_2))
        self.label_w2_1.setText("W2(1,1): " + str(weight2_1))
        self.label_w2_2.setText("W2(1,2): " + str(weight2_2))
        self.label_b2.setText("b2: " + str(bias2))

        weight_1, bias_1 = np.array([[weight1_1, weight1_2]]), np.array([[bias1_1, bias1_2]])
        weight_2, bias_2 = np.array([[weight2_1], [weight2_2]]), np.array([[bias2]])

        p = np.arange(-4, 4, 0.1)
        func = np.vectorize(self.func1)
        out = np.dot(func(np.dot(p.reshape(-1, 1), weight_1) + bias_1), weight_2) + bias_2

        a.plot(p, out.reshape(-1), markersize=3, color="red")
        a.plot([0] * 1000, np.linspace(min([0, np.min(out)]), np.max([0, np.max(out)]), 1000), color="black", linestyle="--", linewidth=0.2)

        self.canvas.draw()

    def change_transfer_function(self, idx):
        self.func1 = self.comboBox1_functions[idx]
        self.idx = idx
        self.graph()

    def on_random(self):
        self.slider_w1_1.setValue(np.random.uniform(-100, 100))
        self.slider_w1_2.setValue(np.random.uniform(-100, 100))
        self.slider_b1_1.setValue(np.random.uniform(-100, 100))
        self.slider_b1_2.setValue(np.random.uniform(-100, 100))
        self.slider_w2_1.setValue(np.random.uniform(-20, 20))
        self.slider_w2_2.setValue(np.random.uniform(-20, 20))
        self.slider_b2.setValue(np.random.uniform(-20, 20))
        self.graph()

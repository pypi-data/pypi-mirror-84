from PyQt5 import QtWidgets, QtCore
import numpy as np
import warnings
import matplotlib.cbook
warnings.filterwarnings("ignore", category=matplotlib.cbook.mplDeprecation)
from matplotlib.animation import FuncAnimation

from nndesigndemos.nndesign_layout import NNDLayout
from nndesigndemos.get_package_path import PACKAGE_PATH


class Generalization(NNDLayout):
    def __init__(self, w_ratio, h_ratio, dpi):
        super(Generalization, self).__init__(w_ratio, h_ratio, dpi, main_menu=1)

        self.fill_chapter("Generalization", 11, "Click the [Train] button\nto train the logsig-linear\nnetwork on the data points.\n\n"
                                                "Use the slide bars to choose\nthe number of neurons and\nthe difficulty of the\ndata points.",
                          PACKAGE_PATH + "Logo/Logo_Ch_11.svg", None)

        self.mu_initial = 0.01
        # self.mingrad = 0.001

        self.S1 = 4
        self.diff = 1
        self.p = np.linspace(-2, 2, 100)
        self.W1, self.b1, self.W2, self.b2 = None, None, None, None
        self.mu = None
        self.ani = None
        self.random_state = 0
        self.init_params()
        self.error_prev, self.ii = 1000, None
        self.RS, self.RS1, self.RSS, self.RSS1 = None, None, None, None
        self.RSS2, self.RSS3, self.RSS4 = None, None, None
        self.init_params()

        self.p = None
        self.make_plot(1, (20, 90, 480, 480))
        self.axes = self.figure.add_subplot(111)
        self.figure.subplots_adjust(bottom=0.2, left=0.1)
        self.axes.set_xlim(-2, 2)
        self.axes.set_ylim(0, 2)
        self.axes.tick_params(labelsize=8)
        self.axes.set_xlabel("Input", fontsize=int(10 * (self.w_ratio + self.h_ratio) / 2))
        self.axes.xaxis.set_label_coords(0.5, 0.1)
        self.axes.set_ylabel("Target", fontsize=int(10 * (self.w_ratio + self.h_ratio) / 2))
        self.axes.yaxis.set_label_coords(0.05, 0.5)
        self.data_to_approx, = self.axes.plot([], "r+", label="Function to Approximate")
        self.net_approx, = self.axes.plot([], label="Network Approximation")
        self.axes.legend(loc='lower center', fontsize=int(8 * (self.w_ratio + self.h_ratio) / 2), framealpha=0.9, numpoints=1, ncol=3,
                         bbox_to_anchor=(0, -.24, 1, -.280), mode='expand')
        self.axes.set_title("Function Approximation")

        self.make_label("label_s11", "1", (40, 550, 20, 50))
        self.make_label("label_s12", "9", (475, 550, 20, 50))
        self.make_label("label_s1", "Number of Hidden Neurons S1: 4", (170, 550, 200, 50))
        self.make_label("label_diff1", "1", (40, 610, 20, 50))
        self.make_label("label_diff2", "9", (475, 610, 20, 50))
        self.make_label("label_diff", "Difficulty index: 1", (210, 610, 200, 50))
        self.make_slider("slider_s1", QtCore.Qt.Horizontal, (1, 9), QtWidgets.QSlider.TicksAbove, 1, 4,
                         (20, 580, 480, 50), self.slide)
        self.make_slider("slider_diff", QtCore.Qt.Horizontal, (1, 9), QtWidgets.QSlider.TicksAbove, 1, 1,
                         (20, 635, 480, 50), self.slide)

        self.make_slider("slider_delay", QtCore.Qt.Horizontal, (0, 50), QtWidgets.QSlider.TicksAbove, 1, 2,
                         (self.x_chapter_usual, 390, self.w_chapter_slider, 50), self.slide, "label_delay", "Animation Delay: 20",
                         (self.x_chapter_usual + 20, 390 - 25, self.w_chapter_slider, 50))
        self.anim_delay = 20

        self.make_button("run_button", "Train",
                         (self.x_chapter_button, 310, self.w_chapter_button, self.h_chapter_button), self.on_run)

        self.make_button("pause_button", "Pause",
                         (self.x_chapter_button, 340, self.w_chapter_button, self.h_chapter_button), self.on_stop)
        self.pause = True

        self.plot_f()

    def on_stop(self):
        if self.pause:
            if self.ani:
                self.ani.event_source.stop()
            self.pause_button.setText("Unpause")
            self.pause = False
        else:
            if self.ani:
                self.ani.event_source.start()
            self.pause_button.setText("Pause")
            self.pause = True

    def slide(self):
        self.error_prev = 1000
        if self.ani:
            self.ani.event_source.stop()
        slider_s1 = self.slider_s1.value()
        if self.S1 != slider_s1:
            self.S1 = slider_s1
            self.init_params()
        self.diff = self.slider_diff.value()
        self.p = np.linspace(-2, 2, 11 * self.slider_diff.value())
        self.p = self.p.reshape(1, -1)
        self.label_s1.setText("Number of Hidden Neurons S1: {}".format(self.S1))
        self.label_diff.setText("Difficulty Index: {}".format(self.diff))
        self.f_to_approx = lambda p: 1 + np.sin(np.pi * p * self.diff / 5)
        self.anim_delay = self.slider_delay.value() * 10
        self.label_delay.setText("Animation Delay: " + str(self.anim_delay))
        self.net_approx.set_data([], [])
        self.plot_f()

    def init_params(self):
        # np.random.seed(self.random_state)
        p_min, p_max = np.min(self.p), np.max(self.p)
        magw = 2.8 * self.S1 ** (1 / 1)
        self.W1 = np.random.uniform(-0.5, 0.5, (self.S1, 1))
        self.W1[self.W1 < 0] = -1
        self.W1[self.W1 >= 0] = 1
        self.W1 *= magw
        self.b1 = magw * np.random.uniform(-0.5, 0.5, (self.S1, 1))
        rng = p_min - p_max
        mid = 0.5 * (p_min + p_max)
        self.W1 = 2 * self.W1 / rng
        self.b1 = self.b1 - self.W1 * mid
        self.W2 = np.random.uniform(-0.5, 0.5, (1, self.S1))
        self.b2 = np.random.uniform(-0.5, 0.5, (1, 1))

    def plot_f(self):
        self.p = np.linspace(-2, 2, 11 * self.slider_diff.value())
        self.p = self.p.reshape(-1, 1)
        self.data_to_approx.set_data(self.p, 1 + np.sin(np.pi * self.p * self.diff / 5))
        self.canvas.draw()

    def f_to_approx(self, p):
        return 1 + np.sin(np.pi * p * self.diff / 5)

    # https://jakevdp.github.io/blog/2012/08/18/matplotlib-animation-tutorial/
    def on_run(self):
        self.pause_button.setText("Pause")
        self.pause = True
        if self.ani:
            self.ani.event_source.stop()
        n_epochs = 100
        self.ani = FuncAnimation(self.figure, self.on_animate_v2, init_func=self.animate_init_v2, frames=n_epochs,
                                 interval=self.anim_delay, repeat=False, blit=True)

    def animate_init(self):
        self.net_approx.set_data([], [])
        return self.net_approx,

    def on_animate(self, idx):

        alpha = 0.1
        nn_output = []

        for sample in self.p:

            a0 = sample.reshape(-1, 1)
            n1 = np.dot(self.W1, a0) + self.b1
            a1 = self.logsigmoid(n1)
            n2 = np.dot(self.W2, a1) + self.b2
            a = self.purelin(n2)
            nn_output.append(a)

            e = self.f_to_approx(a0) - a
            F2_der = np.diag(self.purelin_der(n2).reshape(-1))
            s = -2 * np.dot(F2_der, e)  # (s2 = s)
            F1_der = np.diag(self.logsigmoid_der(n1).reshape(-1))
            s1 = np.dot(F1_der, np.dot(self.W2.T, s))

            self.W1 += -alpha * np.dot(s1, a0.T)
            self.b1 += -alpha * s1
            self.W2 += -alpha * np.dot(s, a1.T)
            self.b2 += -alpha * s

        p = np.linspace(-2, 2, 100).reshape(1, -1)
        a = np.dot(self.W2, self.logsigmoid(np.dot(self.W1, p) + self.b1)) + self.b2
        self.net_approx.set_data(p, a)
        return self.net_approx,

    def animate_init_v2(self):
        np.random.seed(5)
        self.init_params()
        self.error_goal_reached = False
        self.p = self.p.reshape(1, -1)
        self.a1 = self.logsigmoid_stable(np.dot(self.W1, self.p) + self.b1)
        self.a2 = self.purelin(np.dot(self.W2, self.a1) + self.b2)
        self.e = self.f_to_approx(self.p) - self.a2
        self.error_prev = np.dot(self.e, self.e.T).item()
        self.mu = self.mu_initial
        self.RS = self.S1 * 1
        self.RS1 = self.RS + 1
        self.RSS = self.RS + self.S1
        self.RSS1 = self.RSS + 1
        self.RSS2 = self.RSS + self.S1 * 1
        self.RSS3 = self.RSS2 + 1
        self.RSS4 = self.RSS2 + 1
        self.ii = np.eye(self.RSS4)
        self.net_approx.set_data([], [])
        return self.net_approx,

    def on_animate_v2(self, idx):
        """ Marqdt version """

        self.mu /= 10

        self.a1 = np.kron(self.a1, np.ones((1, 1)))
        d2 = self.lin_delta(self.a2)
        d1 = self.log_delta(self.a1, d2, self.W2)
        jac1 = self.marq(np.kron(self.p, np.ones((1, 1))), d1)
        jac2 = self.marq(self.a1, d2)
        jac = np.hstack((jac1, d1.T))
        jac = np.hstack((jac, jac2))
        jac = np.hstack((jac, d2.T))
        je = np.dot(jac.T, self.e.T)

        # grad = np.sqrt(np.dot(je.T, je)).item()
        # if grad < self.mingrad:
        #     self.net_approx.set_data(self.p.reshape(-1), self.a2.reshape(-1))
        #     return self.net_approx,

        jj = np.dot(jac.T, jac)
        # Can't get this operation to produce the exact same results as MATLAB...
        dw = -np.dot(np.linalg.inv(jj + self.mu * self.ii), je)
        dW1 = dw[:self.RS]
        db1 = dw[self.RS:self.RSS]
        dW2 = dw[self.RSS:self.RSS2].reshape(1, -1)
        db2 = dw[self.RSS2].reshape(1, 1)

        self.a1 = self.logsigmoid_stable(np.dot((self.W1 + dW1), self.p) + self.b1 + db1)
        self.a2 = self.purelin(np.dot((self.W2 + dW2), self.a1) + self.b2 + db2)
        self.e = self.f_to_approx(self.p) - self.a2
        error = np.dot(self.e, self.e.T).item()

        while error >= self.error_prev:

            try:

                self.mu *= 10
                if self.mu > 1e10:
                    break

                dw = -np.dot(np.linalg.inv(jj + self.mu * self.ii), je)
                dW1 = dw[:self.RS]
                db1 = dw[self.RS:self.RSS]
                dW2 = dw[self.RSS:self.RSS2].reshape(1, -1)
                db2 = dw[self.RSS2].reshape(1, 1)

                self.a1 = self.logsigmoid_stable(np.dot((self.W1 + dW1), self.p) + self.b1 + db1)
                self.a2 = self.purelin(np.dot((self.W2 + dW2), self.a1) + self.b2 + db2)
                self.e = self.f_to_approx(self.p) - self.a2
                error = np.dot(self.e, self.e.T).item()

            except Exception as e:
                if str(e) == "Singular matrix":
                    print("The matrix was singular... Increasing mu 10-fold")
                    self.mu *= 10
                else:
                    raise e

        if error < self.error_prev:
            self.W1 += dW1
            self.b1 += db1
            self.W2 += dW2
            self.b2 += db2
            self.error_prev = error

        p = np.linspace(-2, 2, 100).reshape(1, -1)
        a1 = self.logsigmoid_stable(np.dot(self.W1, p) + self.b1)
        a2 = self.purelin(np.dot(self.W2, a1) + self.b2)
        self.net_approx.set_data(p.reshape(-1), a2.reshape(-1))
        return self.net_approx,

#!/usr/bin/env python
# coding = utf-8

import sys

from PyQt4 import QtCore as qc
from PyQt4 import QtGui as qw

import pyqtgraph

import params
import thermodynamics


class TabulationParameters(qw.QWidget):
    lbl_t = None
    inp_t = None

    lbl_r = None
    inp_r = None

    rb_mode_r = None
    rb_mode_t = None

    def __init__(self):
        super(TabulationParameters, self).__init__()

        self.rb_mode_r = qw.QRadioButton(u'Фіксований радіус')
        self.rb_mode_t = qw.QRadioButton(u'Фіксований час')

        layout = qw.QVBoxLayout()
        self.setLayout(layout)

        self.lbl_t = qw.QLabel(u't')
        self.lbl_r = qw.QLabel(u'r')

        self.inp_r = qw.QDoubleSpinBox()
        self.inp_r.setDecimals(4)
        self.inp_r.setSingleStep(0.0001)
        self.inp_r.setSuffix(u'м')
        self.inp_r.setValue(0.0085)

        self.inp_t = qw.QDoubleSpinBox()
        self.inp_t.setDecimals(5)
        self.inp_t.setSingleStep(0.00001)
        self.inp_t.setSuffix(u'с')
        self.inp_t.setValue(0.00001)

        layout.addWidget(self.rb_mode_r)
        layout.addWidget(self.rb_mode_t)
        layout.addWidget(self.inp_r)
        layout.addWidget(self.inp_t)

        def showhide_t():
            # self.lbl_t.setVisible(self.rb_mode_t.isChecked())
            self.inp_t.setVisible(self.rb_mode_t.isChecked())

        def showhide_r():
            # self.lbl_r.setVisible(self.rb_mode_r.isChecked())
            self.inp_r.setVisible(self.rb_mode_r.isChecked())

        self.rb_mode_t.toggled.connect(showhide_t)
        self.rb_mode_r.toggled.connect(showhide_r)

        self.rb_mode_r.toggle()
        showhide_r()
        showhide_t()

    @property
    def parameters(self):
        value = 0
        mode = None
        if self.rb_mode_r.isChecked():
            mode = params.TabulationParameters.MODE_FIXED_RADIUS
            value = self.inp_r.value()
        elif self.rb_mode_t.isChecked():
            value = self.inp_t.value()
            mode = params.TabulationParameters.MODE_FIXED_TIME
        return params.TabulationParameters(mode, value)


class MaterialPicker(qw.QWidget):
    ITEMS = [
        params.MaterialProperties.STEEL,
        params.MaterialProperties.COPPER,
        params.MaterialProperties.ALUMINIUM,
    ]

    material_combobox = None
    material_selected = qc.pyqtSignal(params.MaterialProperties, name='materialSelected')
    title = u'Матеріал'

    def __init__(self, title, default_material=None):
        super(MaterialPicker, self).__init__()
        self.title = title
        self.material_combobox = qw.QComboBox()
        self.init_ui()
        if default_material:
            item_index = self.ITEMS.index(default_material)
            self.material_combobox.setCurrentIndex(item_index)

    def init_ui(self):
        layout = qw.QHBoxLayout()
        self.setLayout(layout)

        self.material_combobox.currentIndexChanged.connect(self._material_index_changed)

        self.material_combobox.addItem(u'Сталь', params.MaterialProperties.STEEL)
        self.material_combobox.addItem(u'Мідь', params.MaterialProperties.COPPER)
        self.material_combobox.addItem(u'Алюміній', params.MaterialProperties.ALUMINIUM)

        layout.addWidget(qw.QLabel(self.title))
        layout.addWidget(self.material_combobox)

    @property
    def selected_material(self):
        material_code = self.material_combobox.itemData(self.material_combobox.currentIndex())
        material_properties = params.MaterialProperties(material_code)
        return material_properties

    def _material_index_changed(self, _):
        self.material_selected.emit(self.selected_material)


class MaterialProperty(qw.QWidget):
    title = u''
    fmt = '{:.3e}'
    unit = u''

    def __init__(self, title, fmt=None, unit=None):
        super(MaterialProperty, self).__init__()

        self.fmt = fmt or MaterialProperty.fmt
        self.unit = unit or MaterialProperty.unit

        self.lbl_title = qw.QLabel()
        self.lbl_value = qw.QLabel()
        self.lbl_unit = qw.QLabel()
        self.lbl_unit.setAlignment(qc.Qt.AlignRight)
        self.lbl_unit.setMinimumWidth(50)

        self.lbl_title.setSizePolicy(qw.QSizePolicy.MinimumExpanding, qw.QSizePolicy.Preferred)
        self.lbl_value.setSizePolicy(qw.QSizePolicy.Preferred, qw.QSizePolicy.Preferred)
        self.lbl_unit.setSizePolicy(qw.QSizePolicy.Preferred, qw.QSizePolicy.Preferred)

        self.lbl_title.setText(title)
        self.lbl_unit.setText(unit)

        layout = qw.QHBoxLayout()
        self.setLayout(layout)

        layout.addWidget(self.lbl_title)
        layout.addWidget(self.lbl_value)
        layout.addWidget(self.lbl_unit)

    def set_value(self, value):
        s_value = self.fmt.format(value)
        self.lbl_value.setText(s_value)


class MaterialProperties(qw.QWidget):
    def __init__(self):
        super(MaterialProperties, self).__init__()

        self.sigma = MaterialProperty(u'К-т електропровідності σ', unit=u'1/Ом·м')
        self.mu = MaterialProperty(u'Магнітна проникливість μ', unit=u'Гн/м')
        self.nu = MaterialProperty(u'К-т Пуассона υ', fmt='{:.3f}')

        self.k = MaterialProperty(u'К-т температуропровідності υ', unit=u'м²/с')
        self.lambda_ = MaterialProperty(u'К-т теплопровідності υ', unit=u'Вт/(м·К)')
        self.E = MaterialProperty(u'Модуль Юнга υ', unit=u'Н/м²')

        self.alpha = MaterialProperty(u'К-т лінійного розширення υ', unit=u'1/К')
        self.rho = MaterialProperty(u'Густина υ', fmt='{:d}', unit=u'кг/м³')
        self.sigma_t = MaterialProperty(u'Границя текучості υ', fmt='{:d}', unit=u'МПа')

        self.init_ui()

    def init_ui(self):
        layout = qw.QVBoxLayout()
        self.setLayout(layout)

        layout.addWidget(self.sigma)
        layout.addWidget(self.mu)
        layout.addWidget(self.nu)

        layout.addWidget(self.k)
        layout.addWidget(self.lambda_)
        layout.addWidget(self.E)

        layout.addWidget(self.alpha)
        layout.addWidget(self.rho)
        layout.addWidget(self.sigma_t)

    def update_widgets(self, material_properties):
        print('Updating material properties to ' + material_properties.material_type)
        self.sigma.set_value(material_properties['sigma'])
        self.mu.set_value(material_properties['mu'])
        self.nu.set_value(material_properties['nu'])

        self.k.set_value(material_properties['k'])
        self.lambda_.set_value(material_properties['lambda'])
        self.E.set_value(material_properties['E'])
        self.alpha.set_value(material_properties['alpha'])
        self.rho.set_value(material_properties['rho'])
        self.sigma_t.set_value(material_properties['sigma_t'])

    def set_material_properties(self, material_properties):
        self.update_widgets(material_properties)


class MaterialPanel(qw.QWidget):
    material_picker = None
    material_properties = None
    
    def __init__(self,  title, default_material=None):
        super(MaterialPanel, self).__init__()
        self.material_picker = MaterialPicker(title, default_material)
        self.material_properties = MaterialProperties()

        self.init_ui()

    def init_ui(self):
        layout = qw.QVBoxLayout()
        self.setLayout(layout)

        layout.addWidget(self.material_picker)
        # layout.addWidget(self.material_properties)

        self.material_picker.material_selected.connect(self.material_properties.set_material_properties)
        self.material_properties.set_material_properties(self.material_picker.selected_material)

    @property
    def material(self):
        return self.material_picker.selected_material


class CalculationParameters(qw.QWidget):
    t_label = None
    t_input = None

    r0_label = None
    r0_input = None

    r1_label = None
    r1_input = None

    r2_label = None
    r2_input = None

    def __init__(self):
        super(CalculationParameters, self).__init__()

        self.t_label = qw.QLabel(u'Тривалість імпульсу')
        self.t_input = qw.QDoubleSpinBox()

        self.r0_label = qw.QLabel(u'Внутрішній радіус')
        self.r1_label = qw.QLabel(u'Радіус стику')
        self.r2_label = qw.QLabel(u'Зовнішній радіус')

        self.r0_input = qw.QDoubleSpinBox()
        self.r1_input = qw.QDoubleSpinBox()
        self.r2_input = qw.QDoubleSpinBox()

        self.init_ui()

    def init_ui(self):
        layout = qw.QGridLayout()
        self.setLayout(layout)

        self.t_input.setSuffix(u"c")
        self.t_input.setDecimals(4)
        self.t_input.setMinimum(0.0001)
        self.t_input.setSingleStep(0.0001)
        self.t_input.setValue(0.0001)

        for inp in (self.r0_input, self.r1_input, self.r2_input):
            inp.setMinimum(0.001)
            inp.setSingleStep(0.001)
            inp.setDecimals(3)
            inp.setSuffix(u'м')

        self.r0_input.setValue(0.008)
        self.r1_input.setValue(0.009)
        self.r2_input.setValue(0.01)

        layout.addWidget(self.t_label, 0, 0)
        layout.addWidget(self.t_input, 0, 1)

        layout.addWidget(self.r0_label, 1, 0)
        layout.addWidget(self.r0_input, 1, 1)
        layout.addWidget(self.r1_label, 2, 0)
        layout.addWidget(self.r1_input, 2, 1)
        layout.addWidget(self.r2_label, 3, 0)
        layout.addWidget(self.r2_input, 3, 1)

    @property
    def parameters(self):
        calculation_parameters = params.CalculationParameters(self.t_input.value())
        calculation_parameters.r = tuple(map(float, (self.r0_input.value(), self.r1_input.value(), self.r2_input.value())))
        return calculation_parameters


class PlotWidget(qw.QTabWidget):
    MODE_FIXED_TIME = "t"
    MODE_FIXED_RADIUS = "r"

    pw_H = None
    pw_Q = None
    pw_F = None

    def __init__(self):
        super(PlotWidget, self).__init__()
        self.pw_H = pyqtgraph.PlotWidget()
        self.pw_H.setBackgroundBrush(qw.QBrush(qc.Qt.white))

        self.pw_Q = pyqtgraph.PlotWidget()
        self.pw_Q.setBackgroundBrush(qw.QBrush(qc.Qt.white))

        self.pw_F = pyqtgraph.PlotWidget()
        self.pw_F.setBackgroundBrush(qw.QBrush(qc.Qt.white))

        self.pw_H.plotItem.setLabel('left', u'H')
        self.pw_Q.plotItem.setLabel('left', u'Q')
        self.pw_F.plotItem.setLabel('left', u'F')

        self.addTab(self.pw_H, u'H')
        self.addTab(self.pw_Q, u'Q')
        self.addTab(self.pw_F, u'F')

    def update_labels(self, mode):
        label = None
        if mode == self.MODE_FIXED_RADIUS:
            label = u't'
        elif mode == self.MODE_FIXED_TIME:
            label = u'r'
        for pw in (self.pw_H, self.pw_Q, self.pw_F):
            pw.plotItem.setLabel('bottom', label)


class UI(qw.QWidget):
    material_panel_1 = None
    material_panel_2 = None
    calculation_parameters = None
    tabulation_parameters = None
    button_run = None
    plot_widget = None

    def __init__(self):
        super(UI, self).__init__()
        self.material_panel_1 = MaterialPanel(u'Внутрішній матеріал', params.MaterialProperties.STEEL)
        self.material_panel_2 = MaterialPanel(u'Зовнішній матеріал', params.MaterialProperties.COPPER)
        self.calculation_parameters = CalculationParameters()
        self.tabulation_parameters = TabulationParameters()
        self.button_run = qw.QPushButton(text=u'Обчислити')
        self.plot_widget = PlotWidget()

        self.init_ui()

    def init_ui(self):
        layout = qw.QHBoxLayout()
        self.setLayout(layout)

        column_left = qw.QVBoxLayout()

        column_left.addWidget(self.calculation_parameters)
        column_left.addWidget(self.material_panel_1)
        column_left.addWidget(self.material_panel_2)
        column_left.addWidget(self.tabulation_parameters)
        column_left.addWidget(self.button_run)

        layout.addLayout(column_left)
        layout.addWidget(self.plot_widget)

        self.button_run.clicked.connect(self.calculate)

        self.setWindowTitle(u'Параметри')

    def calculate(self):
        material_properties_1 = self.material_panel_1.material
        material_properties_2 = self.material_panel_2.material
        calculation_parametrs = self.calculation_parameters.parameters
        tabulation_parameters = self.tabulation_parameters.parameters

        h = thermodynamics.H_Calculator(calculation_parametrs, material_properties_1, material_properties_2)
        qf = thermodynamics.QF_Calculator(h, (material_properties_1, material_properties_2))

        # print(calculator.p(1))
        # print(calculator.p(2))
        #
        # print("")
        # print("")
        # print("List of A")
        # print("")
        #

        # for n in (1, 2):
        #     for i in (0, 1, 2):
        #         for j in (1, 2, 3, 4):
        #             print('{i}/{j}/{n} {a:e}'.format(i=i, j=j, n=n, a=calculator.a(i, j, n)))
        #
        # print(calculator.p(1), calculator.p(2))
        # return

        # for i in range(3):
        #     for j in range(1, 5):
        #         print("a ({i}, {j}) = {a:e}".format(i=i, j=j, a=calculator.a(i, j)))
        #
        # for j in range(1, 8):
        #     print("d{0} = {1}".format(j, calculator.d(j)))
        # return

        DIVISION = 250

        r_t = []
        x = []
        if tabulation_parameters.mode == params.TabulationParameters.MODE_FIXED_RADIUS:
            t_0 = 0.
            t_1 = calculation_parametrs.t_i * 1.5
            r = tabulation_parameters.value
            delta = (t_1 - t_0) / DIVISION

            t = t_0
            while t < t_1:
                r_t.append((r, t))
                x.append(t)
                t += delta
        elif tabulation_parameters.mode == params.TabulationParameters.MODE_FIXED_TIME:
            r = calculation_parametrs.r[0]
            delta = (calculation_parametrs.r[2] - calculation_parametrs.r[0]) / DIVISION

            while r < calculation_parametrs.r[2]:
                r_t.append((r, tabulation_parameters.value))
                x.append(r)
                r += delta

        h_y, q_y, f_y = [], [], []
        for r, t in r_t:
            h_y.append(h.H(r, t).real)
            q_y.append(qf.Q(r, t).real)
            f_y.append(qf.F(r, t).real)

        def set_plot_data(plot_widget, x, y):
            pi_H = plot_widget.getPlotItem()
            pi_H.clearPlots()
            pi_H.plot(x, y)

        set_plot_data(self.plot_widget.pw_H, x, h_y)
        set_plot_data(self.plot_widget.pw_Q, x, q_y)
        set_plot_data(self.plot_widget.pw_F, x, f_y)


if __name__ == '__main__':

    app = qw.QApplication(sys.argv)

    ui = UI()
    ui.show()

    sys.exit(app.exec_())

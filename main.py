#!/usr/bin/env python
# coding = utf-8

import sys

from PyQt4 import QtCore as qc
from PyQt4 import QtGui as qw

import pyqtgraph

import params
import thermodynamics


class MaterialPicker(qw.QWidget):
    material_combobox = None
    material_selected = qc.pyqtSignal(params.MaterialProperties, name='materialSelected')

    def __init__(self):
        super(MaterialPicker, self).__init__()
        self.material_combobox = qw.QComboBox()
        self.init_ui()

    def init_ui(self):
        layout = qw.QHBoxLayout()
        self.setLayout(layout)

        self.material_combobox.currentIndexChanged.connect(self._material_index_changed)

        self.material_combobox.addItem(u'Сталь', params.MaterialProperties.STEEL)
        self.material_combobox.addItem(u'Мідь', params.MaterialProperties.COPPER)
        self.material_combobox.addItem(u'Алюміній', params.MaterialProperties.ALUMINIUM)

        layout.addWidget(qw.QLabel(u'Матеріал'))
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
    
    def __init__(self):
        super(MaterialPanel, self).__init__()
        self.material_picker = MaterialPicker()
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

    def __init__(self):
        super(CalculationParameters, self).__init__()

        self.t_label = qw.QLabel(u't_i')
        self.t_input = qw.QDoubleSpinBox()

        self.init_ui()

    def init_ui(self):
        layout = qw.QHBoxLayout()
        self.setLayout(layout)

        self.t_input.setSuffix(u"c")
        self.t_input.setDecimals(4)
        self.t_input.setMinimum(0.0001)
        self.t_input.setSingleStep(0.0001)
        self.t_input.setValue(0.0001)

        layout.addWidget(self.t_label)
        layout.addWidget(self.t_input)

    @property
    def parameters(self):
        return params.CalculationParameters(self.t_input.value())


class UI(qw.QWidget):
    material_panel_1 = None
    material_panel_2 = None
    calculation_parameters = None
    button_run = None
    plot_widget = None

    def __init__(self):
        super(UI, self).__init__()
        self.material_panel_1 = MaterialPanel()
        self.material_panel_2 = MaterialPanel()
        self.calculation_parameters = CalculationParameters()
        self.button_run = qw.QPushButton(text=u'Обчислити')
        self.plot_widget = pyqtgraph.PlotWidget()

        self.init_ui()

    def init_ui(self):
        layout = qw.QHBoxLayout()
        self.setLayout(layout)

        self.plot_widget.setBackgroundBrush(qw.QBrush(qc.Qt.white))

        column_left = qw.QVBoxLayout()

        column_left.addWidget(self.calculation_parameters)
        column_left.addWidget(self.material_panel_1)
        column_left.addWidget(self.material_panel_2)
        column_left.addWidget(self.button_run)

        layout.addLayout(column_left)
        layout.addWidget(self.plot_widget)

        self.button_run.clicked.connect(self.calculate)

        self.setWindowTitle(u'Параметри')

    def calculate(self):
        material_properties_1 = self.material_panel_1.material
        material_properties_2 = self.material_panel_2.material
        calculation_parametrs = self.calculation_parameters.parameters

        calculator = thermodynamics.H_Calculator(calculation_parametrs, material_properties_1, material_properties_2)

        r = calculation_parametrs.r[0]

        delta = (calculation_parametrs.r[2] - calculation_parametrs.r[0]) / 100.

        x, y = [], []

        while r < calculation_parametrs.r[2]:
            h = calculator.H(0, r, calculation_parametrs.t_i / 3)
            y.append(h.real)
            x.append(r)
            r += delta

        plot = self.plot_widget.plot()
        plot.setData(y=y, x=x)


if __name__ == '__main__':

    app = qw.QApplication(sys.argv)

    ui = UI()
    ui.show()

    sys.exit(app.exec_())

#!/usr/bin/env python
# coding = utf-8

import sys

from PyQt5 import QtCore as qc
from PyQt5 import QtWidgets as qw

import params


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
        layout.addWidget(self.material_properties)

        self.material_picker.material_selected.connect(self.material_properties.set_material_properties)
        self.material_properties.set_material_properties(self.material_picker.selected_material)

    @property
    def material(self):
        return self.material_picker.selected_material


class UI(qw.QWidget):
    # material_picker = None
    # material_properties = None
    material_panel = None
    button_run = None

    def __init__(self):
        super(UI, self).__init__()
        self.material_panel = MaterialPanel()
        self.button_run = qw.QPushButton(text=u'Обчислити')

        self.init_ui()

    def init_ui(self):
        layout = qw.QVBoxLayout()
        self.setLayout(layout)

        self.setWindowTitle(u'Параметри')

        layout.addWidget(self.material_panel)
        layout.addWidget(self.button_run)


if __name__ == '__main__':

    app = qw.QApplication(sys.argv)

    ui = UI()
    ui.show()

    sys.exit(app.exec_())

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

    def _material_index_changed(self, material_index):
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

        self.lbl_title.setText(title)
        self.lbl_unit.setText(unit)

        layout = qw.QHBoxLayout()
        self.setLayout(layout)

        layout.addWidget(self.lbl_title)
        layout.addStretch()
        layout.addWidget(self.lbl_value)
        layout.addWidget(self.lbl_unit)

    def set_value(self, value):
        s_value = self.fmt.format(value)
        self.lbl_value.setText(s_value)


class MaterialProperties(qw.QWidget):
    def __init__(self):
        super(MaterialProperties, self).__init__()

        self.sigma = MaterialProperty(u'К-т електропровідності σ', unit=u'1/Ом * м')
        self.mu = MaterialProperty(u'Магнітна проникливість μ', unit=u'Гн/м')
        self.nu = MaterialProperty(u'К-т Пуассона υ', fmt='{:.3f}')

        self.init_ui()

    def init_ui(self):
        layout = qw.QVBoxLayout()
        self.setLayout(layout)

        layout.addWidget(self.sigma)
        layout.addWidget(self.mu)
        layout.addWidget(self.nu)

    def update_widgets(self, material_properties):
        print('Updating material properties to ' + material_properties.material_type)
        self.sigma.set_value(material_properties['sigma'])
        self.mu.set_value(material_properties['mu'])
        self.nu.set_value(material_properties['nu'])

    def set_material_properties(self, material_properties):
        self.update_widgets(material_properties)


class UI(qw.QWidget):
    material_picker = None
    material_properties = None
    button_run = None

    def __init__(self):
        super(UI, self).__init__()
        self.material_picker = MaterialPicker()
        self.material_properties = MaterialProperties()
        self.button_run = qw.QPushButton(text=u'Обчислити')

        self.material_picker.material_selected.connect(self.material_properties.set_material_properties)
        self.material_properties.set_material_properties(self.material_picker.selected_material)

        self.init_ui()

    def init_ui(self):
        layout = qw.QVBoxLayout()
        self.setLayout(layout)

        self.setWindowTitle(u'Параметри')

        layout.addWidget(self.material_picker)
        layout.addWidget(self.material_properties)
        layout.addWidget(self.button_run)


if __name__ == '__main__':

    app = qw.QApplication(sys.argv)

    ui = UI()
    ui.show()

    sys.exit(app.exec_())

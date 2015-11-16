#!/usr/bin/env python
# coding = utf-8

import sys

from PyQt5 import QtCore as qc
from PyQt5 import QtWidgets as qw

import params


class MaterialPicker(qw.QWidget):
    material_combobox = None
    material_selected = qc.pyqtSignal(str, name='materialSelected')

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

        layout.addWidget(qw.QLabel("Матеріал"))
        layout.addWidget(self.material_combobox)

    def _material_index_changed(self, material_index):
        material_code = self.material_combobox.itemData(material_index)
        self.material_selected.emit(material_code)


class UI(qw.QWidget):
    material_picker = None

    def __init__(self):
        super(UI, self).__init__()

        self.material_picker = MaterialPicker()

        self.init_ui()

    def init_ui(self):
        layout = qw.QGridLayout()
        self.setLayout(layout)

        layout.addWidget(self.material_picker, 0, 0)

        self.setGeometry(300, 300, 200, 200)
        self.setWindowTitle('Icon')


if __name__ == '__main__':

    app = qw.QApplication(sys.argv)

    ui = UI()
    ui.show()

    sys.exit(app.exec_())
# -*- coding: utf-8 -*-

import sys
from PyQt4 import QtGui, QtCore
from core import FreakCore


class FreakCalcGUI(QtGui.QMainWindow):
    def __init__(self):
        super(FreakCalcGUI, self).__init__()
        self.add_btn = None
        self.freak_del_btns = []
        self.freak_name_text = []
        self.freak_balance_text = []
        self.freak_each_path_label = []
        self.x = 10
        self.y = 20
        self.init_ui()
        self.freak_calc = FreakCore()

    def init_ui(self):
        self.setWindowTitle("Freak Calculator")
        self.statusBar().showMessage("Ready")
        self.setGeometry(300, 300, 500, 500)
        self.create_menu()
        self.create_add_button()

        self.y += 30
        self.show()

    def create_menu(self):
        menubar = self.menuBar()
        file_menu = menubar.addMenu("&File")

        # new_action = QtGui.QAction("New", self)
        # new_action.setStatusTip("New profile")

        # load_action = QtGui.QAction("Load", self)
        # load_action.setStatusTip("Load early saved profile")
        calc_action = QtGui.QAction("Calculate", self)
        calc_action.setStatusTip("Calculate balance")
        calc_action.triggered.connect(self.calculate)

        exit_action = QtGui.QAction("Exit", self)
        exit_action.setStatusTip("Exit application")
        exit_action.triggered.connect(QtGui.qApp.quit)

        # file_menu.addAction(new_action)
        # file_menu.addAction(load_action)
        file_menu.addAction(exit_action)
        file_menu.addAction(calc_action)
        help_menu = menubar.addMenu("&Help")

    def add_freak(self):
        self.freak_calc.add_freak()
        self.add_btn.move(self.x, self.y)
        self.create_del_button()
        self.create_name_label()
        self.create_balance_label()
        self.create_each_pay_label()
        self.freak_del_btns[-1].setText("del " + self.freak_calc.get_freak_names_nosort()[-1])
        self.freak_name_text[-1].setText(self.freak_calc.get_freak_names_nosort()[-1])
        self.y += 30

    def delete_freak(self):
        sender = self.sender()
        index = self.freak_del_btns.index(sender)
        old_btn = self.freak_del_btns.pop(index)
        old_name = self.freak_name_text.pop(index)
        old_blnc = self.freak_balance_text.pop(index)
        old_pay = self.freak_each_path_label.pop(index)
        self.freak_calc.delete_freak_by_index(index)
        self.y -= 30
        old_btn.hide()
        old_name.hide()
        old_blnc.hide()
        old_pay.hide()
        for index, btn in enumerate(self.freak_del_btns):
            btn.move(self.x + 350, 20 + index * 30)
            self.freak_name_text[index].move(self.x + 50, 20 + index * 30)
            self.freak_balance_text[index].move(self.x + 150, 20 + index * 30)
            self.freak_each_path_label[index].move(self.x + 250, 20 + index * 30)
        self.add_btn.move(self.x, 20 + 30 * len(self.freak_del_btns))

    def create_add_button(self):
        btn = QtGui.QPushButton("Add Freak", self)
        btn.clicked.connect(self.add_freak)
        btn.move(self.x, self.y)
        btn.show()
        if self.add_btn:
            old_btn = self.add_btn.pop()
            old_btn.hide()
        self.add_btn = btn

    def create_del_button(self):
        btn = QtGui.QPushButton("X", self)
        btn.resize(btn.sizeHint())
        btn.clicked.connect(self.delete_freak)
        btn.move(self.x + 350, self.y - 30)
        btn.show()
        self.freak_del_btns.append(btn)

    def create_name_label(self):
        lbl = QtGui.QLineEdit(self)
        lbl.move(self.x + 50, self.y - 30)
        lbl.editingFinished.connect(self.change_freak_name)
        lbl.show()
        self.freak_name_text.append(lbl)

    def change_freak_name(self):
        sender = self.sender()
        if sender in self.freak_name_text:
            index = self.freak_name_text.index(sender)
            self.freak_calc.freaks[index].change_name(sender.text())
            self.freak_del_btns[index].setText("del " + self.freak_calc.freaks[index].name)

    def create_balance_label(self):
        lbl = QtGui.QLineEdit(self)
        lbl.move(self.x + 150, self.y - 30)
        lbl.editingFinished.connect(self.change_freak_balance)
        lbl.show()
        self.freak_balance_text.append(lbl)

    def create_each_pay_label(self):
        lbl = QtGui.QLabel("0.0", self)
        lbl.move(self.x + 250, self.y - 30)
        lbl.show()
        self.freak_each_path_label.append(lbl)

    def change_freak_balance(self):
        sender = self.sender()
        if sender in self.freak_balance_text:
            index = self.freak_balance_text.index(sender)
            try:
                self.freak_calc.freaks[index].set_balance(float(sender.text()))
            except ValueError:
                sender.clear()
            sender.setText(str(self.freak_calc.freaks[index].balance))

    def calculate(self):
        if len(self.freak_calc.freaks):
            self.freak_calc.calculate_payments()
            for index, label in enumerate(self.freak_each_path_label):
                label.setText(str(self.freak_calc.freaks[index].need_to_pay))


if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    gui = FreakCalcGUI()
    sys.exit(app.exec_())

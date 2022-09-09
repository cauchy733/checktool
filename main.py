from PyQt5 import QtWidgets, uic
import sys
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QActionGroup, QFileDialog

import check_rules


class Ui(QtWidgets.QMainWindow):
    path_to_file = ""

    def __init__(self):
        super(Ui, self).__init__()
        self.ui = uic.loadUi('ui/form.ui')
        self.ui_dlg = uic.loadUi("ui/result_dlg.ui")
        self.ui_dlg.setWindowFlags(Qt.WindowCloseButtonHint)
        list_mode_qactions = self.ui.menumode.actions()
        self.ui.action_group_mode = QActionGroup(self.ui.menumode)
        for act in list_mode_qactions:
            self.ui.menumode.removeAction(act)
            self.ui.action_group_mode.addAction(act)
            self.ui.menumode.addAction(act)

        self.ui.actionopen.triggered.connect(self.openfile)
        self.ui.actiontranslate.triggered.connect(self.switch_to_mode_page)
        self.ui.actionruncheck.triggered.connect(self.check)
        self.ui.show()

    def openfile(self):
        __result = QFileDialog.getOpenFileName(self.ui, "请选择文件", None, "*.csv(*.csv)")
        if __result is None:
            self.path_to_file = ""
        else:
            self.path_to_file = __result[0]

    def switch_to_mode_page(self):
        mode_name = self.sender().objectName()
        if mode_name == "actiontranslate":
            self.ui.stackedWidget.setCurrentIndex(1)

    def check(self):

        order_builder = check_rules.OrderBuilder()

        list_match = self.ui.txt_match.toPlainText().split("\n")
        list_match = list(filter(lambda x: x != "", list_match))
        for str_match in list_match:
            order_builder.add_check_in_text(check_rules.CheckBracketsValid(str_match))

        list_exclude = self.ui.txt_exclude.toPlainText().split("\n")
        list_exclude = list(filter(lambda x: x != "", list_exclude))
        for str_exclude in list_exclude:
            order_builder.add_exclude_words(str_exclude)

        if self.ui.checkBox.checkState():
            order_builder.add_check_in_angle_brackets(check_rules.CheckIfHaveSpace())

        try:
            order_builder.set_txt_handle(open(self.path_to_file, "r", encoding="utf-8"))

            ord1 = order_builder.build()
            err_text = ord1.get_error_text()
            if err_text == "":
                self.ui_dlg.textEdit.setPlainText("未发现异常")
            else:
                self.ui_dlg.textEdit.setPlainText(err_text)
        except IOError:
            self.ui_dlg.textEdit.setPlainText("打开文件失败或未选择文件")
        finally:
            self.ui_dlg.show()


app = QtWidgets.QApplication(sys.argv)
window = Ui()
app.exec_()

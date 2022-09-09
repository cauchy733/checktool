import re
import csv


class Checker:
    check_fun = None
    errmsg = ""

    def check(self, text):
        return self.check_fun(text)

    def get_err_msg(self):
        return self.errmsg


class CheckBracketsValid(Checker):
    def __init__(self, params):
        self.check_fun = self.fun
        self.params = params

    def fun(self, text):
        i = 0
        for ch in text:
            if ch == self.params[0]:
                i = i + 1
            if ch == self.params[1]:
                i = i - 1
            if i < 0:
                self.errmsg = self.params + "不匹配"
                return False
        if i == 0:
            return True
        else:
            self.errmsg = self.params + "不匹配"
            return False


class CheckIfHaveSpace(Checker):
    def __init__(self):
        self.check_fun = self.fun

    def fun(self, text):
        if text.find(" ") != -1:
            self.errmsg = "<>中有空格"
            return False
        else:
            return True


class Order:
    error_text = ""

    def __init__(self, order_builder):
        line_ord = 0

        with order_builder.handle as csvfile:
            csv_reader = csv.reader(csvfile)
            for items in csv_reader:
                line_ord = line_ord + 1

                flag_found_ex_words = False
                for exclude_word in order_builder.list_exclude_words:
                    if items[0].find(exclude_word) != -1:
                        flag_found_ex_words = True
                        break
                if flag_found_ex_words:
                    continue

                for item in items:
                    for checker in order_builder.list_check_in_text:
                        if not checker.check(item):
                            self.error_text = self.error_text + str(
                                line_ord) + "行" + checker.get_err_msg() + item + "\n"
                            break

                    result = re.findall("<.+?>", item)
                    for content in result:
                        for checker in order_builder.list_check_in_angle_brackets:
                            if not checker.check(content):
                                self.error_text = self.error_text + str(
                                    line_ord) + "行" + checker.get_err_msg() + item + "\n"
                                break

    def get_error_text(self):
        return self.error_text


class OrderBuilder:
    def __init__(self):
        self.list_check_in_text = []
        self.list_check_in_angle_brackets = []
        self.list_exclude_words = []
        self.handle = None

    def set_txt_handle(self, handle):
        self.handle = handle

    def add_check_in_text(self, checker):
        self.list_check_in_text.append(checker)

    def add_check_in_angle_brackets(self, checker):
        self.list_check_in_angle_brackets.append(checker)

    def add_exclude_words(self, word):
        self.list_exclude_words.append(word)

    def build(self):
        return Order(self)

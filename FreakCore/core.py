class FreakCore(object):
    def_freak_name = "freak"

    def __init__(self, verbose=True):
        self.each_pay = 0
        self.freaks = []
        self.each_pay = 0
        self.verbose = verbose

    def print_freaks(self):
        string = []
        if len(self.freaks):
            for freak in self.freaks:
                string.append("Freak %s with balance=%2.2f" % (freak.name, freak.balance))
        else:
            string.append("Freaks nFot found")
        print "\n".join(string)
        # return "\n".join(string)

    def print_freaks_payments(self):
        string = []
        if len(self.freaks):
            for freak in self.freaks:
                string.append("Freak %s need to pay %2.2f" % (freak.name, freak.need_to_pay))
        else:
            string.append("Freaks not found")
        print "\n".join(string)

    def add_freak(self, name="", balance=0.0):
        if isinstance(balance, int):
            balance = float(balance)
        elif not isinstance(balance, float):
            print "Invalid type of balance: %s for name %s!" % (type(balance), name)
            print "Balance can be int or float!"
            return False
        if not name:
            name_index = 1
            while True:
                if "%s_%d" % (self.def_freak_name, name_index) not in self.get_freak_names():
                    name = "%s_%d" % (self.def_freak_name, name_index)
                    break
                name_index += 1
        if name in self.get_freak_names():
            print "Freak with name %s already exist! Can't use same names!" % name
            return False
        else:
            self.freaks.append(Freak(name, balance))
            if self.verbose:
                print "Freak %s added." % name
        return True

    def delete_freak(self, name):
        """ Delete freak with selected name by freak dict.
        :param name: Name of freak.
        :return: True if deleting success, False if deleting failed.
        """

        if name in self.get_freak_names():
            self.freaks.pop(self.get_freak_index(name))
            if self.verbose:
                print "Freak %s deleted." % name
            return True
        else:
            print "Freak %s not found." % name
            return False

    def delete_all_freaks(self):
        self.freaks = []
        self.each_pay = 0

    def get_freak_by_name(self, name):
        if name not in self.get_freak_names():
            print "Freak %s not found!" % name
            return False
        else:
            return self.freaks[self.get_freak_index(name)]

    def get_freak_index(self, name):
        for freak in self.freaks:
            if freak.name == name:
                return self.freaks.index(freak)
        return False

    def get_freak_names(self):
        return sorted([freak.name for freak in self.freaks])

    def set_freak_balance(self, name, balance):
        if name not in self.get_freak_names():
            print "Freak %s not found." % name
            return False
        else:
            self.freaks[self.get_freak_index(name)].set_balance(balance)

    def get_freak_balance(self, name):
        if name not in self.get_freak_names():
            print "Freak %s not found." % name
            return False
        else:
            return self.freaks[self.get_freak_index(name)].balance

    def _calculate_total_sum(self):
        total_sum = 0
        for freak in self.freaks:
            total_sum += freak.balance
        return total_sum

    def calculate_payments(self):
        total_sum = self._calculate_total_sum()
        self.each_pay = total_sum / len(self.freaks)
        print "Every freak must pay %2.2f" % self.each_pay
        for freak in self.freaks:
            freak.need_to_pay = self.each_pay - freak.balance

    def change_freak_name(self, name, new_name):
        if name not in self.get_freak_names():
            print "Freak %s not found!" % name
            return False
        else:
            if new_name in self.get_freak_names():
                print "Name %s already exist!" % new_name
                return False
            else:
                index = self.get_freak_index(name)
                old = self.freaks.pop(index)
                self.freaks.insert(index, old)
                self.freaks[index].change_name(new_name)
                del old, index


class Freak(object):
    def_freak_name = "freak"

    def __init__(self, name=def_freak_name, balance=0.0):
        self.__freak_name = name
        self.__freak_balance = 0.0
        self.set_balance(balance)
        self.need_to_pay = 0.0

    @property
    def name(self):
        return self.__freak_name

    @property
    def balance(self):
        return self.__freak_balance

    def set_balance(self, balance):
        if isinstance(balance, int):
            balance = float(balance)
        if isinstance(balance, float):
            self.__freak_balance = balance
            return True
        else:
            return False

    def change_name(self, new_name):
        self.__freak_name = new_name

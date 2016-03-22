class FreakCore(object):
    __freaks = []
    def_freak_name = "freak"

    def __init__(self):
        self.each_pay = 0

    # def __repr__(self):
    #     string = []
    #     if len(self.__freaks):
    #         for freak in self.__freaks:
    #             string.append("Freak %s with balance=%2.2f" % (freak.name, freak.balance))
    #     else:
    #         string.append("Freaks not found")
    #     return "\n".join(string)

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
            print "Freak with name %s already exist! Can't use same names!"
            return False
        else:
            self.__freaks.append(Freak(name, balance))
            print "Freak %s added." % name
        return True

    def delete_freak(self, name):
        """ Delete freak with selected name by freak dict.
        :param name: Name of freak.
        :return: True if deleting success, False if deleting failed.
        """

        if name in self.__freaks:
            self.__freaks.pop(self.get_freak_index(name))
            print "Freak %s deleted." % name
            return True
        else:
            print "Freak %s not found." % name
            return False

    def get_freak_by_name(self, name):
        if name not in self.get_freak_names():
            print "Freak %s not found!" % name
            return False
        else:
            return self.__freaks[self.get_freak_index(name)]

    def get_freak_index(self, name):
        for freak in self.__freaks:
            if freak.name == name:
                return self.__freaks.index(freak)
        return False

    def get_freak_names(self):
        return sorted([freak.name for freak in self.__freaks])

    def set_freak_balance(self, name, balance):
        if name not in self.get_freak_names():
            print "Freak %s not found." % name
            return False
        else:
            self.__freaks[self.get_freak_index(name)].set_balance(balance)

    def _calculate_total_sum(self):
        total_sum = 0
        for freak in self.__freaks:
            total_sum += freak.balance
        return total_sum

    def calculate_payments(self):
        total_sum = self._calculate_total_sum()
        self.each_pay = total_sum / len(self.__freaks)
        print "Every freak must pay %2.2f" % self.each_pay
        for freak in self.__freaks:
            freak.need_to_pay = self.each_pay - freak.balance
            print freak.name, freak.need_to_pay

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
                old = self.__freaks.pop(index)
                self.__freaks.insert(index, old)
                self.__freaks[index].change_name(new_name)
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

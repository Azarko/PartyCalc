# -*- coding: utf-8 -*-


""" Api for working with freak calculator """


class FreakCore(object):
    def_freak_name = "freak"

    def __init__(self, verbose=True):
        """ Initialize of class.
        :param verbose: True for show additional stdout. False - if needn't.
        """

        self.each_pay = 0
        self.__freaks = []
        self.each_pay = 0
        self.verbose = verbose

    @property
    def freaks(self):
        return self.__freaks

    def __iter__(self):
        for freak in self.freaks:
            yield freak

    def __len__(self):
        return len(self.freaks)

    def __getitem__(self, item):
        return self.freaks[item]

    def print_freaks(self):
        """ Print name and balance of each saved freak. """

        string = []
        if len(self.__freaks):
            for freak in self.__freaks:
                string.append("Freak %s with balance=%2.2f" % (freak.name, freak.balance))
        else:
            string.append("Freaks nFot found")
        print "\n".join(string)

    def print_freaks_payments(self):
        """ Print name and payment of each saved freak. """

        string = []
        if len(self.__freaks):
            for freak in self.__freaks:
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
            self.__freaks.append(Freak(name, balance))
            if self.verbose:
                print "Freak %s added." % name
        return True

    def delete_freak(self, name):
        """ Delete freak with selected name by freak dict.
        :param name: Name of freak.
        :return: True if deleting success, False if deleting failed.
        """

        if name in self.get_freak_names():
            self.__freaks.pop(self.get_freak_index(name))
            if self.verbose:
                print "Freak %s deleted." % name
            return True
        else:
            print "Freak %s not found." % name
            return False

    def delete_freak_by_index(self, index):
        """ Delete freak by index.
        :param index: Index of freak.
        :return:
        """

        if 0 <= index < len(self.__freaks):
            name = self.__freaks.pop(index).name
            if self.verbose:
                print "Freak %d(%s) deleted." % (index, name)
            return True
        else:
            print "Invalid index: %d." % index
            return False

    def delete_all_freaks(self):
        """ Delete all freaks.
        :return: True
        """

        self.__freaks = []
        self.each_pay = 0
        if self.verbose:
            print 'All freaks deleted'
        return True

    def get_freak_by_name(self, name):
        """ Returns freak by selected name.
        :param name: Name of freak.
        :return: Freak obj or False if freak not found
        """

        if name not in self.get_freak_names():
            print "Freak %s not found!" % name
            return False
        else:
            return self.__freaks[self.get_freak_index(name)]

    def get_freak_index(self, name):
        """ Return index in class list of freak with selected name/

        :param name: Name of freak.
        :return: List index or False
        """

        for freak in self.__freaks:
            if freak.name == name:
                return self.__freaks.index(freak)
        return False

    def get_freak_names(self):
        """ Return sorted list with freak names.
        :return: Names of all freaks (sorted).
        """

        return sorted(self.get_freak_names_nosort())

    def get_freak_names_nosort(self):
        """ Return not sorted list with freak names.
        :return: Names of all freaks (sorted).
        """

        return [freak.name for freak in self.__freaks]

    def get_freak_name(self, index):
        """ Get freak name by index.
        :param index: Index of freak.
        :return:
        """

        if 0 < index < len(self.__freaks):
            return self.__freaks[index].name
        else:
            print "Invalid index: ." % index
            return False

    def set_freak_balance(self, name, balance):
        """ Set to freak with selected name new balance. Old balance disappear.
        :param name: Name of freak.
        :param balance: New balance.
        :return: False if something wrong, True if all ok.
        """

        if name not in self.get_freak_names():
            print "Freak %s not found." % name
            return False
        else:
            self.__freaks[self.get_freak_index(name)].set_balance(balance)

    def get_freak_balance(self, name):
        """ Return balance of freak with selected name.
        :param name: Name of freak.
        :return: Freak's balance or False.
        """

        if name not in self.get_freak_names():
            print "Freak %s not found." % name
            return False
        else:
            return self.__freaks[self.get_freak_index(name)].balance

    def reset_freak_balance(self):
        """ Reset freaks balance to 0"""

        for freak in self.__freaks:
            freak.set_balance(0)

    def _calculate_total_sum(self):
        """ Return Total sum of all freak's balances.
        :return: sum
        """

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

    def change_freak_name(self, name, new_name):
        """ Change name of selected freak to new_name.
        :param name: Old name of freak.
        :param new_name: New name of freak. It can't be same with each one in existing list.
        :return: False of something wrong, else True.
        """
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
        return True


class Freak(object):
    """ Freak class. Contain base freak-unit. """
    def_freak_name = "freak"

    def __init__(self, name=def_freak_name, balance=0.0):
        """ Initialize of class.
        :param name: Name of freak.
        :param balance: Default freak balance.
        """

        self.__freak_name = name
        self.__freak_balance = 0.0
        self.set_balance(balance)
        self.need_to_pay = 0.0

    def __repr__(self):
        return '%s with balance %s' % (self.name, self.balance)

    @property
    def name(self):
        return self.__freak_name

    @property
    def balance(self):
        return self.__freak_balance

    def set_balance(self, balance):
        """ Set new balance.
        :param balance: New balance (int or float).
        :return:  False if all ok, else True.
        """

        if isinstance(balance, int):
            balance = float(balance)
        if isinstance(balance, float):
            self.__freak_balance = balance
            return False
        else:
            return True

    def change_name(self, new_name):
        """ Change freak name to new_name.
        :param new_name: New name for freak.
        """

        self.__freak_name = new_name

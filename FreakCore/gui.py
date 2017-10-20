# -*- coding: utf-8 -*-


from Tkinter import *
from tkMessageBox import askyesno
from tkSimpleDialog import askinteger
from core import FreakCore


class FreakGUI(Frame):
    def __init__(self, parent=None):
        Frame.__init__(self, parent)
        self.__freaks = FreakCore()
        self.__freak_frames = []
        self.__freak_payments = []
        self.__freak_mp = []
        self.pack(expand=YES, fill=BOTH)
        self.master.title('Freak Calculator')
        self.create_menu()
        self.create_toolbar()

    def create_menu(self):
        self.menu = Menu(self.master)
        self.master.config(menu=self.menu)
        self.create_menu_file()
        self.create_menu_edit()

    def create_menu_file(self):
        pulldown = Menu(self.menu)
        pulldown.add_command(label='Calculate', command=self.calculate)
        pulldown.add_separator()
        pulldown.add_command(label='Save', command=self.not_ready)
        pulldown.add_command(label='Save as...', command=self.not_ready)
        pulldown.add_command(label='Load', command=self.not_ready)
        pulldown.add_separator()
        pulldown.add_command(label='Exit', command=self.quit)
        self.menu.add_cascade(label='File', underline=0, menu=pulldown)

    def create_menu_edit(self):
        pulldown = Menu(self.menu)
        pulldown.add_command(label='Delete all freaks', command=self.delete_all_freaks)
        pulldown.add_command(label='Clear', command=self.clear)
        pulldown.add_command(label='Add freak', command=self.add_freak)
        pulldown.add_command(label='Add N freaks', command=self.add_n_freaks)
        self.menu.add_cascade(label='Edit', underline=0, menu=pulldown)

    def create_toolbar(self):
        toolbar = Frame(self)
        toolbar.pack(side=TOP, fill=X)
        Button(toolbar, text='Calculate', cursor='hand2', command=self.calculate).pack(side=LEFT)
        Button(toolbar, text='Add freak', cursor='hand2', command=self.add_freak).pack(side=LEFT)
        Button(toolbar, text='Clear', cursor='hand2', command=self.clear).pack(side=LEFT)
        Button(toolbar, text='Delete all freaks', cursor='hand2', command=self.delete_all_freaks).pack(side=LEFT)

    def add_freak(self):
        frame = Frame(self)
        self.__freaks.add_freak()
        freak_name = self.__freaks[-1].name
        name = Entry(frame, width=30)
        name.insert(0, freak_name)
        name.pack(side=LEFT)
        pay = Entry(frame, width=15)
        pay.insert(0, 0.0)
        pay.pack(side=LEFT)
        self.__freak_payments.append(pay)
        Label(frame, width=15, text='N/A').pack(side=LEFT)
        Button(frame, text='Del', command=lambda: self.delete_freak(frame)).pack(side=LEFT)
        frame.pack(side=TOP, )
        self.__freak_frames.append(frame)

    def add_n_freaks(self):
        n = askinteger('Enter count of freaks', 'Count of new freaks')
        if n is None:
            return
        elif n <= 0:
            raise ValueError('Count must be positive integer!')
        for count in range(n):
            self.add_freak()
            self.update()

    def delete_freak(self, frame):
        self.__freaks.delete_freak_by_index(self.__freak_frames.index(frame))
        self.__freak_frames.remove(frame)
        frame.pack_forget()

    def delete_all_freaks(self):
        if askyesno('Really delete', 'Are you really want to delete all members?'):
            for frame in self.__freak_frames:
                frame.pack_forget()
            self.__freaks.delete_all_freaks()

    def clear(self):
        if askyesno('Really clear', 'Are you really want to clear all payment information?'):
            for frame in self.__freak_payments:
                frame.delete(0, len(frame.get()))
                frame.insert(0, 0.0)
            # self.__freaks.reset_freak_balance()

    def not_ready(self):
        print 'Not ready'

    def calculate(self):
        pass

if __name__ == '__main__':
    FreakGUI().mainloop()

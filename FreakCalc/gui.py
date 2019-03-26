"""
Freak Calc GUI.
App for calculate party payments.
"""

__author__ = 'Boris Polyanskiy'

try:
    from Tkinter import *
    from tkMessageBox import askyesno, showinfo, showerror
    from tkSimpleDialog import askinteger
except ImportError:
    from tkinter import *
    from tkinter.messagebox import askyesno, showinfo, showerror
    from tkinter.simpledialog import askinteger

from .core import FreakCore

__version__ = '0.9.9 beta'
__all__ = ['FreakGUI', 'FreakFrame']

# TODO: move to root folder.
# TODO: save, load


class FreakFrame(Frame):
    name_width = 35
    paid_width = 15
    mp_width = 15
    del_width = 3
    mp_label_color_def = 'SystemButtonFace'
    mp_label_color_pos = 'tomato'
    mp_label_color_neg = 'pale green'
    mp_label_color_0 = 'CadetBlue2'

    def __init__(self, parent=None):
        self.edit_flag = True
        Frame.__init__(self, parent)
        self.__freaks = FreakCore(verbose=True)
        self.__freak_frames = []
        self.create_toolbar()
        self.create_title_frame()
        self.create_total_frame()

    def create_toolbar(self):
        toolbar = Frame(self)
        toolbar.pack(side=TOP, fill=X)
        self.calc_button = Button(toolbar, text='Calculate', cursor='hand2', command=self.calculate, state=DISABLED)
        self.calc_button.pack(side=LEFT)
        Button(toolbar, text='Add freak', cursor='hand2', command=self.add_freak).pack(side=LEFT)
        Button(toolbar, text='Add N freaks', cursor='hand2', command=self.add_n_freaks).pack(side=LEFT)
        Button(toolbar, text='Clear', cursor='hand2', command=self.clear).pack(side=LEFT)
        Button(toolbar, text='Delete all freaks', cursor='hand2', command=self.delete_all_freaks).pack(side=LEFT)
        self.edit_button = Button(toolbar, text='Edit', cursor='hand2', command=self.change_state, state=DISABLED)
        self.edit_button.pack(side=LEFT)
        self.toolbar = toolbar

    def create_title_frame(self):
        frame = Frame(self)
        name = Entry(frame, width=self.name_width)
        name.insert(0, 'Name')
        name['state'] = DISABLED
        name.pack(side=LEFT)
        paid = Entry(frame, width=self.paid_width)
        paid.insert(0, 'Paid')
        paid['state'] = DISABLED
        paid.pack(side=LEFT)
        Label(frame, width=self.mp_width, text='Need to pay', state=DISABLED).pack(side=LEFT)
        Label(frame, width=self.del_width, text='Del', state=DISABLED).pack(side=LEFT)
        frame.pack(side=TOP, anchor=W)

    def create_total_frame(self):
        self.total_frame = Frame(self)
        Label(self.total_frame, text='Each member must pay:').pack(side=LEFT)
        Label(self.total_frame, text='0.0').pack(side=LEFT)

    def add_freak(self, event=None):
        # Need redefine entry input for use with main window's shortcuts
        def read_numbers(event=None):
            # Check for digit and special symbols
            if event.char.isalpha() or event.char in '!@#$%^&*()-=_+/|\\<>,`~':
                return 'break'
            if event.char == '.' and '.' in event.widget.get():
                return 'break'

        def read_symbols(event=None):
            entry = event.widget
            if event.char.isdigit() or event.char.isalpha():
                if entry.selection_present():
                    entry.delete(entry.index(SEL_FIRST), entry.index(SEL_LAST))
                entry.insert(entry.index(INSERT), event.char)
                return 'break'

        if not self.edit_flag:
            return
        frame = Frame(self)
        self.__freaks.add_freak()
        freak_name = self.__freaks[-1].name
        name = Entry(frame, width=self.name_width)
        name.insert(0, freak_name)
        name.bind('<KeyPress>', read_symbols)
        name.pack(side=LEFT)
        paid = Entry(frame, width=self.paid_width)
        paid.insert(0, 0.0)
        paid.bind('<KeyPress>', read_numbers)
        paid.pack(side=LEFT)
        Label(frame, width=self.mp_width, text='N/A', bg=self.mp_label_color_def).pack(side=LEFT)
        Button(frame, text='Del', command=lambda: self.delete_freak(frame), width=self.del_width).pack(side=LEFT)
        frame.pack(side=TOP, anchor=W)
        self.__freak_frames.append(frame)
        if self.calc_button['state'] == DISABLED:
            self.calc_button['state'] = NORMAL

    def add_n_freaks(self, event=None):
        if not self.edit_flag:
            return
        n = askinteger('Enter count of freaks', 'Count of new freaks')
        if n is None:
            return
        elif n <= 0:
            showerror('Error!', 'Count must be positive integer!')
            raise ValueError('Count must be positive integer!')
        elif n > 15:
            showerror('Error!', 'Count too big! Please input value between 1 and 15')
            raise ValueError('Count too big!')
        for count in range(n):
            self.add_freak()
            self.update()

    def delete_freak(self, frame):
        self.__freaks.delete_freak_by_index(self.__freak_frames.index(frame))
        self.__freak_frames.remove(frame)
        frame.pack_forget()
        if not len(self.__freak_frames):
            self.calc_button['state'] = DISABLED
        self.focus_set()

    def delete_last_freak(self, event=None):
        if len(self.__freak_frames):
            self.delete_freak(self.__freak_frames[-1])

    def delete_all_freaks(self, event=None):
        if askyesno('Really delete', 'Are you really want to delete all members?'):
            for frame in self.__freak_frames:
                frame.pack_forget()
            self.__freak_frames = []
            self.__freaks.delete_all_freaks()
            self.calc_button['state'] = DISABLED

    def clear(self, event=None):
        if not self.edit_flag:
            return
        if askyesno('Really clear', 'Are you really want to clear all payment information?'):
            for entry in self.get_pay_entries():
                entry.delete(0, len(entry.get()))
                entry.insert(0, 0.0)
            self.reset_mp_labels_color()

    def get_pay_entries(self):
        return [frame.winfo_children()[1] for frame in self.__freak_frames]

    def get_mp_labels(self):
        return [frame.winfo_children()[2] for frame in self.__freak_frames]

    def reset_mp_labels_color(self):
        for label in self.get_mp_labels():
            label['bg'] = self.mp_label_color_def

    def calculate(self, event=None):
        if not self.edit_flag or not self.__freaks:
            return
        for counter, pay_entry in enumerate(self.get_pay_entries()):
            try:
                freak_balance = float(pay_entry.get())
            except ValueError:
                freak_balance = 0.0
            self.__freaks[counter].set_balance(freak_balance)
        self.__freaks.calculate_payments()
        for freak, mp_label in zip(self.__freaks, self.get_mp_labels()):
            mp_label['text'] = '%.2f' % round(freak.need_to_pay, 2)
            if freak.need_to_pay < 0:
                mp_label['bg'] = self.mp_label_color_neg
            elif freak.need_to_pay > 0:
                mp_label['bg'] = self.mp_label_color_pos
            else:
                mp_label['bg'] = self.mp_label_color_0
        self.change_state()

    def change_state(self, event=None):
        def change_element(element):
            element['state'] = DISABLED if element['state'] == NORMAL else NORMAL

        if event and self.edit_flag:
            return
        if not self.edit_flag:
            self.reset_mp_labels_color()
            self.total_frame.pack_forget()
        else:
            label = self.total_frame.winfo_children()[1]
            label['text'] = round(self.__freaks.each_pay, 2)
            self.total_frame.pack(anchor=W)

        for element in self.toolbar.winfo_children():
            change_element(element)
        for frame in self.__freak_frames:
            for element in frame.winfo_children()[0:2] + [frame.winfo_children()[3]]:
                change_element(element)
        self.edit_flag = not self.edit_flag


class FreakGUI(Tk):
    def __init__(self):
        Tk.__init__(self)
        self.title('Freak Calculator')
        self.resizable(width=False, height=False)
        self.create_menu()
        self.freak_frame = FreakFrame(self)
        self.set_binds()
        self.freak_frame.pack(fill=Y, expand=YES, )
        self.create_footer()

    def create_footer(self):
        toolbar = Frame(self)
        Label(self, text='FreakCalc ver. %s' % __version__).pack(side=RIGHT)
        toolbar.pack(side=BOTTOM, fill=X)

    def set_binds(self):
        unset_control_binds = ['a', 'A', 'c', 'C', 'e', 'E', 'd', 'D']
        for bind in unset_control_binds:
            self.bind('<Control-%s>' % bind, lambda event: None)
        self.bind('a', self.freak_frame.add_freak)
        self.bind('A', self.freak_frame.add_n_freaks)
        self.bind('c', self.freak_frame.calculate)
        self.bind('C', self.freak_frame.clear)
        self.bind('e', self.freak_frame.change_state)
        self.bind('d', self.freak_frame.delete_last_freak)
        self.bind('D', self.freak_frame.delete_all_freaks)
        self.bind('<Return>', lambda event: self.focus_set())
        self.bind('<Escape>', lambda event: self.focus_set())
        self.bind('<Shift-Escape>', lambda event: self.quit())

    def create_menu(self):
        self.menu = Menu(self)
        self.config(menu=self.menu)
        self.create_menu_file()
        self.create_menu_about()

    def create_menu_file(self):
        menu = Menu(self.menu, tearoff=False)
        menu.add_command(label='Save', command=self.not_ready)
        menu.add_command(label='Save as...', command=self.not_ready)
        menu.add_command(label='Load', command=self.not_ready)
        menu.add_separator()
        menu.add_command(label='Exit', command=self.quit)
        self.menu.add_cascade(label='File', underline=0, menu=menu)

    def create_menu_about(self):
        menu = Menu(self.menu, tearoff=False)
        menu.add_command(label='Help', command=self.show_help)
        menu.add_command(label='Shortcuts', command=self.show_shortcuts)
        menu.add_separator()
        menu.add_command(label='About', command=self.show_about)
        self.menu.add_cascade(label='About', underline=0, menu=menu)

    def not_ready(self):
        print('Not ready')

    def show_help(self):
        text = '''
        How to use Freak Calculator:
         - press 'Add freak' for add new member;
         - set his name and pay-value;
         - repeat it for all you party-members;
         - press calculate and watch result;
         - if you need change something - press 'Edit'

        Press 'Clean' for reset all pays.
        Press 'Delete all freaks' for delete all members.
        Press 'Add N freaks' for add few members at same time.
        '''
        showinfo('FreakCalc version %s' % __version__, text)

    def show_shortcuts(self):
        text = '''
        Shortcuts:
         • a - add freak
         • Shift+a - add N freaks
         • Shift+c - clear
         • c - calculate
         • e - edit (working after calculate)
         • d - delete last freak
         • Shift+d - delete all freaks
         • Shift+<Escape> - close app
        '''
        showinfo('FreakCalc shortcuts', text)

    def show_about(self):
        text = 'FreakCalc ver. %s.\nApp for calculating party payments.\n2017.' % __version__
        showinfo('About FreakCalc', text)


if __name__ == '__main__':
    t = FreakGUI()
    t.mainloop()

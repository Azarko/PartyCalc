"""
Party Calc GUI.
App for calculate party payments.
"""

__author__ = 'Boris Polyanskiy'

import csv
import os
import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
from tkinter import simpledialog
import typing

import party_calc
from party_calc import calculator


class CalculatorFrame(tk.Frame):
    name_width = 35
    paid_width = 15
    mp_width = 15
    del_width = 3
    mp_label_color_def = 'SystemButtonFace'
    mp_label_color_pos = 'tomato'
    mp_label_color_neg = 'pale green'
    mp_label_color_0 = 'CadetBlue2'
    max_persons_count = 15

    def __init__(self, parent=None):
        super().__init__(parent)

        self.calculator = calculator.PartyCalculator()
        self._person_frames = []
        self.edit_mode_flag = True

        # create base elements of frame
        self.create_toolbar_frame()
        self.create_title_frame()
        self.create_total_frame()

    def create_title_frame(self) -> None:
        """Create header of the persons table"""
        frame = tk.Frame(self)
        name = tk.Entry(frame, width=self.name_width)
        name.insert(0, 'Name')
        name['state'] = tk.DISABLED
        name.pack(side=tk.LEFT)
        paid = tk.Entry(frame, width=self.paid_width)
        paid.insert(0, 'Paid')
        paid['state'] = tk.DISABLED
        paid.pack(side=tk.LEFT)
        tk.Label(frame, width=self.mp_width, text='Need to pay', state=tk.DISABLED).pack(side=tk.LEFT)
        tk.Label(frame, width=self.del_width, text='Del', state=tk.DISABLED).pack(side=tk.LEFT)
        frame.pack(side=tk.TOP, anchor=tk.W)

    def create_toolbar_frame(self) -> None:
        """Create the control toolbar on the top of the frame"""
        self.toolbar = tk.Frame(self)
        self.calc_button = tk.Button(self.toolbar, text='Calculate', cursor='hand2', command=self.calculate,
                                     state=tk.DISABLED)
        self.calc_button.pack(side=tk.LEFT)
        tk.Button(self.toolbar, text='Add person', cursor='hand2', command=self.add_person).pack(side=tk.LEFT)
        tk.Button(self.toolbar, text='Add N persons', cursor='hand2', command=self.add_n_persons).pack(side=tk.LEFT)
        tk.Button(self.toolbar, text='Clear', cursor='hand2', command=self.reset_payments).pack(side=tk.LEFT)
        tk.Button(self.toolbar, text='Reset all', cursor='hand2', command=self.reset).pack(side=tk.LEFT)
        self.edit_button = tk.Button(self.toolbar, text='Edit', cursor='hand2', command=self.switch_edit_mode,
                                     state=tk.DISABLED)
        self.edit_button.pack(side=tk.LEFT)
        self.toolbar.pack(side=tk.TOP, fill=tk.X)

    def create_total_frame(self):
        """Create summary frame with results of calculation"""
        self.total_frame = tk.Frame(self)
        tk.Label(self.total_frame, text='Each member must pay:').pack(side=tk.LEFT)
        tk.Label(self.total_frame, text='0.0').pack(side=tk.LEFT)

    def _check_persons_limit(self, show_info=True) -> bool:
        """Check if max_persons_count limit is reached

        If limit is reached - show warning (showinfo).

        :return: True if limit reached, else False
        """
        if len(self._person_frames) >= self.max_persons_count:
            if show_info:
                messagebox.showinfo(
                    'Persons limit',
                    f'Max count of persons ({self.max_persons_count}) is reached! Cannot add more!'
                )
            return True
        return False

    def add_person(self, name=None, balance=0.0) -> None:
        """Create and display new person"""

        def validate_float(string: str) -> bool:
            """Check if specified string can be converted to float

            :param string: string
            :return: True if validation passed else False
            """
            if string:
                try:
                    float(string)
                except ValueError:
                    return False
            return True

        if self._check_persons_limit():
            return
        person_name = name if name is not None else self.calculator.select_person_name()
        try:
            self.calculator.add_person(name=person_name, balance=balance)
        except ValueError as err:
            messagebox.showerror('Error', err)
            return
        frame = tk.Frame(self)

        name_var = tk.StringVar(value=person_name)
        name = tk.Entry(frame, width=self.name_width, textvariable=name_var)
        name.bind("<FocusOut>", lambda x: self.edit_name_callback(name_var, frame))
        name.bind("<Return>", lambda x: self.focus())
        name.pack(side=tk.LEFT)

        paid = tk.Entry(frame, width=self.paid_width, validate="key")
        paid.config(validatecommand=(paid.register(validate_float), "%P"))
        paid.insert(0, balance)
        paid.pack(side=tk.LEFT)

        tk.Label(frame, width=self.mp_width, text='N/A', bg=self.mp_label_color_def).pack(side=tk.LEFT)
        tk.Button(frame, text='Del', command=lambda: self.delete_person(frame), width=self.del_width).pack(side=tk.LEFT)
        frame.pack(side=tk.TOP, anchor=tk.W)
        self._person_frames.append(frame)
        self.calc_button['state'] = tk.NORMAL

    def edit_name_callback(self, string_var: tk.StringVar, frame: tk.Frame) -> None:
        """Callback for change person name (Entry)

        :param string_var: StringVar of Entry
        :param frame: parent frame
        :return: None
        """
        person_name = self.calculator.persons[self._person_frames.index(frame)].name
        try:
            self.calculator.change_person_name(person_name, string_var.get())
        except ValueError as err:
            messagebox.showerror('Error', err)
            string_var.set(person_name)

    def add_n_persons(self) -> None:
        """Create and display few persons"""
        if self._check_persons_limit():
            return
        available_count = self.max_persons_count - len(self._person_frames)
        if available_count == 1:
            messagebox.showinfo('Persons limit', 'Only one person is added')
            self.add_person()
            self.update()
            return
        available_str = f'1-{available_count}' if available_count > 1 else '1'
        n = simpledialog.askinteger('Enter count of persons', f'Count of new persons ({available_str})')
        if n is None:
            return
        elif n <= 0:
            messagebox.showerror('Error!', 'Count must be positive integer!')
            return
        elif n > self.max_persons_count:
            messagebox.showerror('Error!', f'Count too big! Please input value between 1 and {self.max_persons_count}')
            return
        if len(self._person_frames) + n > self.max_persons_count:
            n = available_count
            messagebox.showinfo(
                'Persons limit', f'Max count of persons is {self.max_persons_count}, {n} members will be added',
            )
        for count in range(n):
            self.add_person()
            self.update()

    def delete_person(self, frame) -> None:
        """Delete person and linked frame"""
        self.calculator.delete_person(self.calculator[self._person_frames.index(frame)].name)
        self._person_frames.remove(frame)
        frame.pack_forget()
        if not len(self._person_frames):
            self.calc_button['state'] = tk.DISABLED
        self.focus_set()

    def reset(self) -> None:
        """Reset all data"""
        if messagebox.askyesno('Really reset', 'Do you really want to reset all data?'):
            self.calculator.reset()
            for frame in self._person_frames:
                frame.pack_forget()
            self._person_frames = []
            self.calc_button['state'] = tk.DISABLED

    def reset_payments(self) -> None:
        """Reset payments data"""
        if messagebox.askyesno('Really reset', 'Do you really want to reset all payment information?'):
            for entry in self.get_pay_entries():
                entry.delete(0, len(entry.get()))
                entry.insert(0, 0.0)
            self.reset_mp_labels_color()

    def get_pay_entries(self) -> typing.List[tk.Entry]:
        """Return "paid" entries of all person frames"""
        return [frame.winfo_children()[1] for frame in self._person_frames]

    def get_mp_labels(self) -> typing.List[tk.Label]:
        """Return "must pay" entries of all person frames"""
        return [frame.winfo_children()[2] for frame in self._person_frames]

    def reset_mp_labels_color(self) -> None:
        """Reset color of "must pay" entries of all person frames"""
        for label in self.get_mp_labels():
            label['bg'] = self.mp_label_color_def

    def update_calculator(self) -> None:
        """Take data by pay entries and update paid info in PartyCalculator instance"""
        for counter, pay_entry in enumerate(self.get_pay_entries()):
            try:
                person_balance = float(pay_entry.get())
            except ValueError:
                person_balance = 0.0
            self.calculator.set_person_balance(self.calculator[counter].name, person_balance)

    def calculate(self) -> None:
        """Calculate "must pay" for all persons"""
        self.update_calculator()
        self.calculator.calculate_payments()
        for person, mp_label in zip(self.calculator, self.get_mp_labels()):
            mp_label['text'] = '%.2f' % round(person.need_to_pay, 2)
            if person.need_to_pay < 0:
                mp_label['bg'] = self.mp_label_color_neg
            elif person.need_to_pay > 0:
                mp_label['bg'] = self.mp_label_color_pos
            else:
                mp_label['bg'] = self.mp_label_color_0
        self.switch_edit_mode()

    def switch_edit_mode(self) -> None:
        """Event handler to switch state of frame to enabled/disabled (edit/readonly mode)"""
        def change_element(element):
            element['state'] = tk.DISABLED if element['state'] == tk.NORMAL else tk.NORMAL

        if not self.edit_mode_flag:
            self.reset_mp_labels_color()
            self.total_frame.pack_forget()
        else:
            label = self.total_frame.winfo_children()[1]
            label['text'] = round(self.calculator.each_pay, 2)
            self.total_frame.pack(anchor=tk.W)

        for element in self.toolbar.winfo_children():
            change_element(element)
        for frame in self._person_frames:
            for element in frame.winfo_children()[0:2] + [frame.winfo_children()[3]]:
                change_element(element)
        self.edit_mode_flag = not self.edit_mode_flag

    def save_csv(self):
        """Save persons data to selected csv file"""
        file_name = filedialog.asksaveasfilename(defaultextension='.csv', filetype=(('CSV files', '*.csv'),),
                                      initialdir=os.getcwd())

        if file_name:
            self.update_calculator()
            with open(file_name, mode='w', encoding='utf-8', newline='') as stream:
                writer = csv.writer(stream)
                writer.writerow(('person', 'balance'))
                writer.writerows(self.calculator.to_list())

    def load_csv(self):
        """Load persons data from selected csv file"""
        stream = filedialog.askopenfile(filetype=(('CSV files', '*.csv'),), initialdir=os.getcwd())
        if stream:
            reader = csv.reader(stream)
            data = [*reader]
            if data and len(data[0]) == 2 and data[0][1] == 'balance':
                # skip header
                data = data[1:]
            for counter, row in enumerate(data):
                if len(row) != 2:
                    continue
                if self._check_persons_limit(show_info=False):
                    messagebox.showinfo(
                        'Persons limit',
                        f'Stop importing at line {counter + 1}: persons limit ({self.max_persons_count}) is reached\n'
                        f'{len(data) - counter} line(s) ignored'
                    )
                    break
                self.add_person(name=row[0], balance=row[1])


class CalculatorGUI(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self.menu = None
        self.title('Party Calculator')
        self.resizable(width=False, height=False)
        self.calculator_frame = CalculatorFrame(self)
        self.create_menu()
        self.calculator_frame.pack(fill=tk.Y, expand=tk.YES)
        self.create_footer()

    def create_footer(self):
        toolbar = tk.Frame(self)
        tk.Label(self, text='party_calc ver. %s' % party_calc.__version__).pack(side=tk.RIGHT)
        toolbar.pack(side=tk.BOTTOM, fill=tk.X)

    def create_menu(self):
        self.menu = tk.Menu(self)
        self.config(menu=self.menu)
        self.create_menu_file()
        self.create_menu_about()

    def create_menu_file(self):
        menu = tk.Menu(self.menu, tearoff=False)
        menu.add_command(label='Export csv', command=self.calculator_frame.save_csv)
        menu.add_command(label='Import csv', command=self.calculator_frame.load_csv)
        menu.add_separator()
        menu.add_command(label='Exit', command=self.quit)
        self.menu.add_cascade(label='File', underline=0, menu=menu)

    def create_menu_about(self):
        menu = tk.Menu(self.menu, tearoff=False)
        menu.add_command(label='Help', command=self.show_help)
        menu.add_separator()
        menu.add_command(label='About', command=self.show_about)
        self.menu.add_cascade(label='About', underline=0, menu=menu)

    @staticmethod
    def show_help():
        text = '''
        How to use Party Calculator:
         - press 'Add person' for add new member;
         - set his/her name and pay-value;
         - repeat it for all you party-members;
         - press calculate and watch result;
         - if you need change something - press 'Edit'

        Press 'Clear' for reset all pays.
        Press 'Reset all' for delete all members.
        Press 'Add N persons' for add few members at same time.
        '''
        messagebox.showinfo('party_calc version %s' % party_calc.__version__, text)

    @staticmethod
    def show_about():
        text = 'party_calc ver. %s.\nApp for calculating party payments.' % party_calc.__version__
        messagebox.showinfo('About party_calc', text)


def run():
    CalculatorGUI().mainloop()


if __name__ == '__main__':
    run()

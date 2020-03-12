import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

from db_core import DataBase


class MainWindow(tk.Frame):

    def __init__(self):
        super().__init__(main_window)
        self.column_names = ("Nickname", "Battles", "Wins", "Tanks", "Ban?", "Tester?", "Motto", "Clan")
        self.columns = dict(zip(db.fields, self.column_names))

        self.add_record = tk.PhotoImage(file="add_record.png")
        self.edit_record = tk.PhotoImage(file="edit_record.png")
        self.delete_record = tk.PhotoImage(file="delete_record.png")
        self.find_record = tk.PhotoImage(file="find_record.png")
        self.create_db = tk.PhotoImage(file="create_db.png")
        self.save_db = tk.PhotoImage(file="save_db.png")
        self.delete_db = tk.PhotoImage(file="delete_db.png")
        self.export_db = tk.PhotoImage(file="export_db.png")
        self.to_backup = tk.PhotoImage(file="to_backup.png")
        self.from_backup = tk.PhotoImage(file="from_backup.png")

        self.records_list = ttk.Treeview(self,
                                         columns=db.fields,
                                         height=100,
                                         show="headings")

        self.records_list.bind('<Button>', self.handle_click)

        self.init_buttons()
        self.view_records_list()

    def handle_click(self, event):
        if self.records_list.identify_region(event.x, event.y) == "separator":
            return "break"

    def init_buttons(self):
        buttons_bar = tk.Frame(bg='#FFFFFF', bd=2)
        buttons_bar.pack(side=tk.TOP, fill=tk.X)

        btn_add_record = tk.Button(buttons_bar,
                                   text='Add',
                                   command=self.add_record_to_DB,
                                   bg='#FFFFFF',
                                   compound=tk.TOP,
                                   image=self.add_record)
        btn_edit_record = tk.Button(buttons_bar,
                                    text='Edit',
                                    command=self.edit_record_in_DB,
                                    bg='#FFFFFF',
                                    compound=tk.TOP,
                                    image=self.edit_record)
        btn_delete_record = tk.Button(buttons_bar,
                                      text='Delete',
                                      command=self.delete_records_from_db,
                                      bg='#FFFFFF',
                                      compound=tk.TOP,
                                      image=self.delete_record)
        btn_find_record = tk.Button(buttons_bar,
                                    text='Find',
                                    command=self.search_file_in_DB,
                                    bg='#FFFFFF',
                                    compound=tk.TOP,
                                    image=self.find_record)
        btn_create_db = tk.Button(buttons_bar,
                                  text='Create DB',
                                  command=self.create_data_base,
                                  bg='#FFFFFF',
                                  compound=tk.TOP,
                                  image=self.create_db)
        btn_save_db = tk.Button(buttons_bar,
                                text='Save DB',
                                command=self.save_records_in_db,
                                bg='#FFFFFF',
                                compound=tk.TOP,
                                image=self.save_db)
        btn_delete_db = tk.Button(buttons_bar,
                                  text='Delete DB',
                                  command=self.delete_database,
                                  bg='#FFFFFF',
                                  compound=tk.TOP,
                                  image=self.delete_db)
        btn_from_backup = tk.Button(buttons_bar,
                                    text='Recover DB',
                                    command=self.recover_data_from_backup,
                                    bg='#FFFFFF',
                                    compound=tk.TOP,
                                    image=self.from_backup)
        btn_to_backup = tk.Button(buttons_bar,
                                  text='Backup DB',
                                  command=self.write_data_to_backup,
                                  bg='#FFFFFF',
                                  compound=tk.TOP,
                                  image=self.to_backup)
        btn_export_db = tk.Button(buttons_bar,
                                  text='Export DB',
                                  command=self.export_DB_to_CSV,
                                  bg='#FFFFFF',
                                  compound=tk.TOP,
                                  image=self.export_db)

        btn_add_record.pack(side=tk.LEFT)
        btn_edit_record.pack(side=tk.LEFT)
        btn_delete_record.pack(side=tk.LEFT)
        btn_find_record.pack(side=tk.LEFT)

        btn_from_backup.pack(side=tk.RIGHT)
        btn_to_backup.pack(side=tk.RIGHT)
        btn_save_db.pack(side=tk.RIGHT)
        btn_export_db.pack(side=tk.RIGHT)
        btn_delete_db.pack(side=tk.RIGHT)
        btn_create_db.pack(side=tk.RIGHT)

        for field in db.fields:
            self.records_list.column(field, anchor=tk.CENTER, width=125)
            self.records_list.heading(field, text=self.columns[field])

        self.records_list.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    def view_records_list(self):
        for record in self.records_list.get_children():
            self.records_list.delete(record)
        for record in db.records_dict:
            self.records_list.insert('', 'end', values=list(db.records_dict[record].values()))

    def delete_records_from_db(self):
        selected_records = self.records_list.selection()
        for record in selected_records:
            db.delete_record((self.records_list.set(record))['nickname'])
        self.view_records_list()

    def save_records_in_db(self):
        db.write_database_to_file()

    def write_data_to_backup(self):
        db.create_backup_of_database()

    def recover_data_from_backup(self):
        db.recover_database_from_backup()
        self.view_records_list()

    def create_data_base(self):
        self.delete_database()
        db.create_or_read_file()
        self.view_records_list()

    def delete_database(self):
        db.delete_database_file()
        self.view_records_list()

    def add_record_to_DB(self):
        AddRecordWindow()

    def edit_record_in_DB(self):
        if self.records_list.selection():
            EditRecordWindow(self.records_list.set(self.records_list.selection()[0]))

    def search_file_in_DB(self):
        SearchRecordWindow()

    def export_DB_to_CSV(self):
        db.export_to_csv()


class AddRecordWindow(tk.Toplevel):
    def __init__(self):
        super().__init__(main_window)

        self.entry_nickname = ttk.Entry(self)
        self.entry_battles = ttk.Entry(self)
        self.entry_wins = ttk.Entry(self)
        self.entry_tanks = ttk.Entry(self)
        self.entry_ban = ttk.Entry(self)
        self.entry_tester = ttk.Entry(self)
        self.entry_motto = ttk.Entry(self)
        self.entry_clan = ttk.Entry(self)

        self.button_add = ttk.Button(self, text="Add")
        self.button_cancel = ttk.Button(self, text="Close", command=self.destroy)

        self.in_main_window = application
        self.init_window_entities()

    def init_window_entities(self):
        self.title("Adding record to DB")
        self.geometry('360x300+400+300')
        self.resizable(False, False)

        label_nickname = tk.Label(self, text="Nickname")
        label_nickname.place(x=10, y=20)
        label_battles = tk.Label(self, text="Battles")
        label_battles.place(x=10, y=50)
        label_wins = tk.Label(self, text="Wins")
        label_wins.place(x=10, y=80)
        label_tanks = tk.Label(self, text="Tanks")
        label_tanks.place(x=10, y=110)
        label_ban = tk.Label(self, text="Ban")
        label_ban.place(x=10, y=140)
        label_tester = tk.Label(self, text="Tester")
        label_tester.place(x=10, y=170)
        label_motto = tk.Label(self, text="Motto")
        label_motto.place(x=10, y=200)
        label_clan = tk.Label(self, text="Clan")
        label_clan.place(x=10, y=230)

        self.entry_nickname.place(x=150, y=20)
        self.entry_battles.place(x=150, y=50)
        self.entry_wins.place(x=150, y=80)
        self.entry_tanks.place(x=150, y=110)
        self.entry_ban.place(x=150, y=140)
        self.entry_tester.place(x=150, y=170)
        self.entry_motto.place(x=150, y=200)
        self.entry_clan.place(x=150, y=230)

        self.button_add.place(x=65, y=270)
        self.button_add.bind('<Button-1>',
                             lambda event: self.adding_record(self.entry_nickname.get(),
                                                              self.entry_battles.get(),
                                                              self.entry_wins.get(),
                                                              self.entry_tanks.get(),
                                                              self.entry_ban.get(),
                                                              self.entry_tester.get(),
                                                              self.entry_motto.get(),
                                                              self.entry_clan.get()))

        self.button_cancel.place(x=200, y=270)

    def adding_record(self, *fields_list):
        adding_dict = dict()
        for (key, value) in zip(db.fields, fields_list):
            if value:
                adding_dict[key] = value
        handler_answer = db.add_record(adding_dict)
        if handler_answer[0]:
            messagebox.showinfo("Done", handler_answer[1])
        else:
            messagebox.showerror("Error!", handler_answer[1])
        self.in_main_window.view_records_list()


class EditRecordWindow(AddRecordWindow):
    def __init__(self, selection):
        super().__init__()
        self.button_add.destroy()
        self.button_edit = ttk.Button(self, text="Edit")
        self.in_main_window = application
        self.selection = selection

        self.entry_nickname.insert(0, self.selection['nickname'])
        self.entry_battles.insert(0, self.selection['battles_amount'])
        self.entry_wins.insert(0, self.selection['wins_amount'])
        self.entry_tanks.insert(0, self.selection['tanks_amount'])
        self.entry_ban.insert(0, self.selection['is_banned'])
        self.entry_tester.insert(0, self.selection['is_tester'])
        self.entry_motto.insert(0, self.selection['motto'])
        self.entry_clan.insert(0, self.selection['clan_name'])

        self.init_edit_window_entities()

    def init_edit_window_entities(self):
        self.title("Record editing")

        self.button_edit.place(x=65, y=270)
        self.button_edit.bind('<Button-1>',
                              lambda event: self.editing_record(self.entry_nickname.get(),
                                                                self.entry_battles.get(),
                                                                self.entry_wins.get(),
                                                                self.entry_tanks.get(),
                                                                self.entry_ban.get(),
                                                                self.entry_tester.get(),
                                                                self.entry_motto.get(),
                                                                self.entry_clan.get()))

    def editing_record(self, *fields_list):
        editing_dict = dict()
        for (key, value) in zip(db.fields, fields_list):
            if value:
                editing_dict[key] = value
        handler_answer = db.edit_record(self.selection['nickname'], editing_dict)
        if handler_answer[0]:
            messagebox.showinfo("Done", handler_answer[1])
        else:
            messagebox.showerror("Error!", handler_answer[1])
        self.in_main_window.view_records_list()


class SearchRecordWindow(AddRecordWindow):
    def __init__(self):
        super().__init__()
        self.button_add.destroy()
        self.button_search = ttk.Button(self, text="Search")
        self.in_main_window = application
        self.init_edit_window_entities()

    def init_edit_window_entities(self):
        self.title("Finding record")

        self.button_search.place(x=65, y=270)
        self.button_search.bind('<Button-1>',
                                lambda event: self.search_record(self.entry_nickname.get(),
                                                                 self.entry_battles.get(),
                                                                 self.entry_wins.get(),
                                                                 self.entry_tanks.get(),
                                                                 self.entry_ban.get(),
                                                                 self.entry_tester.get(),
                                                                 self.entry_motto.get(),
                                                                 self.entry_clan.get()))

    def search_record(self, *fields_list):
        searching_dict = dict()
        for (key, value) in zip(db.fields, fields_list):
            if value:
                searching_dict[key] = value
        handler_answer = db.search_record(searching_dict)

        if handler_answer[0]:
            if isinstance(handler_answer[1], set):
                messagebox.showinfo("Done", "{} records".format(len(handler_answer[1])))
            else:
                messagebox.showinfo("Done", handler_answer[1])
        else:
            messagebox.showerror("Error!", handler_answer[1])

        if isinstance(handler_answer[1], set):
            SearchResultsWindow(handler_answer[1])


class SearchResultsWindow(tk.Toplevel):
    def __init__(self, results):
        super().__init__()
        self.results = results
        self.column_names = ("Nickname", "Battles", "Wins", "Tanks", "Ban?", "Tester?", "Motto", "Clan")
        self.columns = dict(zip(db.fields, self.column_names))
        self.records_list = ttk.Treeview(self,
                                         columns=db.fields,
                                         height=20,
                                         show="headings")
        self.records_list.bind('<Button>', self.handle_click)
        for field in db.fields:
            self.records_list.column(field, width=100, anchor=tk.CENTER)
            self.records_list.heading(field, text=self.columns[field])
        self.records_list.pack()

        self.view_records_list()

        self.title("Results of searching")
        self.geometry('800x180+400+300')
        self.resizable(False, False)

    def handle_click(self, event):
        if self.records_list.identify_region(event.x, event.y) == "separator":
            return "break"

    def view_records_list(self):
        for record in self.records_list.get_children():
            self.records_list.delete(record)
        for record in self.results:
            self.records_list.insert('', 'end', values=list(db.records_dict[record].values()))


if __name__ == "__main__":
    db = DataBase()
    main_window = tk.Tk()
    application = MainWindow()
    application.pack()
    main_window.title("WoT Blitz Players Server Stats")
    main_window.geometry("1000x400+300+200")
    main_window.resizable(False, False)
    main_window.mainloop()

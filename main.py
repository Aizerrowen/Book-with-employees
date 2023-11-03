import tkinter as tk
from tkinter import ttk, simpledialog, messagebox
import sqlite3

class Main(tk.Frame):
    def __init__(self, root):
        super().__init__(root)
        self.init_main()
        self.db=db
        self.view_records()
        self.conn = sqlite3.connect('db.db')

    def init_main(self):
        toolbar=tk.Frame(bg='#d7d8e0', bd=2)
        toolbar.pack(side=tk.TOP, fill=tk.X)
        self.add_img=tk.PhotoImage(file='./img/add.png')
        btn_add_employee = tk.Button(toolbar, bg='#d7d8e0', bd=0, image=self.add_img, command=self.add_employee)
        btn_add_employee.pack(side=tk.LEFT)
        self.delete_img=tk.PhotoImage(file='./img/delete.png')
        btn_delete = tk.Button(toolbar, bg='#d7d8e0', bd=0, image=self.delete_img, command=self.delete_employee)
        btn_delete.pack(side=tk.LEFT)
        self.search_img=tk.PhotoImage(file='./img/search.png')
        btn_search = tk.Button(toolbar, bg='#d7d8e0', bd=0, image=self.search_img, command=self.search_employee)
        btn_search.pack(side=tk.LEFT)
        self.update_img=tk.PhotoImage(file='./img/update.png')
        btn_update = tk.Button(toolbar, bg='#d7d8e0', bd=0, image=self.update_img, command=self.update_employee)
        btn_update.pack(side=tk.LEFT)

        self.tree=ttk.Treeview(self, columns=('ID', 'Name', 'Number', 'Email', 'Salary' ),height=45, show='headings')
        self.tree.column("ID", width=30, anchor=tk.CENTER)
        self.tree.column("Name", width=250, anchor=tk.CENTER)
        self.tree.column("Number", width=60, anchor=tk.CENTER)
        self.tree.column("Email", width=100, anchor=tk.CENTER)
        self.tree.column("Salary", width=60, anchor=tk.CENTER)

        self.tree.heading("ID", text="ID")
        self.tree.heading("Name", text="Name")
        self.tree.heading("Number", text="Telefon Number")
        self.tree.heading("Email", text="Email")
        self.tree.heading("Salary", text="Salary")

        self.tree.pack(side=tk.LEFT)

    def add_employee(self):
        name = simpledialog.askstring("Input", "Enter employee name:")
        phone = simpledialog.askstring("Input", "Enter employee phone:")
        email = simpledialog.askstring("Input", "Enter employee email:")
        salary = simpledialog.askinteger("Input", "Enter employee salary:")

        cursor = self.conn.cursor()
        cursor.execute("INSERT INTO db (Name, TelefonNumber, Email, Salary) VALUES (?, ?, ?, ?)", (name, phone, email, salary))
        self.conn.commit()
        self.view_records()

    def delete_employee(self):
        
        label_ID = simpledialog.askinteger("Input", "Enter employee ID:")
        self.conn.execute("DELETE FROM db WHERE id=?", (label_ID,))
        self.conn.commit()
        self.view_records()

    def search_employee(self):
        name = simpledialog.askstring("Input", "Enter employee name:")

        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM db WHERE name=?", (name,))
        employees = cursor.fetchall()

        if employees:
            self.tree.delete(*self.tree.get_children())
            for employee in employees:
                self.tree.insert("", "end", values=employee)
        else:
            messagebox.showinfo("Info", "No employee found with the given name.")

    def update_employee(self):
        emp_id = simpledialog.askinteger("Input", "Enter employee ID:")

        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM db WHERE id=?", (emp_id,))
        employee = cursor.fetchone()

        if employee:
            name = simpledialog.askstring("Input", "Новое имя сотрудника:", initialvalue=employee[1])
            phone = simpledialog.askstring("Input", "Новый телефонный номер:", initialvalue=employee[2])
            email = simpledialog.askstring("Input", "Новый email:", initialvalue=employee[3])
            salary = simpledialog.askinteger("Input", "Новая зарплата сотрудника:", initialvalue=employee[4])

            cursor.execute("UPDATE db SET Name=?, TelefonNumber=?, Email=?, Salary=? WHERE id=?", (name, phone, email, salary, emp_id))
            self.conn.commit()
            self.view_records()
        else:
            messagebox.showerror("Error", "Сотрудник не найден")

    def records(self, Name, TelefonNumber, Email, Salary):
        self.db.insert_data(Name, TelefonNumber, Email, Salary)

    def view_records(self):
        self.db.cur.execute('SELECT * FROM db')

        [self.tree.delete(i) for i in self.tree.get_children()]

        [self.tree.insert('', 'end', values=row) for row in self.db.cur.fetchall()]

class data_base:
    def __init__(self):
        self.conn=sqlite3.connect('db.db')
        self.cur=self.conn.cursor()
        self.cur.execute(
            '''CREATE TABLE IF NOT EXISTS db (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                Name TEXT,
                TelefonNumber TEXT,
                Email TEXT,
                Salary INTEGER
                )'''
        )
        self.conn.commit()

    def insert_data(self, name, number, email, salary):
        self.cur.execute(
            'INSERT INTO db (Name, TelefonNumber, Email, Salary) VALUES (?, ?, ?, ?)', (name, number, email, salary)
        )
        self.conn.commit()    


if __name__ == '__main__':
    root = tk.Tk()
    db=data_base()
    app = Main(root)
    app.pack()
    root.title("Список рабочих")
    root.geometry('665x450')
    root.resizable(False, False)
    root.mainloop()
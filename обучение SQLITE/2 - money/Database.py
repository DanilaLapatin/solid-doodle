import sqlite3
import tkinter
from tkinter import *
from tkinter import messagebox
from tkinter import ttk

selected_tuple = None

class DB:
    def __init__(self):
        self.conn = sqlite3.connect("mybooks.db")
        self.cur = self.conn.cursor()
        self.cur.execute("CREATE TABLE IF NOT EXISTS buy (id INTEGER PRIMARY KEY, product TEXT, price TEXT, comment TEXT, date TEXT, category TEXT)")
        self.conn.commit()


    def __del__(self):
        self.conn.close()


    def view(self):
        self.cur.execute("SELECT * FROM buy")
        rows = self.cur.fetchall()
        return rows

    def insert(self, product, price, comment, date, category):
        self.cur.execute("INSERT INTO buy VALUES (NULL,?,?,?,?,?)", (product, price, comment, date, category))
        self.conn.commit()

    def update(self, id, product, price, comment, date, category):
        self.cur.execute("UPDATE buy SET product=?, price=?, comment=?, date=?, category=? WHERE id=?", (product, price, comment, date, category, id,))
        self.conn.commit()

    def delete(self, id):
        self.cur.execute("DELETE FROM buy WHERE id=?", (id,))
        self.conn.commit()


    def search(self, product = "", price = "", comment = "", date = "", category = ""):
        self.cur.execute("""SELECT * FROM buy 
                                WHERE product=? 
                                OR price=?
                                OR comment=?
                                OR date=?
                                OR category=?
                                GROUP BY product,price,comment,date,category """ , (product,price, comment, date, category))

        rows = self.cur.fetchall()
        return rows

#------------------------------------------------------------------------------
#Класс оконного приложения(внешний вид и часть логики приложения)
class Application:
    @staticmethod
    def copypaste(event):
        if event.keycode == 86 and event.keysym != 'v':
            event.widget.event_generate('<<Paste>>')
        elif event.keycode == 67 and event.keysym != 'c':
            event.widget.event_generate('<<Copy>>')
        elif event.keycode == 88 and event.keysym != 'x':
            event.widget.event_generate('<<Cut>>')


    def get_selected_row(self,event):
        global selected_tuple
        if event.widget == self.table and len(self.table.selection()) != 0:
            print("Длина выбранного",len(self.table.selection()))
            index = self.table.selection()[0]
            selected_tuple = tuple(self.table.item(index)["values"])
            print(selected_tuple, index)


    def __init__(self):

        self.db = DB()

        self.window = Tk()
        self.window.title("Бюджет 0.1")
        self.window.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.columns = {
            "Id":"Номер",
            "name":"Название",
            "price":"Стоимость",
            "comment":"Комментарий",
            "date":"Дата",
            "category":"Категория"
        }
        self.categories = ["Питание", "ЖКХ", "Одежда", "Техника", "Детское", "Уход за собой"]

        self.table = ttk.Treeview(self.window,columns=tuple(self.columns.keys()), show="headings")
        self.table.grid(row=2, column=0, rowspan=6, columnspan=2, padx = 10, pady = 10)
        for col in self.columns.keys():
            self.table.heading(col, text=self.columns[col])

        self.l1 = Label(self.window, text="Сумма")
        self.l1.grid(row=10, column=0, pady=(10,0), padx = 10,sticky=tkinter.W)

        self.sum_text = StringVar()
        self.e_sum = Entry(self.window, textvariable=self.sum_text,)
        self.e_sum.grid(row=11, column=0, pady=(0,10), padx = 10, sticky=tkinter.W)

        self.sb1 = Scrollbar(self.window)
        self.sb1.grid(row=2, column=2, rowspan=6)

        self.table.configure(yscrollcommand=self.sb1.set)
        self.sb1.configure(command=self.table.yview)

        self.table.bind('<<TreeviewSelect>>', self.get_selected_row)
        self.window.bind('<Control-Key>', self.copypaste)

        self.b1 = Button(self.window, text="Посмотреть все", width=12, command= self.view_command)
        self.b1.grid(row=2, column=3, padx = (0,10))  # size of the button

        self.b2 = Button(self.window, text="Поиск", width=12, command= self.search_window_command)
        self.b2.grid(row=3, column=3, padx = (0,10))

        self.b3 = Button(self.window, text="Добавить", width=12, command= self.add_window_command)
        self.b3.grid(row=4, column=3, padx = (0,10))

        self.b4 = Button(self.window, text="Обновить", width=12, command= self.update_window_command)
        self.b4.grid(row=5, column=3, padx = (0,10))

        self.b5 = Button(self.window, text="Удалить", width=12, command= self.delete_command)
        self.b5.grid(row=6, column=3, padx = (0,10))

        self.b6 = Button(self.window, text="Закрыть", width=12, command=self.on_closing)
        self.b6.grid(row=7, column=3, padx = (0,10))

        self.view_command()

        self.window.mainloop()


    def second_window_command(self,title):
        self.second_window = tkinter.Toplevel(self.window)
        self.second_window.title =  "Бюджет 0.1: "+ title
        self.ls1 = Label(self.second_window, text="Название")
        self.ls1.grid(row=0, column=0, padx = 10)

        self.ls2 = Label(self.second_window, text="Стоимость")
        self.ls2.grid(row=2, column=0, padx = 10)

        self.ls3 = Label(self.second_window, text="Дата")
        self.ls3.grid(row=4, column=0, padx = 10)

        self.ls4 = Label(self.second_window, text="Категория")
        self.ls4.grid(row=6, column=0, padx=10)

        self.ls5 = Label(self.second_window, text="Комментарий")
        self.ls5.grid(row=8, column=0, padx=10)

        self.product_text = StringVar()
        self.es1 = Entry(self.second_window, textvariable=self.product_text)
        self.es1.grid(row=1, column=0, padx = 10)

        self.price_text = StringVar()
        self.es2 = Entry(self.second_window, textvariable=self.price_text)
        self.es2.grid(row=3, column=0, padx = 10)

        self.date_text = StringVar()
        self.es3 = Entry(self.second_window, textvariable=self.date_text)
        self.es3.grid(row=5, column=0, padx=10)

        self.cat_text = StringVar(value=self.categories[0])
        self.cat_cb_box = ttk.Combobox(self.second_window, textvariable=self.cat_text, values=self.categories)
        self.cat_cb_box.grid(row=7, column=0, padx = 10)

        self.comment_text = StringVar()
        self.es4 = Entry(self.second_window, textvariable=self.comment_text)
        self.es4.grid(row=9, column=0, padx = 10)

        self.second_window.bind('<Control-Key>', self.copypaste)

        self.second_window.focus_set()
        self.second_window.grab_set()


    def search_window_command(self):
        self.second_window_command("Поиск")
        self.bs1 = Button(self.second_window, text="Поиск", width=12, command=self.search_command)
        self.bs1.grid(row=11, column=0, padx=10, pady=(0, 10))


    def update_window_command(self):
        if self.table.selection() == None:

            messagebox.showinfo("Предупреждение", message="Выберите строку базы для обновления")
            self.window.grab_set()
            self.window.wait_window()
        else:
            print("Выбрано",selected_tuple)
            self.window.grab_release()
            self.second_window_command("Обновить")
            self.es1.insert(0,selected_tuple[1])
            self.es2.insert(0,selected_tuple[2])
            self.es3.insert(0,selected_tuple[4])
            self.es4.insert(0,selected_tuple[3])
            self.cat_cb_box.set(selected_tuple[5])
            print(self.cat_text.get())
            self.bs1 = Button(self.second_window, text="Обновить", width=12, command=self.update_command)
            self.bs1.grid(row=11, column=0, padx=10, pady=(0, 10))


    def add_window_command(self):
        self.second_window_command("Добавить")
        self.bs1 = Button(self.second_window, text="Добавить", width=12, command=self.add_command)
        self.bs1.grid(row=11, column=0, padx=10, pady=(0, 10))


    def del_second_window(self):
        self.second_window.destroy()
        del self.second_window
        self.window.grab_release()


    def view_command(self):
        self.sum = 0
        for i in self.table.get_children():
            self.table.delete(i)

        for row in self.db.view():
            self.table.insert('','end', values = row)
            self.sum += int(row[2])

        self.sum_text.set(str(self.sum))


    def search_command(self):
        for i in self.table.get_children():
            self.table.delete(i)
        self.sum = 0
        for row in self.db.search(self.product_text.get(),
                                  self.price_text.get(),
                                  self.comment_text.get(),
                                  self.date_text.get(),self.cat_text.get()):
            self.table.insert('','end', values = row)
            self.sum +=int(row[2])
        self.sum_text.set(str(self.sum))
        self.del_second_window()


    def add_command(self):
        print(self.cat_text.get())
        self.db.insert(self.product_text.get(),
                       self.price_text.get(),
                       self.comment_text.get(),
                       self.date_text.get(),
                       self.cat_text.get())

        self.del_second_window()
        self.view_command()


    def delete_command(self):
        self.db.delete(selected_tuple[0])
        self.view_command()


    def update_command(self):
        print(self.cat_text.get())
        self.db.update(selected_tuple[0],
                       self.product_text.get(),
                       self.price_text.get(),
                       self.comment_text.get(),
                       self.date_text.get(),
                       self.cat_text.get())
        selected_tuple == None
        self.del_second_window()
        self.view_command()


    def on_closing(self):
        if messagebox.askokcancel("", "Закрыть программу?"):
            self.window.destroy()


if __name__ == '__main__':
    app = Application()


from tkinter import *
import os
from tkinter import ttk
from functools import partial

import pandas
import pypyodbc as odbc  # pip install pypyodbc

DRIVER_NAME = 'SQL SERVER'
SERVER_NAME = 'DESKTOP-#######\\SQLEXPRESS'
DATABASE_NAME = 'Supermarket'
connection_string = f"""
    DRIVER={{{DRIVER_NAME}}};
    SERVER={SERVER_NAME};
    DATABASE={DATABASE_NAME};
    Trust_Connection=yes;
"""

global main_screen, app_screen, comenziscreen, comenziscreen1, comenziscreen2, aparitii, tree, username, password
global password_entry, password_label, username_entry, username_label
global username_verify, password_verify, username_login_entry, password_login_entry
global bt1, bt2, bt3, bt4, bt5, bt6, bt7, bt8, T, valoare, rows
global cur1, con1, modifywindow, names, mystr, myvars, record, idnum


def option3():
    global modifywindow
    modifywindow = Toplevel(app_screen)
    modifywindow.geometry("700x300")


def callwindow(option):
    global modifywindow
    if option == 1:
        qq = Toplevel(modifywindow)
        qq.title("INFO")
        qq.geometry("250x100")
        Label(qq, text="You pressed UPDATE").pack()
        Label(qq, text="").pack()
        Button(qq, text="OK", command=qq.destroy).pack()
    elif option == 2:
        qq = Toplevel(modifywindow)
        qq.title("INFO")
        qq.geometry("250x100")
        Label(qq, text="You pressed DELETE").pack()
        Label(qq, text="").pack()
        Button(qq, text="OK", command=qq.destroy).pack()


def connect():
    global cur1, con1
    con1 = odbc.connect(connection_string)
    cur1 = con1.cursor()
    con1.commit()
    con1.close()


def execquery():
    global con1, cur1, names, tree, rows
    querycommand = T.get("1.0", 'end-1c')
    con1 = odbc.connect(connection_string)
    cur1 = con1.cursor()
    cur1.execute(querycommand)
    rows = cur1.fetchall()
    names = list(map(lambda x: x[0], cur1.description))
    print(rows)
    tree.destroy()
    count = 1
    columnTuple = list("")
    for _ in names:
        columnTuple.append("c" + str(count))
        count = count + 1
    columnTuple = tuple(columnTuple)
    count = 0
    tree = ttk.Treeview(app_screen, columns=columnTuple, show='headings')

    scrollbarx = ttk.Scrollbar(app_screen, orient=HORIZONTAL, command=tree.xview)
    scrollbarx.place(width=1020, height=20, x=199, y=1)
    scrollbary = ttk.Scrollbar(app_screen, orient=VERTICAL, command=tree.yview)
    scrollbary.place(width=20, height=720, x=199, y=1)
    tree.configure(xscrollcommand=scrollbarx.set)
    tree.configure(yscrollcommand=scrollbary.set)

    def maxlen(cnter):
        maxlength = 0
        for cnt in rows:
            if len(str(cnt[cnter])) > maxlength:
                maxlength = len(str(cnt[cnter]))
        # print(maxlength)
        return maxlength

    j = 1
    suma = 0
    for i in names:
        value = maxlen(j - 1)
        suma += max(value * 7, len(i) * 9)
        tree.column("#" + str(j), width=value * 6, minwidth=max(len(i) * 9, value * 7))
        tree.heading("#" + str(j), text=i)
        j = j + 1
    if suma > 1000:
        tree.column("#" + str(j - 1), width=2500 - suma)

    for row in rows:
        if count % 2 == 0:
            tree.insert("", END, values=row, tags='gray')
        else:
            tree.insert("", END, values=row)
        count += 1

    tree.place(x=220, y=20, width=1000, height=700)
    tree.tag_configure('gray', background='#cccccc')


def newquery(_):
    global T
    winquery = Toplevel(app_screen)
    winquery.geometry("821x400")
    winquery.title("QUERY")
    winquery.resizable(False, False)
    Label(winquery, text="Enter your query").place(x=50, y=20)
    T = Text(winquery, height=15, width=84)
    T.place(x=21, y=50)
    scrollbary = ttk.Scrollbar(winquery, orient=VERTICAL, command=T.yview)
    scrollbary.place(width=20, height=400, x=801, y=0)
    T.configure(yscrollcommand=scrollbary.set)
    Button(winquery, text="Execute Query", width=20, height=2, command=execquery).place(x=330, y=330)


def setbuttons(temporar):
    global comenziscreen, comenziscreen1, comenziscreen2
    action4 = partial(newquery, 3)
    Button(comenziscreen2, text="Query", width=10, height=1, command=action4).pack(side=BOTTOM)
    action3 = partial(updatequery, 3)
    Button(comenziscreen2, text="ADD", width=10, height=1, command=action3).pack(side=BOTTOM)
    for i in temporar:
        if i != "table1" and i != "sqlite_sequence":
            # print(i[0])
            action_with_arg = partial(View, i)
            Button(comenziscreen1, text=i, width='20', height='1', command=action_with_arg).pack()
    comenziscreen.place(x=15)


def addelement():
    global con1, cur1, myvars, mystr
    con1 = odbc.connect(connection_string)
    cur1 = con1.cursor()
    dataf = pandas.read_sql("select * from " + app_screen.title(), con1)
    dataf = list(dataf.dtypes)
    i = 0
    print(dataf)
    for j in dataf:
        dataf[i] = str(j)
        i += 1
    cont = 0
    print(dataf)
    dataf = dataf[valoare:]
    columnsstring = ""
    for i in names[valoare:]:
        columnsstring = columnsstring + str(i) + ", "
    columnsstring = columnsstring[:-2]
    mystring = "INSERT INTO " + app_screen.title() + "(" + columnsstring + ")" + " VALUES ("
    print("hahahahahahahahaha")
    print(myvars[mystr[0]].get())
    for _ in names[valoare:]:
        # print(myvars[mystr[cont]].get())
        if myvars[mystr[cont]].get() != "":
            if dataf[cont].find("object") != -1 or dataf[cont].find("datetime") != -1:
                mystring = mystring + "\'" + myvars[mystr[cont]].get() + "',"
            else:
                mystring = mystring + myvars[mystr[cont]].get() + ","
        cont += 1
    mystring = mystring[:-1] + ");"
    print(mystring)
    cur1.execute(mystring)
    con1.commit()
    con1.close()
    qq = Toplevel(modifywindow)
    qq.title("INFO")
    qq.geometry("250x100")
    Label(qq, text="You pressed ADD row").pack()
    Label(qq, text="").pack()
    Button(qq, text="OK", command=qq.destroy).pack()


def updatequery(option):
    global cur1, con1, mystr, myvars, idnum
    global modifywindow
    if option == 1:
        con1 = odbc.connect(connection_string)
        cur1 = con1.cursor()
        dataf = pandas.read_sql("select * from " + app_screen.title(), con1)
        dataf = list(dataf.dtypes)
        i = 0
        print(dataf)
        for j in dataf:
            dataf[i] = str(j)
            i += 1
        mystring = "UPDATE " + app_screen.title() + " SET "
        cont = 0
        conditie = str(names[0])
        print("Update")
        print(names)
        dataf = dataf[valoare:]
        for j in names[valoare:]:
            print(j)
            print(myvars[mystr[cont]].get())
            if dataf[cont].find("object") != -1 or dataf[cont].find("datetime") != -1:
                mystring = mystring + str(j) + "='" + myvars[mystr[cont]].get() + "', "
            else:
                mystring = mystring + str(j) + "=" + myvars[mystr[cont]].get() + ", "
            cont += 1
        mystring = mystring[:-2] + " WHERE " + conditie + "=" + str(idnum) + ";"
        print("lalaband")
        print(mystring)
        cur1.execute(mystring)
        con1.commit()
        con1.close()
        callwindow(option)
    elif option == 2:
        con1 = odbc.connect(connection_string)
        cur1 = con1.cursor()
        mystring = "DELETE FROM " + app_screen.title() + " WHERE " + str(names[0]) + "=" + "\'" + str(idnum) + "\';"
        print(mystring)
        cur1.execute(mystring)
        con1.commit()
        con1.close()
        callwindow(option)
    elif option == 3:
        option3()
        placeholder = StringVar()
        cont = 0
        mystr = ["v0"]
        myvars = vars()
        for j in names[valoare:]:
            Label(modifywindow, text=j).grid(column=0, row=cont)
            placeholder.set("a" + str(cont))
            # print(placeholder.get())
            myvars[mystr[cont]] = StringVar()
            myvars[mystr[cont]].set("")
            Entry(modifywindow, name="entry" + str(cont), textvariable=myvars[mystr[cont]]).grid(column=1, row=cont)
            cont += 1
            mystr.append("v" + str(cont))
        Button(modifywindow, text="ADD row", width=10, height=1, command=addelement).grid(column=1, row=cont + 1)


def modifyvalues():
    global modifywindow, names, mystr, myvars, record, con1, cur1, valoare
    placeholder = StringVar()
    modifywindow = Toplevel(app_screen)
    modifywindow.geometry("700x300")
    cont = 0
    mystr = ["v0"]
    myvars = vars()
    con1 = odbc.connect(connection_string)
    cur1 = con1.cursor()
    # cur1.execute("select count(C.COLUMN_NAME) FROM INFORMATION_SCHEMA.TABLE_CONSTRAINTS T JOIN "
    #              "INFORMATION_SCHEMA.CONSTRAINT_COLUMN_USAGE C ON C.CONSTRAINT_NAME=T.CONSTRAINT_NAME WHERE "
    #              "C.TABLE_NAME='" + app_screen.title() + "' and T.CONSTRAINT_TYPE='PRIMARY KEY' ")
    # valoare = cur1.fetchall()
    # valoare = 0 if valoare[0][0] > 1 else 1
    print(record)
    print(names)

    for i, j in zip(record, names[valoare:]):
        Label(modifywindow, text=j).grid(column=0, row=cont)
        placeholder.set("a" + str(cont))
        # print(placeholder.get())
        myvars[mystr[cont]] = StringVar()
        myvars[mystr[cont]].set(str(i))
        Entry(modifywindow, name="entry" + str(cont), textvariable=myvars[mystr[cont]]).grid(column=1, row=cont)
        cont += 1
        mystr.append("v" + str(cont))
    Label(modifywindow, text="").grid(column=1, row=cont)
    action1 = partial(updatequery, 1)
    Button(modifywindow, text="UPDATE", width=10, height=1, command=action1).grid(column=1, row=cont + 1)
    action2 = partial(updatequery, 2)
    Button(modifywindow, text="DELETE", width=10, height=1, command=action2).grid(column=0, row=cont + 1)
    con1.close()


def item_selected(_):
    global modifywindow, record, rows, idnum
    print("Print tree selection")
    print(rows)
    print(tree.selection())
    for selected_item in tree.selection():
        item = tree.item(selected_item)
        print("Print selected item")
        print(int(selected_item[1:], 16))
        idnum = rows[int(selected_item[1:], 16)-1][0]
        record = item['values']
        modifyvalues()
        # pyperclip.copy(str(record))


def View(titlu):
    app_screen.title(titlu)
    global aparitii, tree, names, cur1, con1, valoare, rows
    aparitii += 1
    if aparitii > 1:
        tree.destroy()
    con1 = odbc.connect(connection_string)
    cur1 = con1.cursor()
    temporar = []
    for i in cur1.tables(tableType='TABLE', schema='dbo'):
        temporar.append(i[2])
    cur1.execute("SELECT * FROM " + titlu + ";")
    rows = cur1.fetchall()
    names = list(map(lambda x: x[0], cur1.description))
    if aparitii == 1:
        setbuttons(temporar)
    count = 1
    columnTuple = list("")
    cur1.execute("select count(C.COLUMN_NAME) FROM INFORMATION_SCHEMA.TABLE_CONSTRAINTS T JOIN "
                 "INFORMATION_SCHEMA.CONSTRAINT_COLUMN_USAGE C ON C.CONSTRAINT_NAME=T.CONSTRAINT_NAME WHERE "
                 "C.TABLE_NAME='" + app_screen.title() + "' and T.CONSTRAINT_TYPE='PRIMARY KEY' ")
    valoare = cur1.fetchall()
    print(valoare)
    valoare = 0 if valoare[0][0] > 1 else 1
    for _ in names[valoare:]:
        columnTuple.append("c" + str(count))
        count = count + 1
    columnTuple = tuple(columnTuple)
    # print(columnTuple)
    tree = ttk.Treeview(app_screen, columns=columnTuple, show='headings')

    scrollbarx = ttk.Scrollbar(app_screen, orient=HORIZONTAL, command=tree.xview)
    scrollbarx.place(width=1020, height=20, x=199, y=1)
    scrollbary = ttk.Scrollbar(app_screen, orient=VERTICAL, command=tree.yview)
    scrollbary.place(width=20, height=720, x=199, y=1)
    tree.configure(xscrollcommand=scrollbarx.set)
    tree.configure(yscrollcommand=scrollbary.set)

    def maxlen(cnter):
        maxlength = 0
        for cnt in rows:
            if len(str(cnt[cnter])) > maxlength:
                maxlength = len(str(cnt[cnter]))
        # print(maxlength)
        return maxlength

    j = 1
    suma = 0
    for i in names[valoare:]:
        value = maxlen(j - 1)
        suma += max(value * 7, len(i) * 9)
        tree.column("#" + str(j), width=value * 6, minwidth=max(len(i) * 9, value * 7))
        tree.heading("#" + str(j), text=i)
        j = j + 1
    if suma > 1000:
        tree.column("#" + str(j - 1), width=2500 - suma)
    tree.bind('<<TreeviewSelect>>', item_selected)
    tree.pack(fill='x', expand=YES)
    count = 0
    for row in rows:
        print(row)
        if count % 2 == 0:
            # print(row)
            tree.insert("", END, values=row[valoare:], tags='gray')
        else:
            tree.insert("", END, values=row[valoare:])
        count += 1
    tree.update_idletasks()
    tree.place(x=220, y=20, width=1000, height=700)
    tree.tag_configure('gray', background='#cccccc')
    con1.close()
    return names


def deletebuttonsmain():
    bt1.destroy()
    bt2.destroy()
    bt3.destroy()
    bt4.destroy()
    bt5.destroy()


def deleteloginbuttons():
    bt1.destroy()
    bt2.destroy()
    bt3.destroy()
    bt4.destroy()
    bt5.destroy()
    bt6.destroy()
    bt7.destroy()
    username_login_entry.destroy()
    password_login_entry.destroy()
    main_account_screen()


def deleteregbuttons():
    bt1.destroy()
    bt2.destroy()
    bt3.destroy()
    bt4.destroy()
    bt5.destroy()
    username_entry.destroy()
    password_entry.destroy()
    username_label.destroy()
    password_label.destroy()
    main_account_screen()


def register():
    deletebuttonsmain()
    main_screen.title("Register")
    main_screen.geometry("300x250")
    global username
    global password
    global username_entry, username_label
    global password_entry, password_label
    global bt1, bt2, bt3, bt4, bt5
    username = StringVar()
    password = StringVar()

    bt1 = Label(main_screen, text="Please enter details below to register")
    bt1.pack()
    bt2 = Label(main_screen, text="")
    bt2.pack()
    username_label = Label(main_screen, text="Username                         ")
    username_label.pack()
    username_entry = Entry(main_screen, textvariable=username)
    username_entry.pack()
    password_label = Label(main_screen, text="Password                          ")
    password_label.pack()
    password_entry = Entry(main_screen, textvariable=password, show='*')
    password_entry.pack()
    bt3 = Label(main_screen, text="")
    bt3.pack()
    bt4 = Button(main_screen, text="Register", width=10, height=1, command=register_user)
    bt4.pack()
    bt5 = Button(main_screen, text="Back", width=5, height=1, command=deleteregbuttons)
    bt5.place(x=0, y=0)
    bt5.pack()


def login():
    deletebuttonsmain()
    global bt1, bt2, bt3, bt4, bt5, bt6, bt7, bt8
    main_screen.title("Login")
    main_screen.geometry("300x250")
    bt1 = Label(main_screen, text="Please enter details below to login")
    bt1.pack()
    bt2 = Label(main_screen, text="")
    bt2.pack()

    global username_verify
    global password_verify

    username_verify = StringVar()
    password_verify = StringVar()

    global username_login_entry
    global password_login_entry

    bt3 = Label(main_screen, text="Username                         ")
    bt3.pack()
    username_login_entry = Entry(main_screen, textvariable=username_verify)
    username_login_entry.pack()
    bt4 = Label(main_screen, text="Password                          ")
    bt4.pack()
    password_login_entry = Entry(main_screen, textvariable=password_verify, show='*')
    password_login_entry.pack()
    bt5 = Label(main_screen, text="")
    bt5.pack()
    bt6 = Button(main_screen, text="Login", width=10, height=1, command=login_verify)
    bt6.pack()
    bt7 = Button(main_screen, text="Back", width=5, height=1, command=deleteloginbuttons)
    bt7.place(x=0, y=0)
    bt7.pack()


def register_user():
    username_info = username.get()
    password_info = password.get()

    file = open("Users\\" + username_info, "w")
    file.write(username_info + "\n")
    file.write(password_info)
    file.close()

    username_entry.delete(0, END)
    password_entry.delete(0, END)

    Label(main_screen, text="Registration Success", fg="green", font=("calibri", 11)).pack()


def login_verify():
    username1 = username_verify.get()
    password1 = password_verify.get()
    username_login_entry.delete(0, END)
    password_login_entry.delete(0, END)

    list_of_files = os.listdir("Users\\")
    if username1 in list_of_files:
        file1 = open("Users\\" + username1, "r")
        verify = file1.read().splitlines()
        if password1 in verify:
            login_sucess()
        else:
            password_not_recognised()

    else:
        user_not_found()


def on_closing():
    main_screen.state(newstate='normal')
    app_screen.destroy()


def login_sucess():
    global app_screen
    main_screen.state(newstate='iconic')
    global aparitii
    aparitii = 0
    app_screen = Toplevel(main_screen)
    app_screen.iconbitmap("strudel.ico")
    app_screen.protocol("WM_DELETE_WINDOW", on_closing)
    app_screen.geometry("1220x720+350+150")
    app_screen.resizable(False, False)
    global comenziscreen, comenziscreen1, comenziscreen2
    comenziscreen = Frame(app_screen)
    comenziscreen.place(height=700, width=1000, x=220, y=20)
    comenziscreen1 = Frame(app_screen)
    comenziscreen1.place(height=650, width=200, x=0, y=0)
    comenziscreen2 = Frame(app_screen)
    comenziscreen2.place(height=70, width=200, x=0, y=650)
    connect()
    View("Angajati")


def password_not_recognised():
    password_not_recog_screen = Toplevel(main_screen)
    password_not_recog_screen.title("ERROR")
    password_not_recog_screen.geometry("250x100")
    Label(password_not_recog_screen, text="Invalid Password ").pack()
    Label(password_not_recog_screen, text="").pack()
    Button(password_not_recog_screen, text="OK", command=password_not_recog_screen.destroy).pack()


def user_not_found():
    user_not_found_screen = Toplevel(main_screen)
    user_not_found_screen.title("ERROR")
    user_not_found_screen.geometry("250x100")
    Label(user_not_found_screen, text="User Not Found").pack()
    Label(user_not_found_screen, text="").pack()
    Button(user_not_found_screen, text="OK", command=user_not_found_screen.destroy).pack()


def setupmain():
    global main_screen
    main_screen = Tk()
    main_screen.iconbitmap("strudel.ico")
    main_screen.geometry("300x250+800+300")
    main_screen.title("Account Login")
    main_screen.resizable(False, False)


def main_account_screen():
    global bt1, bt2, bt3, bt4, bt5
    bt1 = Label(text="Select Your Choice", bg="white", width="300", height="2", font=("Calibri", 13))
    bt1.pack()
    bt2 = Label(text="")
    bt2.pack()
    bt3 = Button(text="Login", height="2", width="30", command=login)
    bt3.pack()
    bt4 = Label(text="")
    bt4.pack()
    bt5 = Button(text="Register", height="2", width="30", command=register)
    bt5.pack()
    main_screen.mainloop()


setupmain()
main_account_screen()

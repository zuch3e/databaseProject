# Neleptcu Daniel-Andrei 332AB, 11/01/2024 Proiect BD

from tkinter import *
import os
from tkinter import ttk
from functools import partial
from tkinter.ttk import Combobox
import copy
from tkcalendar import Calendar
import pandas
import pypyodbc as odbc
from datetime import datetime

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
global password_entry, password_label, username_entry, username_label, winquery
global username_verify, password_verify, username_login_entry, password_login_entry
global bt1, bt2, bt3, bt4, bt5, bt6, bt7, bt8, T, TQ, TT, valoare, rows, TL, TW, twvar, twvar2
global cur1, con1, modifywindow, names, mystr, myvars, record, idnum, TE, t15val, T15

mapare = [["departament_id", "Departamente", "nume_departament", "nume departament"],
          ["supervizor_id", "Angajati", "CONCAT(nume, ' ', prenume)", "supervizor"],
          ["produs_id", "Produse", "nume_produs", "nume produs"],
          ["manager_id", "Angajati", "CONCAT(nume, ' ', prenume)", "manager"],
          ["producator_id", "Producatori", "nume_producator", "nume producator"],
          ["angajat_id", "Angajati", "CONCAT(nume, ' ', prenume)", "Nume Angajat"],
          ["bonfiscal_id", "BonAngajat", "bonfiscal_id", "bonfiscal_id"]]

interogariTema = [
    # 1
    """
Select nume_produs as "Nume Produs" from Produse P
inner join Bon_fiscal B
on P.produs_id=B.produs_id
WHERE B.cantitate > placeHolder
""",
    # 2
    """
Select distinct nume_producator as "Nume Producator" from Producatori P
inner join ProducatoriProduse PP
on P.producator_id=PP.producator_id
inner join Produse Pr
on PP.produs_id=Pr.produs_id
where Pr.nume_produs like '%placeHolder%'
""",
    # 3
    """
select distinct count(*) as "Numar Bonuri" from Bon_Fiscal BF
inner join BonAngajat BA
on BF.bonfiscal_id=BA.bonfiscal_id
inner join Produse Pr
on BF.produs_id=Pr.produs_id
where Pr.nume_produs like '%placeHolder%' and Ba.bonfiscal_data > 'place2Holder'
group by Bf.bonfiscal_id
""",
    # 4
    """
select distinct concat(A.nume, ' ', A.prenume) as "Nume Angajati" from Angajati A
inner join BonAngajat BA
on A.angajat_id=BA.angajat_id
inner join Bon_Fiscal BF
on BA.bonfiscal_id=BF.bonfiscal_id
inner join Produse P
on BF.produs_id=P.produs_id
where P.nume_produs like '%placeHolder%'
""",
    # 5
    """
select sum(PPT.cost_total) as "Cost Total" from ProducatoriProduseTranzactii PPT
inner join Produse P
on P.produs_id=PPT.produs_id
where P.nume_produs like '%placeHolder%'
""",
    # 6
    """
SELECT concat(A.Nume, ' ', A.Prenume) as "Nume Supervizori" 
FROM Angajati A INNER JOIN Angajati AA ON A.Angajat_ID=AA.Supervizor_ID
GROUP BY A.Nume, A.Prenume 
HAVING COUNT(A.Angajat_ID) >= placeHolder
""",
    # 7
    """
SELECT A.Nume, A.Prenume, A.Salariu, D.nume_departament as "Nume Departament"
FROM Angajati As A
INNER JOIN
( SELECT MAX(AA.Salariu) as SalariuMaxim, DD.Departament_ID, DD.Nume_Departament
FROM Angajati as AA
INNER JOIN Departamente As DD on AA.Departament_ID = DD.Departament_ID
GROUP BY DD.Departament_ID, DD.Nume_Departament
) As D on A.Departament_ID = D.Departament_ID and D.SalariuMaxim = A.Salariu
ORDER BY A.Salariu DESC
""",
    # 8
    """
SELECT A.Nume, A.Prenume, B.Nume_Departament as "Nume Departament", A.data_nasterii as "Data Nasterii"
FROM Angajati A
INNER JOIN (SELECT Departament_ID, MAX(data_nasterii) AS data_nasterii
FROM Angajati
GROUP BY Departament_ID) C
ON A.Departament_ID = C.Departament_ID AND A.data_nasterii=C.data_nasterii
INNER JOIN Departamente B ON A.Departament_ID = B.Departament_ID
""",
    # 9
    """
SELECT D.nume_departament "Nume departament"
FROM Departamente D
WHERE (SELECT count(*) FROM angajati a WHERE a.Departament_ID=D. Departament_ID) < placeHolder
""",
    # 10
    """
SELECT TOP placeHolder concat(A.nume, ' ', A.prenume) as "Angajat", D.nume_departament as "Departament", A.salariu 
FROM angajati A
INNER JOIN Departamente D
ON A.departament_id=D.departament_id
ORDER BY salariu DESC
""",
    # 11
    """
SELECT year(data_nasterii) as "Anul Nasterii", count(*) as "Nr Angajati"
FROM angajati
GROUP BY year(data_nasterii)
HAVING count (*) IN (SELECT TOP 1 count(*)
FROM angajati
GROUP BY year(data_nasterii)
ORDER BY 1 DESC)
""",
    # 12
    """
SELECT concat(Nume, ' ', Prenume), salariu FROM Angajati
WHERE SALARIU > (
SELECT AVG(Salariu) FROM Angajati)
ORDER BY salariu asc
""",
    # 13
    """
SELECT P.nume_produs, P.categorie, P.calorii FROM Produse P
WHERE P.calorii > (
SELECT AVG(Q.calorii)
FROM Produse Q
where Q.categorie = P.categorie)
""",
    # 14
    """
Select Pr.nume_producator as "Producator", P.nume_produs as "Produs", P.categorie, P.pret from Producatori Pr
inner join ProducatoriProduse PP 
on Pr.producator_id=PP.producator_id
inner join Produse P
on PP.produs_id=P.produs_id
inner join (	
SELECT categorie, MAX(pret) as pret_maxim FROM produse
GROUP BY categorie ) AS preturi_maxime
ON P.categorie = preturi_maxime.categorie and P.pret = preturi_maxime.pret_maxim
""",
    # 15
    """
Select PQ.nume_produs as "Produs", -PPT.cost_total + (Select sum(BF.cantitate)*P.pret FROM bon_fiscal BF
inner join Produse P
on P.produs_id = Bf.produs_id
where P.produs_id=PPT.produs_id
GROUP BY Bf.produs_id, P.pret) as "Profit Actual" FROM ProducatoriProduseTranzactii PPT
inner join Produse PQ
on PPT.produs_id = PQ.produs_id
""",
    # 16
    """
SELECT concat(A.nume, ' ', A.prenume) as "Angajat", D.nume_departament as "Nume departament", A.salariu
FROM angajati A
inner join Departamente D
on A.departament_id=D.departament_id
WHERE salariu > ALL
(SELECT AA.salariu
FROM angajati AA  
inner JOIN Departamente DD
ON AA.departament_id = DD.departament_id
WHERE DD.nume_departament like '%placeHolder%')

"""
]

interogariTemaTemp = copy.copy(interogariTema)

enunturi = [
    "Numele produselor vandute cu o cantitate mai mare decat cea [introdusa]",
    "Numele producatorilor ce aprovizioneaza cu un [anumit produs]",
    "Numarul de bonuri pe care apare un [anumit produs] vandut dupa o [anumita data]",
    "Numele angajatilor care au vandut un [anumit produs]",
    "Pretul platit de supermarket pentru a achizitiona un [anumit produs]",
    "Supervizorii care au mai multi subordonati decat o [anumita valoare]",
    "Angajatii cu cel mai mare salariu pentru fiecare departament, sortati descrescator",
    "Cei mai tineri angajati din fiecare departament. Ordonati dupa data nasterii.",
    "Departamentele care au mai putini angajati decat un [anumit numar]",
    "Primii [n] angajati si departamentul lor in functie de salariul castigat",
    "In ce an s-au nascut cei mai multi angajati? Afisati anul si numarul angajatilor",
    "Angajatii care au un salariu mai mare decat media salariilor, sortati crescator",
    "Produsele care depasesc media caloriilor din categoria lor.",
    "Producatorii celor mai scumpe produse din fiecare categorie",
    "Profitul realizat pentru fiecare produs (vanzare - aprovizionare)",
    "Angajatii cu salariul mai mare decat salariul maxim dintr-un [anumit departament]."]

index = 0


def getquery(querycommand):
    global con1, cur1, names, tree, rows
    con1 = odbc.connect(connection_string)
    cur1 = con1.cursor()
    cur1.execute(querycommand)
    rows = cur1.fetchall()
    names = list(map(lambda x: x[0], cur1.description))
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


def query1():
    global index, twvar, t15val, TE, interogariTema, interogariTemaTemp
    if index == 15:
        interogariTema[index] = interogariTema[index].replace("placeHolder", str(t15val.get()))
    else:
        interogariTema[index] = interogariTema[index].replace("placeHolder", str(twvar.get()))
    if index == 2:
        modifdate = datetime.strptime(TE.get_date(), '%m/%d/%y').strftime('%Y-%m-%d')
        interogariTema[index] = interogariTema[index].replace("place2Holder", modifdate)
    getquery(interogariTema[index])
    interogariTema[index] = interogariTemaTemp[index]


def option3():
    global modifywindow
    modifywindow = Toplevel(app_screen)
    modifywindow.geometry("350x300")
    modifywindow.title(app_screen.title() + " ADD")


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
    querycommand = T.get("1.0", 'end-1c')
    getquery(querycommand)


def gonext():
    global index, TT, TL, TQ, TW, TE, T15

    if index < len(enunturi) - 1:
        index += 1
        if index == 15:
            T15.place(x=winquery.winfo_width() / 2 - 90, y=winquery.winfo_height() / 2 - 10)
        else:
            T15.place(x=winquery.winfo_width(), y=winquery.winfo_height())
        if index == 2:
            TE.place(width=250, height=180, x=winquery.winfo_width() / 2 - 90 - 44, y=winquery.winfo_height() / 2 - 30)
            TW.place(x=winquery.winfo_width() / 2 - 90, y=winquery.winfo_height() / 2 - 55)
        else:
            TE.place(width=250, height=180, x=winquery.winfo_width(), y=winquery.winfo_height())
        if index in [6, 7, 10, 11, 12, 13, 14, 15]:
            TW.place(x=winquery.winfo_width(), y=winquery.winfo_height())
        elif index != 2:
            TW.place(x=winquery.winfo_width() / 2 - 90, y=winquery.winfo_height() / 2 - 10)
        TL.config(text="Interogarea numarul " + str(index + 1))
        TT.config(text=enunturi[index])
        TQ.set(enunturi[index])


def goprev():
    global index, TT, TL, TQ, TE, winquery, T15
    if index >= 1:
        index -= 1
        if index == 15:
            T15.place(x=winquery.winfo_width() / 2 - 90, y=winquery.winfo_height() / 2 - 10)
        else:
            T15.place(x=winquery.winfo_width(), y=winquery.winfo_height())
        if index == 2:
            TE.place(width=250, height=180, x=winquery.winfo_width() / 2 - 90 - 44, y=winquery.winfo_height() / 2 - 30)
            TW.place(x=winquery.winfo_width() / 2 - 90, y=winquery.winfo_height() / 2 - 55)
        else:
            TE.place(width=250, height=180, x=winquery.winfo_width(), y=winquery.winfo_height())
        if index in [6, 7, 10, 11, 12, 13, 14, 15]:
            TW.place(x=winquery.winfo_width(), y=winquery.winfo_height())
        elif index != 2:
            TW.place(x=winquery.winfo_width() / 2 - 90, y=winquery.winfo_height() / 2 - 10)
        TL.config(text="Interogarea numarul " + str(index + 1))
        TT.config(text=enunturi[index])
        TQ.set(enunturi[index])


def newquery(alegere):
    global T, TT, TQ, TL, TW, TE, twvar, winquery, twvar2, T15, t15val
    if alegere == 4:
        winquery = Toplevel(app_screen)
        winquery.geometry("821x400")
        winquery.title("QUERY")
        winquery.resizable(False, False)
        winquery.update_idletasks()
        Label(winquery, text="Enter your query").place(x=50, y=20)
        T = Text(winquery, height=15, width=84)
        T.place(x=21, y=50)
        scrollbary = ttk.Scrollbar(winquery, orient=VERTICAL, command=T.yview)
        scrollbary.place(width=20, height=400, x=801, y=0)
        T.configure(yscrollcommand=scrollbary.set)
        Button(winquery, text="Execute Query", width=20, height=2, command=execquery).place(x=330, y=330)
    else:
        twvar = StringVar()
        twvar2 = StringVar()
        t15val = StringVar()

        def schimbquery(_):
            global index, t15val
            i = 0
            for en in enunturi:
                if en == comboval.get():
                    index = i
                    break
                i += 1
            TT.config(text=enunturi[index])
            TL.config(text="Interogarea numarul " + str(index + 1))
            TE.place(width=250, height=180, x=winquery.winfo_width(), y=winquery.winfo_height())
            if index == 15:
                T15.place(x=winquery.winfo_width() / 2 - 90, y=winquery.winfo_height() / 2 - 10)
                print("sunt la 15")
            else:
                T15.place(x=winquery.winfo_width(), y=winquery.winfo_height())
                print("nu sunt la 15")
            if index == 2:
                TE.place(width=250, height=180, x=winquery.winfo_width() / 2 - 90 - 44,
                         y=winquery.winfo_height() / 2 - 30)
                TW.place(x=winquery.winfo_width() / 2 - 90, y=winquery.winfo_height() / 2 - 55)
            else:
                TE.place(width=250, height=180, x=winquery.winfo_width(), y=winquery.winfo_height())
            if index in [6, 7, 10, 11, 12, 13, 14, 15]:
                TW.place(x=winquery.winfo_width(), y=winquery.winfo_height())
            elif index != 2:
                TW.place(x=winquery.winfo_width() / 2 - 90, y=winquery.winfo_height() / 2 - 10)

        winquery = Toplevel(app_screen)
        winquery.geometry("800x400")
        winquery.title("QUERY")
        winquery.resizable(False, False)
        winquery.update_idletasks()
        comboval = StringVar()
        comboval.set(value=enunturi[0])
        TQ = Combobox(winquery, textvariable=comboval, values=tuple(enunturi), width=92)
        TQ.bind('<<ComboboxSelected>>', schimbquery)
        TQ.place(x=20, y=10)
        TL = Label(winquery, text="Interogarea numarul 1")
        TL.place(x=20, y=40)
        TT = Label(winquery,
                   text="Numele produselor vandute cu o cantitate mai mare decat cea [introdusa]",
                   justify="left")
        TT.place(x=20, y=70)
        TE = Calendar(winquery, selectmode='day', year=2024, month=1, day=1)
        TE.place(width=250, height=180, x=winquery.winfo_width(), y=winquery.winfo_height())
        TW = Entry(winquery, textvariable=twvar)
        TW.place(x=winquery.winfo_width() / 2 - 90, y=winquery.winfo_height() / 2 - 10)

        conn1 = odbc.connect(connection_string)
        curr1 = conn1.cursor()
        curr1.execute("Select nume_departament from departamente")
        strrr = curr1.fetchall()
        for iq, iqi in zip(strrr, range(len(strrr))):
            strrr[iqi] = iq[0]
        t15val = StringVar(value=strrr[0])
        T15 = Combobox(winquery, textvariable=t15val, values=tuple(strrr), width=22)
        T15.place(x=winquery.winfo_width(), y=winquery.winfo_height())
        conn1.commit()
        conn1.close()

        Button(winquery, text="Execute", width=10, height=1, command=query1).place(x=winquery.winfo_width() / 2 - 45,
                                                                                   y=winquery.winfo_height() - 32)
        Button(winquery, text="Next", width=10, height=1, command=gonext).place(x=winquery.winfo_width() - 90,
                                                                                y=winquery.winfo_height() - 32)
        Button(winquery, text="Previous", width=10, height=1, command=goprev).place(x=0, y=winquery.winfo_height() - 32)


def setbuttons(temporar):
    global comenziscreen, comenziscreen1, comenziscreen2
    qval = StringVar(value="16Interogari")
    optt = ["16Interogari", "Query"]

    def action4choose(_):
        if qval.get() == "16Interogari":
            action4 = partial(newquery, 3)
            action4()
        else:
            action5 = partial(newquery, 4)
            action5()

    OptionMenu(comenziscreen2, qval, *optt, command=action4choose).pack(side=BOTTOM)
    action3 = partial(updatequery, 3)
    Button(comenziscreen2, text="ADD", width=10, height=1, command=action3).pack(side=BOTTOM)
    for i in temporar:
        if i != "table1" and i != "sqlite_sequence":
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
    for j in dataf:
        dataf[i] = str(j)
        i += 1
    cont = 0
    dataf = dataf[valoare:]
    columnsstring = ""
    for i in names[valoare:]:
        columnsstring = columnsstring + str(i) + ", "
    columnsstring = columnsstring[:-2]
    mystring = "INSERT INTO " + app_screen.title() + "(" + columnsstring + ")" + " VALUES ("
    if app_screen.title() == "BonAngajat":
        mystring = "INSERT INTO " + app_screen.title() + "(angajat_id, bonfiscal_data)" + " VALUES ("
    for _ in names[valoare:]:
        if myvars[mystr[cont]].get() != "" or myvars[mystr[cont]].get() != "NULL":
            if dataf[cont].find("object") != -1 or dataf[cont].find("datetime") != -1:
                mystring = mystring + "\'" + myvars[mystr[cont]].get() + "',"
            else:
                mystring = mystring + myvars[mystr[cont]].get() + ","
        cont += 1
    if app_screen.title() == "BonAngajat":
        mystring = mystring[:-1].replace("VALUES (,", "VALUES (")
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
    print("am intrat", option)
    global modifywindow
    if option == 1:
        con1 = odbc.connect(connection_string)
        cur1 = con1.cursor()
        dataf = pandas.read_sql("select * from " + app_screen.title(), con1)
        dataf = list(dataf.dtypes)
        i = 0
        for j in dataf:
            dataf[i] = str(j)
            i += 1
        mystring = "UPDATE " + app_screen.title() + " SET "
        cont = 0
        conditie = str(names[0])
        dataf = dataf[valoare:]
        for j in names[valoare:]:
            if app_screen.title() == "BonAngajat" and j != "bonfiscal_id" and j != "prettotal":
                if dataf[cont].find("object") != -1 or dataf[cont].find("datetime") != -1:
                    mystring = mystring + str(j) + "='" + myvars[mystr[cont]].get() + "', "
                else:
                    mystring = mystring + str(j) + "=" + myvars[mystr[cont]].get() + ", "
            elif app_screen.title() != "BonAngajat":
                if dataf[cont].find("object") != -1 or dataf[cont].find("datetime") != -1:
                    mystring = mystring + str(j) + "='" + myvars[mystr[cont]].get() + "', "
                else:
                    mystring = mystring + str(j) + "=" + myvars[mystr[cont]].get() + ", "
            cont += 1

        mystring = mystring[:-2] + " WHERE " + conditie + "=" + str(idnum) + ";"
        mystring = mystring.replace("None", "NULL")
        mystring = mystring.replace("'NULL'", "NULL")
        print(mystring)
        cur1.execute(mystring)
        con1.commit()
        con1.close()
        callwindow(option)
    elif option == 2:
        con1 = odbc.connect(connection_string)
        cur1 = con1.cursor()
        mystring = "DELETE FROM " + app_screen.title() + " WHERE " + str(names[0]) + "=" + str(idnum)
        print(mystring)
        if app_screen.title() == "BonAngajat":
            mystring1 = "DELETE FROM Bon_Fiscal WHERE bonfiscal_id = " + str(idnum) + ";"
            print(mystring1)
            cur1.execute(mystring1)
            con1.commit()
        cur1.execute(mystring)
        con1.commit()
        con1.close()
        callwindow(option)
    elif option == 3:
        con1 = odbc.connect(connection_string)
        cur1 = con1.cursor()
        option3()
        placeholder = StringVar()
        cont = 0
        mystr = ["v0"]
        myvars = vars()
        for j in names[valoare:]:
            jtemp = j
            for itemp in mapare:
                if itemp[0] == j:
                    jtemp = itemp[3]
                    break
            jtemp = jtemp.replace("_", " ")
            if app_screen.title() == "BonAngajat" and j != "bonfiscal_id" and j != "prettotal":
                Label(modifywindow, text=jtemp).grid(column=0, row=cont)
            elif app_screen.title() != "BonAngajat":
                Label(modifywindow, text=jtemp).grid(column=0, row=cont)
            placeholder.set("a" + str(cont))
            myvars[mystr[cont]] = StringVar()
            myvars[mystr[cont]].set("")
            if j == "produs_id":
                cur1.execute("SELECT nume_produs FROM Produse")
                produse = cur1.fetchall()
                cur1.execute("SELECT produs_id FROM Produse")
                idproduse = cur1.fetchall()
                produsearr = []
                idprodusearr = []
                for q, k in zip(produse, idproduse):
                    produsearr.append(q[0])
                    idprodusearr.append(k[0])
                valle = StringVar(value="")
                valle.set(myvars[mystr[cont]].get())

                def textget(_):
                    for qq, kk in zip(produsearr, idprodusearr):
                        if valle.get() == qq:
                            myvars[mystr[tempcont]].set(str(kk))
                            break

                tempcont = cont
                OptionMenu(modifywindow, valle, *produsearr, command=textget).grid(column=1, row=cont)
            elif j == "supervizor_id":
                cur1.execute("SELECT CONCAT(nume, ' ', prenume) FROM Angajati")
                sup = cur1.fetchall()
                cur1.execute("SELECT angajat_id FROM Angajati")
                idsup = cur1.fetchall()
                suparr = ["None"]
                idsuparr = ["NULL"]
                for q, k in zip(sup, idsup):
                    suparr.append(q[0])
                    idsuparr.append(k[0])
                valles = StringVar(value="")
                valles.set(myvars[mystr[cont]].get())

                def textgets(_):
                    for qq, kk in zip(suparr, idsuparr):
                        if valles.get() == qq:
                            myvars[mystr[tempconts]].set(str(kk))
                            break

                tempconts = cont
                OptionMenu(modifywindow, valles, *suparr, command=textgets).grid(column=1, row=cont)
            elif j == "departament_id":
                cur1.execute("SELECT nume_departament FROM Departamente")
                dep = cur1.fetchall()
                cur1.execute("SELECT departament_id FROM Departamente")
                iddep = cur1.fetchall()
                deparr = []
                iddeparr = []
                for q, k in zip(dep, iddep):
                    deparr.append(q[0])
                    iddeparr.append(k[0])
                valled = StringVar(value="")
                valled.set(myvars[mystr[cont]].get())

                def textgetd(_):
                    for qq, kk in zip(deparr, iddeparr):
                        if valled.get() == qq:
                            myvars[mystr[tempcontdep]].set(str(kk))
                            break

                tempcontdep = cont
                OptionMenu(modifywindow, valled, *deparr, command=textgetd).grid(column=1, row=cont)
            elif j == "manager_id":
                cur1.execute("SELECT CONCAT(nume, ' ', prenume) FROM Angajati")
                man = cur1.fetchall()
                cur1.execute("SELECT angajat_id FROM Angajati ORDER BY angajat_id")
                idman = cur1.fetchall()
                manarr = []
                idmanarr = []
                for q, k in zip(man, idman):
                    manarr.append(q[0])
                    idmanarr.append(k[0])
                vallem = StringVar(value="")
                vallem.set(myvars[mystr[cont]].get())

                def textgetm(_):
                    for qq, kk in zip(manarr, idmanarr):
                        if vallem.get() == qq:
                            myvars[mystr[tempcontman]].set(str(kk))
                            break

                tempcontman = cont
                OptionMenu(modifywindow, vallem, *manarr, command=textgetm).grid(column=1, row=cont)
            elif j == "angajat_id":
                cur1.execute("SELECT CONCAT(nume, ' ', prenume) FROM Angajati WHERE departament_id = 2")
                ang = cur1.fetchall()
                cur1.execute("SELECT angajat_id FROM Angajati WHERE departament_id = 2 ORDER BY angajat_id")
                idang = cur1.fetchall()
                angarr = []
                idangarr = []
                for q, k in zip(ang, idang):
                    angarr.append(q[0])
                    idangarr.append(k[0])
                vallea = StringVar(value="")
                vallea.set(myvars[mystr[cont]].get())

                def textgetm(_):
                    for qq, kk in zip(angarr, idangarr):
                        if vallea.get() == qq:
                            myvars[mystr[tempcontang]].set(str(kk))
                            break

                tempcontang = cont
                OptionMenu(modifywindow, vallea, *angarr, command=textgetm).grid(column=1, row=cont)
            elif j == "producator_id":
                cur1.execute("SELECT nume_producator FROM Producatori")
                pro = cur1.fetchall()
                cur1.execute("SELECT producator_id FROM Producatori")
                idpro = cur1.fetchall()
                proarr = []
                idproarr = []
                for q, k in zip(pro, idpro):
                    proarr.append(q[0])
                    idproarr.append(k[0])
                vallep = StringVar(value="")
                vallep.set(myvars[mystr[cont]].get())

                def textgetp(_):
                    for qq, kk in zip(proarr, idproarr):
                        if vallep.get() == qq:
                            myvars[mystr[tempcontpro]].set(str(kk))
                            break

                tempcontpro = cont
                textgetp(1)
                OptionMenu(modifywindow, vallep, *proarr, command=textgetp).grid(column=1, row=cont)
            else:
                if app_screen.title() == "BonAngajat" and j != "bonfiscal_id" and j != "prettotal":
                    Entry(modifywindow, name="entry" + str(cont), textvariable=myvars[mystr[cont]]).grid(column=1,
                                                                                                         row=cont)
                elif app_screen.title() != "BonAngajat":
                    Entry(modifywindow, name="entry" + str(cont), textvariable=myvars[mystr[cont]]).grid(column=1,
                                                                                                         row=cont)

            cont += 1
            mystr.append("v" + str(cont))
        Button(modifywindow, text="ADD row", width=10, height=1, command=addelement).grid(column=1, row=cont + 1)
        con1.commit()
        con1.close()
        callwindow(option)


def modifyvalues():
    global modifywindow, names, mystr, myvars, record, con1, cur1, valoare
    placeholder = StringVar()
    modifywindow = Toplevel(app_screen)
    modifywindow.geometry("350x300")
    modifywindow.title(app_screen.title() + " Modify")
    cont = 0
    mystr = ["v0"]
    myvars = vars()
    con1 = odbc.connect(connection_string)
    cur1 = con1.cursor()
    for i, j in zip(record, names[valoare:]):
        jtemp = j
        for itemp in mapare:
            if itemp[0] == j:
                jtemp = itemp[3]
                break
        jtemp = jtemp.replace("_", " ")
        if app_screen.title() == "BonAngajat" and j != "bonfiscal_id" and j != "prettotal":
            Label(modifywindow, text=jtemp).grid(column=0, row=cont)
        elif app_screen.title() != "BonAngajat":
            Label(modifywindow, text=jtemp).grid(column=0, row=cont)
        placeholder.set("a" + str(cont))
        myvars[mystr[cont]] = StringVar()
        myvars[mystr[cont]].set(str(i))
        if j == "produs_id":
            cur1.execute("SELECT nume_produs FROM Produse")
            produse = cur1.fetchall()
            cur1.execute("SELECT produs_id FROM Produse")
            idproduse = cur1.fetchall()
            produsearr = []
            idprodusearr = []
            for q, k in zip(produse, idproduse):
                produsearr.append(q[0])
                idprodusearr.append(k[0])
            valle = StringVar(value="")
            valle.set(myvars[mystr[cont]].get())

            def textget(_):
                for qq, kk in zip(produsearr, idprodusearr):
                    if valle.get() == qq:
                        myvars[mystr[tempcont]].set(str(kk))
                        break

            tempcont = cont
            textget(0)
            OptionMenu(modifywindow, valle, *produsearr, command=textget).grid(column=1, row=cont)
        elif j == "supervizor_id":
            cur1.execute("SELECT CONCAT(nume, ' ', prenume) FROM Angajati")
            sup = cur1.fetchall()
            cur1.execute("SELECT angajat_id FROM Angajati ORDER BY angajat_id")
            idsup = cur1.fetchall()
            suparr = ["None"]
            idsuparr = ["NULL"]
            for q, k in zip(sup, idsup):
                suparr.append(q[0])
                idsuparr.append(k[0])
            valles = StringVar(value="")
            valles.set(myvars[mystr[cont]].get())

            def textgets(_):
                for qq, kk in zip(suparr, idsuparr):
                    if valles.get() == qq:
                        myvars[mystr[tempconts]].set(str(kk))
                        break

            tempconts = cont
            textgets(0)
            OptionMenu(modifywindow, valles, *suparr, command=textgets).grid(column=1, row=cont)
        elif j == "departament_id":
            cur1.execute("SELECT nume_departament FROM Departamente")
            dep = cur1.fetchall()
            cur1.execute("SELECT departament_id FROM Departamente")
            iddep = cur1.fetchall()
            deparr = []
            iddeparr = []
            for q, k in zip(dep, iddep):
                deparr.append(q[0])
                iddeparr.append(k[0])
            valled = StringVar(value="")
            valled.set(myvars[mystr[cont]].get())

            def textgetd(_):
                for qq, kk in zip(deparr, iddeparr):
                    if valled.get() == qq:
                        myvars[mystr[tempcontdep]].set(str(kk))
                        break

            tempcontdep = cont
            textgetd(0)
            OptionMenu(modifywindow, valled, *deparr, command=textgetd).grid(column=1, row=cont)
        elif j == "manager_id":
            cur1.execute("SELECT CONCAT(nume, ' ', prenume) FROM Angajati")
            man = cur1.fetchall()
            cur1.execute("SELECT angajat_id FROM Angajati ORDER BY angajat_id")
            idman = cur1.fetchall()
            manarr = []
            idmanarr = []
            for q, k in zip(man, idman):
                manarr.append(q[0])
                idmanarr.append(k[0])
            vallem = StringVar(value="")
            vallem.set(myvars[mystr[cont]].get())

            def textgetm(_):
                for qq, kk in zip(manarr, idmanarr):
                    if vallem.get() == qq:
                        myvars[mystr[tempcontman]].set(str(kk))
                        break

            tempcontman = cont
            textgetm(0)
            OptionMenu(modifywindow, vallem, *manarr, command=textgetm).grid(column=1, row=cont)
        elif j == "angajat_id":
            cur1.execute("SELECT CONCAT(nume, ' ', prenume) FROM Angajati WHERE departament_id = 2")
            ang = cur1.fetchall()
            cur1.execute("SELECT angajat_id FROM Angajati WHERE departament_id = 2 ORDER BY angajat_id")
            idang = cur1.fetchall()
            angarr = []
            idangarr = []
            for q, k in zip(ang, idang):
                angarr.append(q[0])
                idangarr.append(k[0])
            vallea = StringVar(value="")
            vallea.set(myvars[mystr[cont]].get())

            def textgeta(_):
                for qq, kk in zip(angarr, idangarr):
                    if vallea.get() == qq:
                        myvars[mystr[tempcontang]].set(str(kk))
                        break

            tempcontang = cont
            textgeta(1)
            OptionMenu(modifywindow, vallea, *angarr, command=textgeta).grid(column=1, row=cont)
        elif j == "producator_id":
            cur1.execute("SELECT nume_producator FROM Producatori")
            pro = cur1.fetchall()
            cur1.execute("SELECT producator_id FROM Producatori")
            idpro = cur1.fetchall()
            proarr = []
            idproarr = []
            for q, k in zip(pro, idpro):
                proarr.append(q[0])
                idproarr.append(k[0])
            vallep = StringVar(value="")
            vallep.set(myvars[mystr[cont]].get())

            def textgetp(_):
                for qq, kk in zip(proarr, idproarr):
                    if vallep.get() == qq:
                        myvars[mystr[tempcontpro]].set(str(kk))
                        break

            tempcontpro = cont
            textgetp(1)
            OptionMenu(modifywindow, vallep, *proarr, command=textgetp).grid(column=1, row=cont)
        else:
            if app_screen.title() == "BonAngajat" and j != "bonfiscal_id" and j != "prettotal":
                Entry(modifywindow, name="entry" + str(cont), textvariable=myvars[mystr[cont]]).grid(column=1, row=cont)
            elif app_screen.title() != "BonAngajat":
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
    for selected_item in tree.selection():
        item = tree.item(selected_item)
        idnum = rows[int(selected_item[1:], 16) - 1][0]
        record = item['values']
        modifyvalues()


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
    valoare = 0 if valoare[0][0] > 1 or app_screen.title() == "BonAngajat" else 1
    for _ in names[valoare:]:
        columnTuple.append("c" + str(count))
        count = count + 1
    columnTuple = tuple(columnTuple)
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
        return maxlength

    j = 1
    suma = 0
    vec = []
    vecname = []
    vectable = []
    vecswap = []
    ii = 0
    for i in names[valoare:]:
        for k in mapare:
            if k[0] == i:
                i = k[3]
                vecname.append(k[0])
                vectable.append(k[1])
                vecswap.append(k[2])
                vec.append(ii)
        value = maxlen(j - 1)
        suma += max(value * 7, len(i) * 9)
        i = i.replace("_", " ")
        tree.column("#" + str(j), width=value * 6, minwidth=max(len(i) * 9, value * 7))
        tree.heading("#" + str(j), text=i)
        j = j + 1
        ii += 1
    if suma > 1000:
        tree.column("#" + str(j - 1), width=2500 - suma)
    tree.bind('<<TreeviewSelect>>', item_selected)
    tree.pack(fill='x', expand=YES)
    count = 0
    for row in rows:
        for k in vec:
            if app_screen.title() == "BonAngajat":
                cur1.execute("SELECT CONCAT(nume, ' ', prenume) FROM Angajati WHERE angajat_id=" + str(row[1]))
                row = list(row)
                row[1] = cur1.fetchall()[0][0]
                row = tuple(row)
                break
            if str(row[k + 1]) != "None":
                t = k if valoare == 0 else k + 1
                vecname[t - 1] = "angajat_id" if vecname[t - 1] == "manager_id" or vecname[
                    t - 1] == "supervizor_id" else vecname[t - 1]
                cur1.execute(
                    "SELECT " + vecswap[t - 1] + " FROM " + vectable[t - 1] + " WHERE " + vecname[t - 1] + " = " + str(
                        row[t]))
                curval = cur1.fetchall()
                row = list(row)
                row[t] = curval[0][0]
                row = tuple(row)

        if count % 2 == 0:
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

    reg_success()


def reg_success():
    user_not_found_screen = Toplevel(main_screen)
    user_not_found_screen.title("INFO")
    user_not_found_screen.geometry("250x100")
    Label(user_not_found_screen, text="Registered successfully").pack()
    Label(user_not_found_screen, text="").pack()
    Button(user_not_found_screen, text="OK", command=user_not_found_screen.destroy).pack()


def login_verify():
    username1 = username_verify.get()
    password1 = password_verify.get()
    username_login_entry.delete(0, END)
    password_login_entry.delete(0, END)

    list_of_files = os.listdir(
        "../../OneDrive - Universitatea Politehnica Bucuresti/Anul 3/BD/De trimis/ProiectBD/Users\\")
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
